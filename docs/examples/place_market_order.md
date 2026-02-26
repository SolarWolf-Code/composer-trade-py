# Direct Trading - Place a market order for a single stock.

```python
"""
Direct Trading - Place a market order for a single stock.

This example shows how to place a direct order for a single stock
(like AAPL) without using a symphony.
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

from composer.models.trading import OrderType, TimeInForce

load_dotenv()

client = ComposerClient(
    api_key=os.getenv("COMPOSER_API_KEY"),
    api_secret=os.getenv("COMPOSER_API_SECRET"),
)

# Get account
accounts = client.accounts.list()
account = accounts.accounts[0]

# Get buying power
buying_power = client.accounts.get_buying_power(account.account_uuid)[0]
print(f"Direct Trading Buying Power: ${buying_power.direct_trading_buying_power:,.2f}")

# Define order parameters
symbol = "AAPL"
notional_value = 1000

if notional_value > buying_power.direct_trading_buying_power:
    print("Not enough buying power. Your order will be queued until you add enough cash")

print(f"\nPlacing order for {symbol}...")

# Place the order (uncomment to execute)
order = client.trading.create_order_request(
    account_id=account.account_uuid,
    type=OrderType.MARKET,
    symbol=symbol,
    time_in_force=TimeInForce.DAY,
    notional=notional_value,
)

print(f"  Order ID: {order.order_request_id}")
```

**Output:**
```
Direct Trading Buying Power: $18.10
Not enough buying power. Your order will be queued until you add enough cash

Placing order for AAPL...
  Order ID: 2e59925b-3f81-448f-8404-80c00a5f392f
```
