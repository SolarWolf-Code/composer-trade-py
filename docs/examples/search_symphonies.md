# Search for public symphonies meeting specific criteria.

```python
"""
Search for public symphonies meeting specific criteria.
This example shows available symphonies with their metadata and runs a quick backtest.
"""

from composer import ComposerClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

print("Searching for public symphonies...\n")

# Search for symphonies (without filter since oos fields may not be populated)
results = client.search.search_symphonies_v2(
    offset=0,
)

print(f"Found {len(results)} public symphonies\n")

print("="*120)
print("SEARCH RESULTS")
print("="*120)

# Display results in a table with available fields
print(f"\n{'#':<3} {'Name':<40} {'Assets':>8} {'Filters':>8} {'Rebalance':<10} {'ID':<12}")
print("-"*120)

for i, symphony in enumerate(results[:15], 1):
    name = (symphony.name[:37] + "...") if symphony.name and len(symphony.name) > 40 else (symphony.name or "N/A")
    
    assets = symphony.num_node_asset or 0
    filters = symphony.num_node_filter or 0
    rebal = symphony.rebalance_frequency or "N/A"
    sid = symphony.symphony_sid[:12]
    
    print(f"{i:<3} {name:<40} {assets:>8} {filters:>8} {rebal:<10} {sid:<12}")

print("\n" + "="*120)

# Show details for top result including AI description
if results:
    top_result = results[0]
    print(f"\n--- TOP RESULT DETAILS ---")
    print(f"\nName: {top_result.name or 'N/A'}")
    print(f"ID: {top_result.symphony_sid}")
    print(f"Description: {top_result.description or 'N/A'}")
    print(f"Asset Classes: {', '.join(top_result.asset_classes) if top_result.asset_classes else 'N/A'}")
    print(f"Rebalance Frequency: {top_result.rebalance_frequency or 'N/A'}")
    print(f"\nStructure:")
    print(f"  - Assets: {top_result.num_node_asset}")
    print(f"  - Filters: {top_result.num_node_filter}")
    print(f"  - Groups: {top_result.num_node_group}")
    print(f"  - IF Nodes: {top_result.num_node_if}")
    
    if top_result.ai_description:
        ai = top_result.ai_description
        print(f"\nAI Summary: {ai.summary or 'N/A'}")
        print(f"\nCategories: {ai.categories or 'N/A'}")
    
    # Run a quick backtest to get performance metrics
    print(f"\n--- RUNNING 30-DAY BACKTEST ---")
    print("-"*50)
    
    from datetime import datetime, timedelta
    
    end_date = datetime.now().date().isoformat()
    start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
    
    backtest = client.public_symphony.backtest_symphony_v2(
        top_result.symphony_sid,
        start_date=start_date,
        end_date=end_date,
    )
    
    if backtest.stats:
        stats = backtest.stats
        print(f"Sharpe Ratio: {stats.sharpe_ratio:.2f}" if stats.sharpe_ratio else "Sharpe: N/A")
        print(f"Cumulative Return: {stats.cumulative_return*100:+.2f}%" if stats.cumulative_return else "Cumulative Return: N/A")
        print(f"Max Drawdown: {stats.max_drawdown*100:.2f}%" if stats.max_drawdown else "Max Drawdown: N/A")
        print(f"Annualized Return: {stats.annualized_rate_of_return*100:+.2f}%" if stats.annualized_rate_of_return else "Annualized Return: N/A")
    
    # Show daily values
    if backtest.dvm_capital:
        print(f"\nDaily values (last 5 days):")
        dates = sorted(backtest.dvm_capital.keys(), reverse=True)[:5]
        for date in dates:
            if top_result.symphony_sid in backtest.dvm_capital[date]:
                value = backtest.dvm_capital[date][top_result.symphony_sid]
                print(f"  {date}: ${value:,.2f}")

print("\n" + "="*120)
print("FILTER OPTIONS")
print("="*120)
print("""
You can filter by various fields. Some available filters:
  - asset_classes (e.g., "CRYPTO" in asset_classes)
  - rebalance_frequency (e.g., rebalance_frequency == 'daily')
  - num_node_asset, num_node_filter, num_node_group
  - oos_* fields (may not always be populated)
  
Examples:
  - filter="rebalance_frequency == 'daily'"
  - filter="'CRYPTO' in asset_classes"
  - filter="num_node_asset > 100"
  
You can also sort by any field:
  - order_by=[["num_node_asset", "desc"]]
  - order_by=[["rebalance_frequency", "asc"]]
""")
```

**Output:**
```
Searching for public symphonies...

Found 5 public symphonies

========================================================================================================================
SEARCH RESULTS
========================================================================================================================

#   Name                                       Assets  Filters Rebalance  ID          
------------------------------------------------------------------------------------------------------------------------
1   Revised Gold Digger                            10        0 daily      nODZigmFcKBm
2   Core - Allana Tactical Momentum               442       34 daily      fLQfosCfkFqb
3   Macro on top Pals Minor Spell of Summ...      157        9 daily      ZKBZN6MTCjsw
4   Copy of MSTR FTLT + MSTR Nested + MST...      278        0 daily      1A4cveqbh3YU
5   Jerry Five Inv Vol 200d                         6        0 daily      wtIOhEGiLO98

========================================================================================================================

--- TOP RESULT DETAILS ---

Name: Revised Gold Digger
ID: nODZigmFcKBmvBmbuzae
Description: (Created with Composer AI)
Asset Classes: EQUITIES
Rebalance Frequency: daily

Structure:
  - Assets: 10
  - Filters: 0
  - Groups: 0
  - IF Nodes: 5

AI Summary: N/A

Categories: N/A

--- RUNNING 30-DAY BACKTEST ---
--------------------------------------------------
Sharpe Ratio: 0.14
Cumulative Return: -17.31%
Max Drawdown: 46.15%
Annualized Return: -91.96%

Daily values (last 5 days):
  2026-02-13: $8,268.85
  2026-02-12: $7,096.09
  2026-02-11: $9,130.38
  2026-02-10: $8,429.58
  2026-02-09: $8,418.63

========================================================================================================================
FILTER OPTIONS
========================================================================================================================

You can filter by various fields. Some available filters:
  - asset_classes (e.g., "CRYPTO" in asset_classes)
  - rebalance_frequency (e.g., rebalance_frequency == 'daily')
  - num_node_asset, num_node_filter, num_node_group
  - oos_* fields (may not always be populated)

Examples:
  - filter="rebalance_frequency == 'daily'"
  - filter="'CRYPTO' in asset_classes"
  - filter="num_node_asset > 100"

You can also sort by any field:
  - order_by=[["num_node_asset", "desc"]]
  - order_by=[["rebalance_frequency", "asc"]]
```
