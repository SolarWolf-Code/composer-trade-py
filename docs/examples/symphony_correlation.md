# Calculate Pearson correlation between multiple symphonies using backtest data.

```python
"""
Calculate Pearson correlation between multiple symphonies using backtest data.
This example uses 3 symphonies and compares their daily % changes over a 1-year period.
"""

from composer import ComposerClient
from datetime import datetime, timedelta
import math
import os
from dotenv import load_dotenv

load_dotenv()

def mean(values):
    """Calculate the mean of a list of values."""
    return sum(values) / len(values)

def pearson_correlation(x, y):
    """
    Calculate Pearson correlation coefficient between two lists.
    r = sum((xi - mean_x) * (yi - mean_y)) / (sqrt(sum((xi - mean_x)^2)) * sqrt(sum((yi - mean_y)^2)))
    """
    if len(x) != len(y) or len(x) == 0:
        return 0
    
    mean_x = mean(x)
    mean_y = mean(y)
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x) * math.sqrt(sum_sq_y)
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

def extract_daily_pct_changes(backtest_result, symphony_id):
    """
    Extract daily percentage changes from backtest dvm_capital.
    Returns list of daily % changes.
    """
    if not backtest_result.dvm_capital:
        return []
    
    daily_values = []
    for date, series_dict in backtest_result.dvm_capital.items():
        if symphony_id in series_dict:
            daily_values.append((date, series_dict[symphony_id]))
    
    # Sort by date
    daily_values.sort(key=lambda x: x[0])
    
    # Calculate daily % changes
    pct_changes = []
    for i in range(1, len(daily_values)):
        prev_value = daily_values[i - 1][1]
        curr_value = daily_values[i][1]
        if prev_value != 0:
            pct_change = ((curr_value - prev_value) / prev_value) * 100
            pct_changes.append(pct_change)
    
    return pct_changes

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Define symphonies to analyze
symphonies = [
    "VPVpD1SoqR5ykVu4NdWS", # Holy Grail
    "rK0k16GLnmhNHuTYu2gz", # TQQQ FTLT
    "Y1g7n9BO3dsGknQlefo9", # QQQ FTLT + Bonds
]

# Define date range (last 1 year)
end_date = datetime.now().date().isoformat()
start_date = (datetime.now() - timedelta(days=365)).date().isoformat()

print(f"Analyzing correlations between {len(symphonies)} symphonies")
print(f"Date range: {start_date} to {end_date}\n")

# Run backtests and extract daily % changes
symphony_changes = {}

for symphony_id in symphonies:
    print(f"Running backtest for {symphony_id}...")
    
    backtest = client.public_symphony.backtest_symphony_v2(
        symphony_id,
        start_date=start_date,
        end_date=end_date,
    )
    
    pct_changes = extract_daily_pct_changes(backtest, symphony_id)
    symphony_changes[symphony_id] = pct_changes
    
    print(f"  -> {len(pct_changes)} days of data")
    
    if len(pct_changes) > 0:
        avg_change = mean(pct_changes)
        print(f"  -> Avg daily change: {avg_change:+.2f}%")

print("\n" + "="*50)
print("PEARSON CORRELATION MATRIX")
print("="*50 + "\n")

# Calculate correlation matrix
short_ids = [sid[:8] for sid in symphonies]

# Print header
print(f"{'Symphony':<12}", end="")
for sid in short_ids:
    print(f"{sid:>12}", end="")
print()
print("-" * (12 + 12 * len(symphonies)))

# Calculate and print each row
for i, sym_i in enumerate(symphonies):
    print(f"{short_ids[i]:<12}", end="")
    
    for j, sym_j in enumerate(symphonies):
        changes_i = symphony_changes[sym_i]
        changes_j = symphony_changes[sym_j]
        
        # Align to same length
        min_len = min(len(changes_i), len(changes_j))
        
        if min_len > 0 and i == j:
            corr = 1.0
        elif min_len > 0:
            corr = pearson_correlation(changes_i[:min_len], changes_j[:min_len])
        else:
            corr = 0.0
        
        print(f"{corr:>12.4f}", end="")
    print()

print("\n" + "="*50)
print("INTERPRETATION")
print("="*50)
print("""
- Values close to 1.0:  Strong positive correlation (move together)
- Values close to -1.0: Strong negative correlation (move opposite)
- Values close to 0:    No linear correlation
""")
```

**Output:**
```
Analyzing correlations between 3 symphonies
Date range: 2025-02-16 to 2026-02-16

Running backtest for VPVpD1SoqR5ykVu4NdWS...
  -> 249 days of data
  -> Avg daily change: +0.29%
Running backtest for rK0k16GLnmhNHuTYu2gz...
  -> 249 days of data
  -> Avg daily change: +0.21%
Running backtest for Y1g7n9BO3dsGknQlefo9...
  -> 249 days of data
  -> Avg daily change: +0.07%

==================================================
PEARSON CORRELATION MATRIX
==================================================

Symphony        VPVpD1So    rK0k16GL    Y1g7n9BO
------------------------------------------------
VPVpD1So          1.0000      0.9158      0.8180
rK0k16GL          0.9158      1.0000      0.9209
Y1g7n9BO          0.8180      0.9209      1.0000

==================================================
INTERPRETATION
==================================================

- Values close to 1.0:  Strong positive correlation (move together)
- Values close to -1.0: Strong negative correlation (move opposite)
- Values close to 0:    No linear correlation
```
