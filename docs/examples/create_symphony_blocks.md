# Create a symphony programmatically with reusable block definitions.

```python
"""
Create a symphony programmatically with reusable block definitions.

This example demonstrates how to define a group of assets once as a variable
and reference it in multiple places. This makes it easy to update the same
assets in multiple locations by changing just one variable.
"""

from composer import ComposerClient
from composer.models.common.symphony import (
    Asset,
    WeightCashEqual,
    Group,
    SymphonyDefinition,
    WeightMap,
)
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# =============================================================================
# DEFINE REUSABLE BLOCKS
# =============================================================================
# Here's the key: define your asset group as a variable ONCE, then reference
# it multiple times. When you want to change a ticker, just update here!

# Create a weight block with equal weight across these assets
tech_weight_block = WeightCashEqual(
    children=[
        Asset(ticker="MSFT", name="Microsoft Corporation", exchange="XNAS"),
        Asset(ticker="AAPL", name="Apple Inc", exchange="XNAS"),
        Asset(ticker="GOOG", name="Alphabet Inc Class A", exchange="XNAS"),
    ]
)


# =============================================================================
# USE THE BLOCK MULTIPLE TIMES
# =============================================================================
# Reference the same block multiple times in the symphony structure.
# The structure is: SymphonyDefinition -> WeightCashEqual -> [Group, Group]
# Note: IDs are auto-generated as proper UUIDs if not provided

symphony = SymphonyDefinition(
    name="Tech Block Reference Demo",
    description="Demonstrates using the same block in multiple places",
    rebalance="daily",
    children=[
        # Single WeightCashEqual containing multiple Groups (the reusable blocks)
        WeightCashEqual(
            children=[
                # First reference: Group 1 (same tech_weight_block!)
                Group(
                    name="Tech Group 1",
                    collapsed=False,
                    children=[tech_weight_block],
                ),
                # Second reference: Group 2 (same tech_weight_block!)
                Group(
                    name="Tech Group 2",
                    collapsed=False,
                    children=[tech_weight_block],
                ),
            ]
        ),
    ],
)

print("Created symphony definition with block referenced twice")
print()


# =============================================================================
# PRINT THE MODEL DUMP
# =============================================================================
print("=" * 60)
print("SYMPHONY STRUCTURE (model_dump)")
print("=" * 60)
print(json.dumps(symphony.model_dump(by_alias=True, mode="json"), indent=2))
print()


# =============================================================================
# DEMONSTRATE THE POWER OF VARIABLES: CHANGE ONE PLACE
# =============================================================================
print("=" * 60)
print("UPDATING THE BLOCK")
print("=" * 60)
print("\nNow let's change GOOG to NVDA - this updates BOTH references!")
print()

# Recreate the blocks with the updated assets
tech_weight_block_updated = WeightCashEqual(
    children=[
        Asset(ticker="MSFT", name="Microsoft Corporation", exchange="XNAS"),
        Asset(ticker="AAPL", name="Apple Inc", exchange="XNAS"),
        Asset(ticker="NVDA", name="NVIDIA Corporation", exchange="XNAS"),  # Changed from GOOG
    ]
)

# Create a new symphony with the updated block
symphony_updated = SymphonyDefinition(
    name="Tech Block Reference Demo - NVDA",
    description="Demonstrates using the same block in multiple places - NVDA version",
    rebalance="daily",
    children=[
        WeightCashEqual(
            children=[
                Group(
                    name="Tech Group 1",
                    collapsed=False,
                    children=[tech_weight_block_updated],
                ),
                Group(
                    name="Tech Group 2",
                    collapsed=False,
                    children=[tech_weight_block_updated],
                ),
            ]
        ),
    ],
)

print("Updated symphony with NVDA instead of GOOG:")
print(json.dumps(symphony_updated.model_dump(by_alias=True, mode="json"), indent=2))
print()


# =============================================================================
# CREATE THE SYMPHONY
# =============================================================================
# To actually create the symphony in your account, uncomment this:
#
result = client.user_symphony.create_symphony(
    name="Tech Block Reference Demo - NVDA",
    color="#829DFF",
    hashtag="#tech",
    symphony=symphony_updated,
)
print(f"Created symphony: {result.symphony_id}")
```

**Output:**
```
Created symphony definition with block referenced twice

============================================================
SYMPHONY STRUCTURE (model_dump)
============================================================
{
  "id": "8e8a7519-c1ee-4fdf-8f64-43a7b0094107",
  "weight": null,
  "step": "root",
  "name": "Tech Block Reference Demo",
  "description": "Demonstrates using the same block in multiple places",
  "rebalance": "daily",
  "rebalance-corridor-width": null,
  "children": [
    {
      "id": "3dce60ef-0b30-4ab6-8185-5d8d2e9242a5",
      "weight": null,
      "step": "wt-cash-equal",
      "children": [
        {
          "id": "b2370df1-3da3-45e1-9e6d-a2c69af16c28",
          "weight": null,
          "step": "group",
          "name": "Tech Group 1",
          "children": [
            {
              "id": "6013ddbd-aa27-4de9-84c9-663fadf08b0e",
              "weight": null,
              "step": "wt-cash-equal",
              "children": [
                {
                  "id": "4025f368-b583-431f-937c-cb3ee866fb03",
                  "weight": null,
                  "step": "asset",
                  "name": "Microsoft Corporation",
                  "ticker": "MSFT",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "7cd47761-f693-4fb6-92e1-4e6182e8f1fe",
                  "weight": null,
                  "step": "asset",
                  "name": "Apple Inc",
                  "ticker": "AAPL",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "293e3007-bb04-40b5-8442-bbde47274ed1",
                  "weight": null,
                  "step": "asset",
                  "name": "Alphabet Inc Class A",
                  "ticker": "GOOG",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                }
              ]
            }
          ]
        },
        {
          "id": "9cc0f133-0336-4f94-a8d5-e9a422afe25a",
          "weight": null,
          "step": "group",
          "name": "Tech Group 2",
          "children": [
            {
              "id": "6013ddbd-aa27-4de9-84c9-663fadf08b0e",
              "weight": null,
              "step": "wt-cash-equal",
              "children": [
                {
                  "id": "4025f368-b583-431f-937c-cb3ee866fb03",
                  "weight": null,
                  "step": "asset",
                  "name": "Microsoft Corporation",
                  "ticker": "MSFT",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "7cd47761-f693-4fb6-92e1-4e6182e8f1fe",
                  "weight": null,
                  "step": "asset",
                  "name": "Apple Inc",
                  "ticker": "AAPL",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "293e3007-bb04-40b5-8442-bbde47274ed1",
                  "weight": null,
                  "step": "asset",
                  "name": "Alphabet Inc Class A",
                  "ticker": "GOOG",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}

============================================================
UPDATING THE BLOCK
============================================================

Now let's change GOOG to NVDA - this updates BOTH references!

Updated symphony with NVDA instead of GOOG:
{
  "id": "7a283509-3520-457e-b00b-9fc77b772485",
  "weight": null,
  "step": "root",
  "name": "Tech Block Reference Demo - NVDA",
  "description": "Demonstrates using the same block in multiple places - NVDA version",
  "rebalance": "daily",
  "rebalance-corridor-width": null,
  "children": [
    {
      "id": "b0dc18c8-ee04-4518-98ee-63f54d53fe4d",
      "weight": null,
      "step": "wt-cash-equal",
      "children": [
        {
          "id": "633353b4-242a-42d2-8357-8f21efeb8b89",
          "weight": null,
          "step": "group",
          "name": "Tech Group 1",
          "children": [
            {
              "id": "432a9772-76d9-459d-aa33-c0cd37c713e3",
              "weight": null,
              "step": "wt-cash-equal",
              "children": [
                {
                  "id": "cbd7b4cb-8d61-4d51-b976-c6543a6cf3b3",
                  "weight": null,
                  "step": "asset",
                  "name": "Microsoft Corporation",
                  "ticker": "MSFT",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "0ae9f5f2-67c2-4de2-b515-49fb5995bd2e",
                  "weight": null,
                  "step": "asset",
                  "name": "Apple Inc",
                  "ticker": "AAPL",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "65c6c58a-782d-4260-ae34-f34e9f8fce2f",
                  "weight": null,
                  "step": "asset",
                  "name": "NVIDIA Corporation",
                  "ticker": "NVDA",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                }
              ]
            }
          ]
        },
        {
          "id": "c2d95c27-307c-4481-a012-e25ac9ceb89d",
          "weight": null,
          "step": "group",
          "name": "Tech Group 2",
          "children": [
            {
              "id": "432a9772-76d9-459d-aa33-c0cd37c713e3",
              "weight": null,
              "step": "wt-cash-equal",
              "children": [
                {
                  "id": "cbd7b4cb-8d61-4d51-b976-c6543a6cf3b3",
                  "weight": null,
                  "step": "asset",
                  "name": "Microsoft Corporation",
                  "ticker": "MSFT",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "0ae9f5f2-67c2-4de2-b515-49fb5995bd2e",
                  "weight": null,
                  "step": "asset",
                  "name": "Apple Inc",
                  "ticker": "AAPL",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                },
                {
                  "id": "65c6c58a-782d-4260-ae34-f34e9f8fce2f",
                  "weight": null,
                  "step": "asset",
                  "name": "NVIDIA Corporation",
                  "ticker": "NVDA",
                  "exchange": "XNAS",
                  "price": null,
                  "dollar_volume": null,
                  "has_marketcap": null,
                  "children-count": null
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}

Created symphony: 5cFvCQWDOaT4RaA7zVWW
```
