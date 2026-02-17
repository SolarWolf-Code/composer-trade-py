"""
Example: Create and backtest a symphony programmatically.

This example shows how to build a trading strategy from scratch using
the symphony node types, then backtest it.
"""

from composer import ComposerClient, BacktestRequest
from composer.models.common.symphony import (
    Asset,
    If,
    IfChildTrue,
    IfChildFalse,
    WeightCashEqual,
    Function,
    RebalanceFrequency,
)
from composer.models.backtest import SymphonyDefinition
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Build a simple symphony: "Buy TQQQ if price > 200-day MA, else buy UVXY"
symphony = SymphonyDefinition(
    name="Trend Following",
    description="Buy leveraged QQQ on uptrend, VIX on downtrend",
    rebalance=RebalanceFrequency.DAILY,
    children=[
        WeightCashEqual(
            children=[
                If(
                    children=[
                        # True condition: TQQQ price > 200-day MA
                        IfChildTrue(
                            comparator="gt",
                            lhs_fn=Function.CURRENT_PRICE,
                            lhs_val="TQQQ",
                            rhs_val="TQQQ",
                            rhs_fixed_value=False,
                            rhs_fn=Function.MOVING_AVERAGE_PRICE,
                            rhs_window_days=200,
                            children=[Asset(ticker="TQQQ", name="ProShares UltraPro QQQ")],
                        ),
                        # False condition: Buy UVXY (volatility)
                        IfChildFalse(
                            children=[Asset(ticker="UVXY", name="ProShares Ultra VIX Short-Term")]
                        ),
                    ]
                )
            ]
        )
    ],
)

# Backtest the symphony
print("\nRunning backtest...")
result = client.backtest.run_v2(
    BacktestRequest(
        capital=10000.0,
        start_date="2020-01-01",
        end_date="2024-01-01",
        benchmark_tickers=["QQQ", "SPY"],
        symphony=SymphonyDefinition(raw_value=symphony),
    )
)

# Display results
print(f"\nBacktest Results:")
print(f"  Sharpe Ratio: {result.stats.sharpe_ratio:.2f}")
print(f"  Cumulative Return: {result.stats.cumulative_return:.2%}")
print(f"  Max Drawdown: {result.stats.max_drawdown:.2%}")
print(f"  Final Value: ${result.last_market_days_value:,.2f}")
