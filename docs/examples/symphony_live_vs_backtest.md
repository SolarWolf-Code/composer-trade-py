# Compare live vs backtest returns for a symphony

```python
"""
Compare live vs backtest returns for a symphony
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

all_accounts = client.accounts.list()
first_account = all_accounts.accounts[0]

all_symphonies = client.portfolio.get_symphony_stats_meta(first_account.account_uuid)
first_symphony = all_symphonies.symphonies[0]

# Get live returns
live_returns = client.portfolio.get_symphony_value_history(
    first_account.account_uuid, first_symphony.id
)

# Get the date range from live returns
live_dates_list = sorted(live_returns.dates.keys())
start_date = live_dates_list[0]
end_date = live_dates_list[-1]

# Get initial capital from first live return
initial_capital = live_returns.dates[live_dates_list[0]].series

# Get backtest returns with matching date range and capital
backtest_returns = client.user_symphony.backtest_symphony_v2(
    first_symphony.id,
    start_date=start_date,
    end_date=end_date,
    capital=initial_capital,
)

# Find the symphony ID in the backtest dvm_capital
symphony_id = first_symphony.id

# Build comparable backtest series (using deposit_adjusted_series equivalent)
backtest_series = {}
if backtest_returns.dvm_capital:
    for date, series_dict in backtest_returns.dvm_capital.items():
        if symphony_id in series_dict:
            backtest_series[date] = series_dict[symphony_id]

# Find overlapping dates
live_dates = set(live_returns.dates.keys())
backtest_dates = set(backtest_series.keys())
overlapping_dates = sorted(live_dates & backtest_dates)

print(f"Live returns: {len(live_returns.dates)} days ({min(live_dates)} to {max(live_dates)})")
print(
    f"Backtest returns: {len(backtest_series)} days ({min(backtest_dates)} to {max(backtest_dates)})"
)
print(f"Overlapping dates: {len(overlapping_dates)}")

# Compare overlapping dates
if overlapping_dates:
    print("\n--- Deviation Analysis ---")

    deviations = []
    for date in overlapping_dates:
        live_value = live_returns.dates[date].deposit_adjusted_series
        backtest_value = backtest_series[date]

        if backtest_value > 0:
            deviation_pct = ((live_value - backtest_value) / backtest_value) * 100
        else:
            deviation_pct = 0

        deviations.append(
            {
                "date": date,
                "live": live_value,
                "backtest": backtest_value,
                "deviation_pct": deviation_pct,
            }
        )

    # Summary statistics
    avg_deviation = sum(d["deviation_pct"] for d in deviations) / len(deviations)
    max_deviation = max(deviations, key=lambda x: abs(x["deviation_pct"]))

    # Cumulative difference (% change from first to last)
    first_live = deviations[0]["live"]
    last_live = deviations[-1]["live"]
    first_backtest = deviations[0]["backtest"]
    last_backtest = deviations[-1]["backtest"]

    live_pct_change = ((last_live - first_live) / first_live) * 100
    backtest_pct_change = ((last_backtest - first_backtest) / first_backtest) * 100
    cumulative_diff_pct = live_pct_change - backtest_pct_change

    print(f"Average deviation: {avg_deviation:.2f}%")
    print(f"Live % change: {live_pct_change:+.2f}% (${first_live:,.2f} -> ${last_live:,.2f})")
    print(
        f"Backtest % change: {backtest_pct_change:+.2f}% (${first_backtest:,.2f} -> ${last_backtest:,.2f})"
    )
    print(f"Cumulative difference: {cumulative_diff_pct:+.2f}%")
    print(f"Max deviation: {max_deviation['deviation_pct']:.2f}% on {max_deviation['date']}")
    print(f"  Live: ${max_deviation['live']:,.2f}, Backtest: ${max_deviation['backtest']:,.2f}")

    # Show first few comparisons
    print("\nFirst 5 comparisons:")
    for d in deviations[:5]:
        print(
            f"  {d['date']}: Live=${d['live']:,.2f}, Backtest=${d['backtest']:,.2f}, Deviation={d['deviation_pct']:+.2f}%"
        )
else:
    print("\nNo overlapping dates found.")
    print("Live returns may be from a different period than backtest.")
```

**Output:**
```
Live returns: 5 days (2026-02-09 to 2026-02-13)
Backtest returns: 5 days (2026-02-09 to 2026-02-13)
Overlapping dates: 5

--- Deviation Analysis ---
Average deviation: 0.11%
Live % change: -6.76% ($12,990.00 -> $12,111.55)
Backtest % change: -6.32% ($12,926.46 -> $12,109.49)
Cumulative difference: -0.44%
Max deviation: 0.49% on 2026-02-09
  Live: $12,990.00, Backtest: $12,926.46

First 5 comparisons:
  2026-02-09: Live=$12,990.00, Backtest=$12,926.46, Deviation=+0.49%
  2026-02-10: Live=$12,748.05, Backtest=$12,746.57, Deviation=+0.01%
  2026-02-11: Live=$12,842.90, Backtest=$12,841.51, Deviation=+0.01%
  2026-02-12: Live=$12,059.14, Backtest=$12,057.03, Deviation=+0.02%
  2026-02-13: Live=$12,111.55, Backtest=$12,109.49, Deviation=+0.02%
```
