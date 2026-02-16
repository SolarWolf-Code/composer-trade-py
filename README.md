# Composer Trade Python SDK

<p align="center">
  <img src="composer-trade-py.png" alt="Composer Trade Python SDK" width="200">
</p>

A Python SDK for the [Composer](https://www.composer.trade/) trading platform API. Build, backtest, and deploy automated trading strategies programmatically.

## Features

- **Complete API Coverage**: All endpoints from the Composer API
- **Type-Safe Models**: Full Pydantic models for all requests and responses
- **Programmatic Symphony Building**: Build trading strategies using Python code
- **Backtesting**: Test strategies before deploying
- **Portfolio Management**: View holdings, stats, and history
- **Direct Trading**: Place orders directly
- **Market Data**: Access options chains and contract data

## Installation

```bash
pip install composer-trade-py
```

## Quick Start
## Building a Symphony

Create automated trading strategies programmatically:

```python
from composer.models.common.symphony import Asset, WeightCashEqual
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Build a simple strategy
symphony = SymphonyDefinition(
    name="Buy and Hold AAPL",
    description="Simple buy and hold strategy",
    rebalance="daily",
    children=[
        WeightCashEqual(
            children=[Asset(ticker="AAPL", name="Apple Inc")]
        )
    ]
)

# Create it in your account
result = client.user_symphony.create_symphony(
    name="Buy and Hold AAPL",
    color="#FF6B6B",
    hashtag="#AAPL",
    symphony=symphony
)
print(f"Created symphony: {result.symphony_id}")
```

## Backtesting

Test your strategies before deploying:

```python
from composer.models.backtest import BacktestParams
from composer.models.common import SymphonyDefinition

# Run a backtest
result = client.user_symphony.backtest_symphony(
    symphony_id="your-symphony-id",
    params=BacktestParams(
        capital=10000.0,
        start_date="2020-01-01",
        end_date="2024-01-01",
        benchmark_tickers=["SPY"]
    )
)

print(f"Sharpe Ratio: {result.stats.sharpe_ratio}")
print(f"Cumulative Return: {result.stats.cumulative_return}")
```

Or run a backtest with a custom symphony definition:

```python
from composer.models.backtest import BacktestParams
from composer.models.common import SymphonyDefinition

result = client.backtest.run(
    BacktestParams(
        capital=10000.0,
        start_date="2020-01-01",
        end_date="2024-01-01",
        benchmark_tickers=["SPY"],
        symphony=symphony
    )
)

print(f"Sharpe Ratio: {result.stats.sharpe_ratio}")
print(f"Cumulative Return: {result.stats.cumulative_return}")
```

## Documentation

For complete documentation, visit the Composer API Docs:

- [Trading API](https://trading-api.composer.trade/api/v1/api-docs/index.html#/)
- [Backtest API](https://backtest-api.composer.trade/api/v1/api-docs/index.html#/)
- [Stagehand API](https://stagehand-api.composer.trade/api/v1/api-docs/index.html)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
