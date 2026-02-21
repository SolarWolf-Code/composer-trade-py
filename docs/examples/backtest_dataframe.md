# Backtest: Convert to Pandas DataFrame and Get Percent Change

```python
"""
Convert backtest results to a Pandas DataFrame and calculate daily percent change.
"""

from composer import ComposerClient
import os
from dotenv import load_dotenv

load_dotenv()

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

result = client.public_symphony.backtest_symphony_v2(
    symphony_id="KjmxaN1TUNef1cuzFRzq",
    benchmark_tickers=["QQQ", "TQQQ", "SPY"],
    benchmark_symphonies=["AbyvpflKdp1GLQA7GeIj"],
)

# Convert dvm_capital to DataFrame
df = result.dvm_capital.df

# Calculate daily percent change
pct_change = df.pct_change().dropna()

print(pct_change)
```

**Output:**
```
QQQ  AbyvpflKdp1GLQA7GeIj      TQQQ       SPY  VPVpD1SoqR5ykVu4NdWS
date                                                                                
2021-11-03  0.010610              0.000057  0.031867  0.006110              0.031507
2021-11-04  0.012823              0.003711  0.037264  0.004703              0.021189
2021-11-05  0.000954              0.006988  0.003691  0.003476              0.054217
2021-11-08 -0.001365              0.002308 -0.004168  0.000860              0.001270
2021-11-09 -0.006888              0.007521 -0.020433 -0.003303              0.026399
...              ...                   ...       ...       ...                   ...
2026-02-13  0.002114              0.030654  0.004351  0.000705              0.004351
2026-02-17 -0.001030             -0.025952 -0.002476  0.001613             -0.002476
2026-02-18  0.007484              0.007386  0.021510  0.005038              0.021510
2026-02-19 -0.003830              0.007775 -0.011338 -0.002637             -0.011338
2026-02-20  0.008832              0.008523  0.025189  0.007232              0.025189

[1078 rows x 5 columns]
```
