"""
Direct Trading - Place a market order for a single stock.
"""

from composer import ComposerClient
from dotenv import load_dotenv
import os

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

print(f"\nPlacing order for {symbol}...")

# Place the order (uncomment to execute)
order = client.trading.create_order_request(
    account_id=account.account_uuid,
    type="MARKET",
    symbol=symbol,
    time_in_force="DAY",
    notional=notional_value,
)

print(f"  Order ID: {order.order_request_id}")
