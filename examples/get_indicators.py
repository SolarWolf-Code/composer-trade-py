"""
Example: Get technical indicators from the Backtest API.

This demonstrates how to use the public_symphony.get_indicators() endpoint
which does NOT require authentication.

Usage:
    python examples/get_indicators.py
"""

from composer import ComposerClient

# Initialize client - credentials not needed for public endpoints
client = ComposerClient(
    api_key="dummy",  # Required but not used for public endpoints
    api_secret="dummy",
)

# Get all available technical indicators
print("Fetching indicators from Backtest API...")
indicators = client.public_symphony.get_indicators()

print(f"\nFound {len(indicators)} indicators:\n")

for ind in indicators:
    print(f"  {ind.name}")
    print(f"    Key: {ind.key}")
    print(f"    Code: {ind.composer_code_name}")
    print(f"    Unit: {ind.unit}")
    print(f"    Beta: {ind.beta}")
    print(f"    Asset Only: {ind.asset_only}")
    if ind.description:
        print(f"    Description: {ind.description}")
    if ind.parameters:
        print(f"    Parameters:")
        for param in ind.parameters:
            print(
                f"      - {param.name} ({param.type}): default={param.default_value}, range=[{param.min_value}, {param.max_value}]"
            )
    print()
