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

```python
from composer import ComposerClient
from composer.models.trading import CreateOrderRequest, OrderType, TimeInForce

# Initialize client
client = ComposerClient(
    api_key="your-api-key",
    api_secret="your-api-secret"
)

# List your accounts
accounts = client.accounts.list()
account_id = accounts[0].account_uuid

# Place a direct trade
order = client.trading.create_order(
    account_id=account_id,
    request=CreateOrderRequest(
        type=OrderType.MARKET,
        symbol="AAPL",
        time_in_force=TimeInForce.DAY,
        notional=1000.0
    )
)
print(f"Created order: {order.order_request_id}")
```

## Building a Symphony

Create automated trading strategies programmatically:

```python
from composer.models.common.symphony import Root, Asset, WeightCashEqual
from composer.models.symphony import CreateSymphonyRequest, AssetClass

# Build a simple strategy
symphony = Root(
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
request = CreateSymphonyRequest(
    name="Buy and Hold AAPL",
    asset_class=AssetClass.EQUITIES,
    color="#FF6B6B",
    hashtag="#AAPL",
    symphony=symphony
)

result = client.symphony.create_symphony(request)
print(f"Created symphony: {result.symphony_id}")
```

## Backtesting

Test your strategies before deploying:

```python
from composer.models.backtest import BacktestRequest, SymphonyDefinition

result = client.backtest.run(
    BacktestRequest(
        capital=10000.0,
        start_date="2020-01-01",
        end_date="2024-01-01",
        benchmark_tickers=["SPY"],
        symphony=SymphonyDefinition(raw_value=symphony)
    )
)

print(f"Sharpe Ratio: {result.stats.sharpe_ratio}")
print(f"Cumulative Return: {result.stats.cumulative_return}")
```

## Documentation

For complete documentation, visit the [Composer API Docs](https://api.composer.trade/docs/index.html).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
