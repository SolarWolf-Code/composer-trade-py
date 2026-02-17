# Removes asset names from score - usefull when builing large symphonies

```python
"""
Removes asset names from score - usefull when builing large symphonies
"""

from composer import ComposerClient
from composer.models.common.symphony import Asset
import os
import copy
import json
import sys
from dotenv import load_dotenv

load_dotenv()

def sizeof_object(obj):
    """
    Estimate object size by JSON serializing it.
    Falls back to sys.getsizeof if serialization fails.
    """
    try:
        serialized = json.dumps(obj, default=lambda o: o.__dict__)
        return len(serialized.encode("utf-8"))
    except Exception:
        return sys.getsizeof(obj)


def human_readable_size(num_bytes):
    """
    Convert bytes into a human readable string.
    """
    for unit in ["bytes", "KB", "MB", "GB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:,.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:,.2f} TB"



client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get symphony score
score = client.user_symphony.get_score("BvXV5Ndkou804ejl9Hbf")

original_size = sizeof_object(score)

cleaned_score = copy.deepcopy(score)

# Remove name from all asset classes
def remove_asset_names(node):
    """Recursively remove name from all Asset nodes."""
    if isinstance(node, Asset):
        node.name = None
    elif hasattr(node, "children") and node.children:
        for child in node.children:
            remove_asset_names(child)

# Process copied score
if cleaned_score.children:
    for child in cleaned_score.children:
        remove_asset_names(child)

cleaned_size = sizeof_object(cleaned_score)


print("\n--- Size Comparison ---")
print(f"Original Size: {human_readable_size(original_size)}")
print(f"Cleaned Size:  {human_readable_size(cleaned_size)}")
print(
    f"Difference:    {human_readable_size(original_size - cleaned_size)} "
    f"({((original_size - cleaned_size) / original_size * 100):.2f}% smaller)"
)
```

**Output:**
```

--- Size Comparison ---
Original Size: 11.06 KB
Cleaned Size:  10.66 KB
Difference:    409.00 bytes (3.61% smaller)
```
