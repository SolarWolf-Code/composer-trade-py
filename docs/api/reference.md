# API Reference

Welcome to the Composer Trade SDK API reference. This section provides detailed documentation for all resources and methods available in the SDK.

## Getting Started

First, instantiate the `ComposerClient` with your API credentials:

```python
from composer import ComposerClient

client = ComposerClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)
```

## Available Resources

| Category | Description |
|----------|-------------|
| [Client](client.md) | Main ComposerClient initialization |
| [Portfolio](portfolio.md) | Portfolio, Accounts, Cash, User management |
| [Backtest & Symphonies](backtest.md) | Backtesting, Symphony management, Search, Watchlists |
| [Trading](trading.md) | Trading, Deploy, Dry Run operations |
| [Market Data](market-data.md) | Market data and quotes |
| [Advanced](advanced.md) | AI Agents, Conversations, Reports, Auth |

## Models

The SDK includes numerous Pydantic models for request/response handling. See the [Models Reference](models.md) for detailed information on all available data models.
