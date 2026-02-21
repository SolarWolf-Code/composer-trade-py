# Portfolio Symphony: Convert Time Series to Pandas DataFrame

```python
"""
Convert portfolio time series to a Pandas DataFrame and calculate daily percent change.
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

account_id = client.accounts.list().accounts[0].account_uuid
symphonies = client.portfolio.get_symphony_stats_meta(account_id)
symphony_id = symphonies.symphonies[0].id

res = client.portfolio.get_symphony_value_history(
    account_id=account_id,
    symphony_id=symphony_id
)

print("=== Symphony Value History ===")
print(res.df)
print()

pct_change = res.df["deposit_adjusted_series"].pct_change().dropna()
print("=== Daily Percent Change ===")
print(pct_change.head(10))
```

**Output:**
```
=== Symphony Value History ===
              series  deposit_adjusted_series
date                                         
2026-02-09  12927.76                 12990.00
2026-02-10  12748.05                 12748.05
2026-02-11  12842.90                 12842.90
2026-02-12  12059.14                 12059.14
2026-02-13  12111.55                 12111.55
2026-02-17  12081.60                 12081.60
2026-02-18  13856.63                 12309.85
2026-02-19  13699.68                 12170.42
2026-02-20  14044.41                 12476.67

=== Daily Percent Change ===
date
2026-02-10   -0.018626
2026-02-11    0.007440
2026-02-12   -0.061027
2026-02-13    0.004346
2026-02-17   -0.002473
2026-02-18    0.018892
2026-02-19   -0.011327
2026-02-20    0.025163
Name: deposit_adjusted_series, dtype: float64
```
