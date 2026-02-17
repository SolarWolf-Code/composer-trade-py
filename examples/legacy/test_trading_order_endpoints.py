"""Example file to test trading endpoints."""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: COMPOSER_API_KEY and COMPOSER_API_SECRET must be set")
        return

    client = ComposerClient(api_key, api_secret)

    print("=" * 60)
    print("Testing Trading Endpoints")
    print("=" * 60)

    # Get accounts
    print("\n1. Get Accounts:")
    print("-" * 40)
    try:
        accounts = client.accounts.list()
        print(f"   Number of accounts: {len(accounts.accounts)}")
        if not accounts.accounts:
            print("   No accounts found!")
            return
        account_id = accounts.accounts[0].account_uuid
        print(f"   Using account_id: {account_id}")
    except Exception as e:
        print(f"   Error: {e}")
        return

    # Test: Create order request (equity)
    print("\n2. Create Order Request (Equity):")
    print("-" * 40)
    equity_order_id = None
    try:
        result = client.trading.create_order_request(
            account_id=account_id,
            type="MARKET",
            symbol="AAPL",
            time_in_force="DAY",
            quantity=1.0,
        )
        print(f"   Order ID: {result.order_request_id}")
        print(f"   Order time: {result.order_time}")
        equity_order_id = result.order_request_id
    except Exception as e:
        print(f"   Error: {e}")

    # Test: Get order requests
    print("\n3. Get Order Requests:")
    print("-" * 40)
    try:
        orders = client.trading.get_order_requests(account_id, limit=5)
        print(f"   Number of orders: {len(orders.order_requests)}")
        for o in orders.order_requests[:3]:
            print(f"   - {o.symbol}: {o.status}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test: Cancel equity order request
    if equity_order_id:
        print("\n4. Cancel Equity Order:")
        print("-" * 40)
        try:
            client.trading.delete_order_request(account_id, equity_order_id)
            print(f"   Order {equity_order_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    # Test: Create order request (options) - need a real options symbol
    print("\n5. Create Order Request (Options):")
    print("-" * 40)
    options_order_id = None
    try:
        # Options require a specific symbol format like: OPTIONS::AAPL1234567890PC20240119//USD
        # Your account only has TQQQ, no options positions
        print(
            "   Skipped: Need a real options symbol (e.g., OPTIONS::AAPL1234567890PC20240119//USD)"
        )
    except Exception as e:
        print(f"   Error: {e}")

    # Test: Modify options order (if we have one)
    if options_order_id:
        print("\n6. Modify Options Order:")
        print("-" * 40)
        try:
            client.trading.modify_order_request(
                account_id,
                options_order_id,
                limit_price=150.0,
            )
            print(f"   Order {options_order_id} modified successfully")
        except Exception as e:
            print(f"   Error: {e}")

    # Test: Cancel options order
    if options_order_id:
        print("\n7. Cancel Options Order:")
        print("-" * 40)
        try:
            client.trading.delete_order_request(account_id, options_order_id)
            print(f"   Order {options_order_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
