"""Symphony conversion utilities."""

import json
import hashlib
from collections import OrderedDict
from enum import Enum
from pathlib import Path
from pydantic import BaseModel

try:
    import ruff

    HAS_RUFF = True
except ImportError:
    HAS_RUFF = False


def to_source(obj, indent=0, dedup_map=None, emitted_vars=None):
    """Recursively convert an object to Python source code.

    Handles BaseModel, Enum, list, dict, and primitives.
    If dedup_map and emitted_vars provided, handles deduplication.

    Args:
        obj: The object to convert
        indent: Current indentation level
        dedup_map: Dict mapping node id to variable name for deduplication
        emitted_vars: Dict to store emitted variable definitions

    Returns:
        Python source code as string
    """
    spacing = " " * indent

    if dedup_map is None:
        dedup_map = {}
    if emitted_vars is None:
        emitted_vars = {}

    # Check if this is a deduplicated node
    if isinstance(obj, BaseModel):
        obj_id = id(obj)
        if obj_id in dedup_map:
            var_name = dedup_map[obj_id]
            if var_name not in emitted_vars:
                # First time - generate the full code and store it
                emitted_vars[var_name] = None  # Placeholder to avoid recursion
                full_code = _generate_model_code(obj, indent, dedup_map, emitted_vars)
                emitted_vars[var_name] = full_code
            return var_name

    if isinstance(obj, BaseModel):
        return _generate_model_code(obj, indent, dedup_map, emitted_vars)

    elif isinstance(obj, list):
        if not obj:
            return "[]"
        lines = ["["]
        for item in obj:
            rendered = to_source(item, indent + 4, dedup_map, emitted_vars)
            lines.append(" " * (indent + 4) + f"{rendered},")
        lines.append(spacing + "]")
        return "\n".join(lines)

    elif isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = ["{"]
        for key, value in obj.items():
            rendered_key = to_source(key, indent + 4, dedup_map, emitted_vars)
            rendered_value = to_source(value, indent + 4, dedup_map, emitted_vars)
            lines.append(" " * (indent + 4) + f"{rendered_key}: {rendered_value},")
        lines.append(spacing + "}")
        return "\n".join(lines)

    elif isinstance(obj, Enum):
        return f"{obj.__class__.__name__}.{obj.name}"

    elif isinstance(obj, str):
        return repr(obj)

    else:
        return repr(obj)


def _generate_model_code(obj, indent, dedup_map, emitted_vars):
    """Generate Python code for a BaseModel instance."""
    spacing = " " * indent
    cls_name = obj.__class__.__name__
    lines = [f"{cls_name}("]

    for key in type(obj).model_fields:
        value = getattr(obj, key)
        if value is None:
            continue
        rendered = to_source(value, indent + 4, dedup_map, emitted_vars)
        lines.append(" " * (indent + 4) + f"{key}={rendered},")

    lines.append(spacing + ")")
    return "\n".join(lines)


def _node_to_dict(node, exclude_ids=True):
    """Convert a node to a canonical dict for hashing.

    Args:
        node: The node to convert
        exclude_ids: If True, exclude 'id' fields from hash (for deduplication)

    Returns:
        OrderedDict representation of the node
    """
    if isinstance(node, BaseModel):
        step = getattr(node, "step", None)
        if step is None:
            return {"__type__": node.__class__.__name__}

        result = OrderedDict()
        result["step"] = step
        result["__type__"] = node.__class__.__name__

        # Get all field values
        for key in type(node).model_fields:
            # Skip id fields when computing hash for deduplication
            if exclude_ids and key == "id":
                continue

            value = getattr(node, key)
            if value is None:
                continue

            if isinstance(value, Enum):
                result[key] = value.value
            elif isinstance(value, BaseModel):
                result[key] = _node_to_dict(value, exclude_ids)
            elif isinstance(value, list):
                result[key] = [
                    _node_to_dict(item, exclude_ids) if isinstance(item, BaseModel) else item
                    for item in value
                ]
            elif isinstance(value, dict):
                result[key] = {
                    k: _node_to_dict(v, exclude_ids) if isinstance(v, BaseModel) else v
                    for k, v in value.items()
                }
            else:
                result[key] = value

        return result
    return node


def _compute_hash(node, exclude_ids=True):
    """Compute a canonical hash for a node."""
    node_dict = _node_to_dict(node, exclude_ids)
    json_str = json.dumps(node_dict, sort_keys=True, default=str)
    full_hash = hashlib.sha256(json_str.encode()).hexdigest()
    return full_hash[:8]


def _count_hashes(node, hash_counts, hash_cache):
    """Count occurrences of each hash (pre-order traversal)."""
    node_hash = _compute_hash(node)
    hash_cache[id(node)] = node_hash
    hash_counts[node_hash] = hash_counts.get(node_hash, 0) + 1

    if hasattr(node, "children"):
        for child in node.children:
            _count_hashes(child, hash_counts, hash_cache)


def _make_var_name(node, hash_str):
    """Generate a descriptive variable name for a deduplicated node."""
    step = getattr(node, "step", "node")
    name = getattr(node, "name", "")

    # Map step to a cleaner prefix
    step_map = {
        "group": "group",
        "wt-cash-equal": "wce",
        "wt-cash-specified": "wcs",
        "wt-inverse-vol": "wiv",
        "if": "ifnode",
        "if-child": "ifchild",
        "filter": "filter",
        "asset": "asset",
        "root": "symphony",
    }
    prefix = step_map.get(step, step.replace("-", "_"))

    # Sanitize name
    if name:
        clean_name = name.lower().replace(" ", "_")
        clean_name = "".join(c for c in clean_name if c.isalnum() or c == "_")
        clean_name = clean_name[:20]  # Truncate
        if clean_name:
            return f"{prefix}_{clean_name}_{hash_str}"

    return f"{prefix}_{hash_str}"


def _extract_dependencies(code, var_names):
    """Extract variable dependencies from generated code.

    Args:
        code: The generated Python code for a variable
        var_names: Set of all deduplicated variable names

    Returns:
        Set of variable names that this code depends on
    """
    dependencies = set()
    for var_name in var_names:
        if var_name in code and f"{var_name} =" not in code:
            dependencies.add(var_name)
    return dependencies


def _topological_sort(emitted_vars):
    """Sort variables by dependencies using topological sort.

    Ensures that if variable A references variable B, then B is defined before A.

    Args:
        emitted_vars: Dict mapping variable name to generated code

    Returns:
        List of variable names in dependency order
    """
    var_names = set(emitted_vars.keys())
    graph = {v: [] for v in var_names}
    in_degree = {v: 0 for v in var_names}

    for var_name, code in emitted_vars.items():
        deps = _extract_dependencies(code, var_names)
        for dep in deps:
            if dep in var_names:
                graph[dep].append(var_name)
                in_degree[var_name] += 1

    queue = [v for v in var_names if in_degree[v] == 0]
    sorted_vars = []

    while queue:
        node = queue.pop(0)
        sorted_vars.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_vars) != len(var_names):
        sorted_vars = list(var_names)

    return sorted_vars


def symphony_to_python(
    score,
    output=None,
    dedup=False,
    min_hits=2,
    show_stats=False,
    symphony_id=None,
):
    """Convert a SymphonyScore to a Python definition file.

    Args:
        score: A SymphonyScore object from the API
        output: Output filename, defaults to {symphony_id}.py
        dedup: Enable deduplication of repeated Groups (default: False)
        min_hits: Minimum occurrences to trigger deduplication (default: 2)
        show_stats: Print deduplication statistics (default: False)
        symphony_id: Optional symphony ID to use in the output (defaults to score.id)

    Returns:
        The output filename that was written
    """
    # Use provided symphony_id or fall back to score.id
    if symphony_id is None:
        symphony_id = score.id

    # Determine output file
    if output is None:
        output = f"{symphony_id}.py"

    if dedup:
        # Pass 1: Count all hashes
        hash_counts = {}
        hash_cache = {}
        _count_hashes(score, hash_counts, hash_cache)

        # Show stats if requested
        if show_stats:
            sorted_hashes = sorted(hash_counts.items(), key=lambda x: x[1], reverse=True)
            print(f"\n=== Hash Cache Statistics for {symphony_id} ===")
            print(f"Total unique hashes: {len(hash_counts)}")
            print(
                f"\nTop 20 most frequent blocks (only Groups with ≥{min_hits} hits will be deduplicated):"
            )
            print("-" * 60)
            print(f"{'Hash':<12} {'Count':<8} {'Type':<15} {'Status'}")
            print("-" * 60)

            # Build a map of hash -> node type for display
            hash_to_type = {}

            def map_hash_to_type(node, hash_cache):
                node_hash = hash_cache.get(id(node))
                if node_hash:
                    step = getattr(node, "step", "unknown")
                    hash_to_type[node_hash] = step
                if hasattr(node, "children"):
                    for child in node.children:
                        map_hash_to_type(child, hash_cache)

            # Need to recompute hashes to get the mapping
            temp_cache = {}
            _count_hashes(score, {}, temp_cache)
            map_hash_to_type(score, temp_cache)

            for h, count in sorted_hashes[:20]:
                node_type = hash_to_type.get(h, "unknown")
                is_group = node_type == "group"
                is_eligible = count >= min_hits and is_group

                if is_eligible:
                    status = "WILL DEDUP"
                else:
                    status = "inline"
                print(f"_{h:<11} {count:<8} {node_type:<15} {status}")
            print("-" * 60)

            # Count totals
            total_dedup = sum(
                1
                for h, c in hash_counts.items()
                if c >= min_hits and hash_to_type.get(h) == "group"
            )

            print(f"Total Groups to deduplicate: {total_dedup}")
            print(f"Total other blocks: {len(hash_counts) - total_dedup}")
            print()

        # Pass 2: Build dedup_map for Groups with count >= min_hits
        dedup_map = {}

        def build_dedup_map(node, hash_cache, hash_counts, min_hits):
            node_hash = hash_cache.get(id(node))
            if node_hash:
                step = getattr(node, "step", None)
                hit_count = hash_counts.get(node_hash, 0)

                if step == "group" and hit_count >= min_hits:
                    var_name = _make_var_name(node, node_hash)
                    dedup_map[id(node)] = var_name

            if hasattr(node, "children"):
                for child in node.children:
                    build_dedup_map(child, hash_cache, hash_counts, min_hits)

        # Recompute hash cache for this pass
        hash_cache = {}
        _count_hashes(score, {}, hash_cache)
        build_dedup_map(score, hash_cache, hash_counts, min_hits)

        # Pass 3: Generate code with deduplication
        emitted_vars = {}
        main_code = to_source(score, 0, dedup_map, emitted_vars)
    else:
        # No deduplication
        dedup_map = {}
        emitted_vars = {}
        main_code = to_source(score, 0, dedup_map, emitted_vars)

    # Fix the main symphony variable name
    main_code = main_code.replace("SymphonyDefinition(", "symph = SymphonyDefinition(", 1)

    # Generate imports
    header = f'''"""Symphony definition for {symphony_id}"""
from composer.models.common.symphony import *
from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

'''

    # Generate deduplicated variables section
    variables_code = ""
    if emitted_vars:
        variables_code = "# Deduplicated components\n"
        sorted_var_names = _topological_sort(emitted_vars)
        for var_name in sorted_var_names:
            code = emitted_vars[var_name]
            variables_code += f"{var_name} = {code}\n\n"
        variables_code += "\n"

    # Generate footer with backtest code
    footer = f"""
# Backtest
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

res = client.backtest.run_v2(symphony=symph)
print(res)
"""

    # Assemble final code
    full_code = header + variables_code + main_code + footer

    # Write output file
    with open(output, "w") as f:
        f.write(full_code)

    # Format with ruff if available
    if HAS_RUFF:
        import subprocess

        subprocess.run(
            ["ruff", "format", output],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    print(f"Saved to {output}")

    return output
