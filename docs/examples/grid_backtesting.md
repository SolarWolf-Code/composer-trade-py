# Grid Backtesting

```py
"""
Perform a grid search backtest on different RSI levels
"""

from composer.models.common.symphony import *
from composer import ComposerClient
from dotenv import load_dotenv
import os

load_dotenv()

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

for rsi_length in [10, 14, 20]:
    safe_sectors_or_bonds = Group(
        id="94d631c5-c86b-4af4-84dd-fa3eec2e8d9a",
        step="group",
        name="Safe Sectors or Bonds",
        children=[
            WeightCashEqual(
                id="cd6ceaf4-d770-45a6-b96d-0c5a22ffb8dd",
                step="wt-cash-equal",
                children=[
                    Filter(
                        id="6b59cb0a-b18a-43e0-8a40-ce474406cb67",
                        step="filter",
                        select_fn="bottom",
                        select_n=1,
                        sort_by_fn=Function.RELATIVE_STRENGTH_INDEX,
                        sort_by_fn_params={
                            "window": rsi_length,
                        },
                        children=[
                            Asset(
                                id="9db712c9-144d-4b22-89c6-3d574f02b02b",
                                step="asset",
                                ticker="BSV",
                            ),
                            Asset(
                                id="39809167-6ed7-4e3a-b55b-a4aa313e26f3",
                                step="asset",
                                ticker="TLT",
                            ),
                            Asset(
                                id="edaf56af-7df4-4267-9a53-20176f162be6",
                                step="asset",
                                ticker="LQD",
                            ),
                            Asset(
                                id="aed9c537-6790-4cf9-98fb-fad60b169671",
                                step="asset",
                                ticker="VBF",
                            ),
                            Asset(
                                id="5c0b9dc9-290e-4d7f-bf85-ba5d175d1094",
                                step="asset",
                                ticker="XLP",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    symphony = SymphonyDefinition(
        name="Safe Sectors Different RSI Levels",
        rebalance="daily",
        children=[WeightCashEqual(children=[safe_sectors_or_bonds])],
    )

    backtest = client.backtest.run_v2(symphony=symphony)
    print(f"{backtest.stats.annualized_rate_of_return * 100:.2f}% CAGR using RSI({rsi_length})")
```

**Output:**
```
25.53% CAGR using RSI(10)
24.07% CAGR using RSI(14)
20.99% CAGR using RSI(20)
```