"""
Example: Direct trading - placing orders.

This example demonstrates:
1. List existing orders
2. Create a new BUY order
3. List orders again to see the new order
"""

import os
from dotenv import load_dotenv

from composer import ComposerClient
from composer.models.trading import (
    CreateOrderRequest,
    OrderType,
    TimeInForce,
)

load_dotenv()


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    print("=" * 60)
    print("1. GET ACCOUNT")
    print("=" * 60)

    accounts = client.accounts.list()
    if not accounts:
        print("No accounts found. Please create an account first.")
        return

    account = accounts[0]
    account_id = account.account_uuid
    print(f"Using account: {account_id} ({account.broker})")
    print(
        f"Direct tradable asset classes: {[a.value for a in account.direct_tradable_asset_classes.buy]}"
    )
    print()

    print("=" * 60)
    print("2. LIST EXISTING ORDERS")
    print("=" * 60)

    try:
        orders = client.trading.list_orders(account_id)
        print(f"Found {len(orders)} orders:\n")
        for i, order in enumerate(orders[:5]):  # Show first 5
            side_str = order.side.value if order.side else "N/A"
            type_str = order.type.value if order.type else "N/A"
            status_str = order.status.value if order.status else "N/A"
            print(f"  {i + 1}. {order.symbol or 'N/A'} ({side_str} {type_str})")
            print(f"     Status: {status_str}")
            print(f"     Order ID: {order.order_request_id}")
            if order.notional:
                print(f"     Notional: ${order.notional:,.2f}")
            if order.quantity:
                print(f"     Quantity: {order.quantity}")
            print()
    except Exception as e:
        print(f"  Error listing orders: {e}\n")

    print("=" * 60)
    print("3. CREATE NEW ORDER")
    print("=" * 60)
    print("Creating a MARKET order to buy $1000 of AAPL...\n")

    try:
        order_request = CreateOrderRequest(
            type=OrderType.MARKET,
            symbol="AAPL",
            time_in_force=TimeInForce.DAY,
            notional=1000.0,
        )

        new_order = client.trading.create_order(account_id, order_request)
        print(f"  Created order!")
        print(f"  Order ID: {new_order.order_request_id}")
        print(f"  Order Time: {new_order.order_time}")
        if new_order.commission is not None:
            print(f"  Commission: ${new_order.commission}")
        print()
    except Exception as e:
        print(f"  Error creating order: {e}\n")

    print("=" * 60)
    print("4. LIST ORDERS AGAIN")
    print("=" * 60)

    try:
        orders = client.trading.list_orders(account_id)
        print(f"Found {len(orders)} orders:\n")
        for i, order in enumerate(orders[:5]):
            side_str = order.side.value if order.side else "N/A"
            type_str = order.type.value if order.type else "N/A"
            status_str = order.status.value if order.status else "N/A"
            print(f"  {i + 1}. {order.symbol or 'N/A'} ({side_str} {type_str})")
            print(f"     Status: {status_str}")
            print(f"     Order ID: {order.order_request_id}")
            if order.notional:
                print(f"     Notional: ${order.notional:,.2f}")
            print()
    except Exception as e:
        print(f"  Error listing orders: {e}\n")

    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print("Trading operations completed.")


if __name__ == "__main__":
    main()
