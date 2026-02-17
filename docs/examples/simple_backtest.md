# Backtest one of your symphonies by providing it's ID

```python
"""
Backtest one of your symphonies by providing it's ID
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

result = client.user_symphony.backtest_symphony(
    symphony_id="P8npOsKAqRoPDoL6sQiE",
    capital=10000.0,
    start_date="2024-01-01",
    end_date="2024-03-01",
    benchmark_tickers=["SPY"],
)

print(f"Stats: {result.stats}")
```

**Output:**
```
Stats: Stats(sharpe=1.79, cumulative=3.42%, drawdown=3.16%, ann_return=22.36%)
```
