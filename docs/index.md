# Composer Trade SDK

<p align="center">
  <img src="images/composer-trade-py.svg" alt="Composer Trade" width="200">
</p>

Unofficial Python SDK for [Composer.trade](https://composer.trade) API.

## Installation

```bash
pip install composer-trade-py
```

## Quick Start

```python
from composer import ComposerClient

client = ComposerClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# List portfolios
portfolios = client.portfolio.list()

# Get account info
account = client.accounts.get()
```

## Features

- **Portfolio Management** - View and manage your portfolios
- **Backtesting** - Test trading strategies against historical data
- **Market Data** - Access real-time and historical market data
- **Trading** - Deploy and manage trading strategies
- **AI Agents** - Interact with AI-powered trading agents

## API Reference

See [API Reference](api/reference.md) for full documentation.
