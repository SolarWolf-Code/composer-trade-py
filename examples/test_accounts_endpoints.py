"""
Example: Testing Accounts endpoints.

This demonstrates all accounts GET endpoints:
- list
- get_holdings
- get_available_types
- get_supported_regions
- get_activities_trades
- get_activities_trades_volume
- get_activities_trade_history
- get_info
- get_buying_power
- get_investor_documents

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    # Optionally set specific account ID
    export COMPOSER_ACCOUNT_ID="account-uuid"

    python examples/test_accounts_endpoints.py
"""

import os
from datetime import datetime, timedelta, timezone
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: Please set COMPOSER_API_KEY and COMPOSER_API_SECRET")
        return

    client = ComposerClient(api_key=api_key, api_secret=api_secret)

    # Get account ID from env or fetch from accounts list
    account_id = os.environ.get("COMPOSER_ACCOUNT_ID")

    if not account_id:
        print("\n1. Fetching accounts list to get account_id...")
        try:
            accounts_response = client.accounts.list()
            if accounts_response.accounts:
                account_id = accounts_response.accounts[0].account_uuid
                print(f"   Using first account: {account_id}")
            else:
                print("   ERROR: No accounts found")
                return
        except Exception as e:
            print(f"   ERROR: {e}")
            return

    print("\n" + "=" * 60)
    print("ACCOUNTS ENDPOINTS")
    print("=" * 60)

    # Test 1: list
    print("\n1. list")
    try:
        accounts = client.accounts.list()
        print(f"   SUCCESS: Found {len(accounts.accounts)} accounts")
        for acc in accounts.accounts[:3]:
            print(f"   - {acc.account_type}: {acc.broker} ({acc.status})")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get_holdings
    print("\n2. get_holdings")
    try:
        holdings = client.accounts.get_holdings(account_id)
        print(f"   SUCCESS: Found {len(holdings)} holdings")
        for h in holdings[:3]:
            print(f"   - {h.ticker}: {h.quantity} shares ({h.asset_class})")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_available_types
    print("\n3. get_available_types")
    try:
        available = client.accounts.get_available_types()
        print(f"   SUCCESS: Got available account types")
        for region, types in list(available.items())[:3]:
            print(f"   - {region}: {len(types)} types available")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 4: get_supported_regions
    print("\n4. get_supported_regions")
    try:
        regions = client.accounts.get_supported_regions()
        print(f"   SUCCESS: Got supported regions")
        print(f"   - EQUITIES: {len(regions.EQUITIES.countries)} countries")
        print(f"   - CRYPTO: {len(regions.CRYPTO.countries)} countries")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 5: get_activities_trades
    print("\n5. get_activities_trades")
    try:
        trades = client.accounts.get_activities_trades(account_id, limit=10)
        print(f"   SUCCESS: Found {len(trades)} trades")
        for t in trades[:3]:
            print(f"   - {t.symbol}: {t.side} {t.filled_qty} @ ${t.filled_avg_price}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 6: get_activities_trades_volume
    print("\n6. get_activities_trades_volume")
    try:
        start_time = (datetime.now(timezone.utc) - timedelta(days=30)).strftime(
            "%Y-%m-%dT%H:%M:%S-05:00"
        )
        volume = client.accounts.get_activities_trades_volume(account_id, start_time=start_time)
        print(f"   SUCCESS: Volume: {volume.volume}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 7: get_activities_trade_history
    print("\n7. get_activities_trade_history")
    try:
        history = client.accounts.get_activities_trade_history(account_id, limit=10)
        print(f"   SUCCESS: Found {len(history)} history items")
        for h in history[:3]:
            print(f"   - {h.activity_type}: {h.symbol} ({h.status})")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 8: get_info
    print("\n8. get_info")
    try:
        info = client.accounts.get_info(account_id)
        print(f"   SUCCESS: Account info retrieved")
        print(f"   - Type: {info.account_type}")
        print(f"   - Broker: {info.broker}")
        print(f"   - Owner: {info.identity.given_name} {info.identity.family_name}")
        print(f"   - Email: {info.contact.email_address}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 9: get_buying_power
    print("\n9. get_buying_power")
    try:
        buying_power = client.accounts.get_buying_power(account_id)
        print(f"   SUCCESS: Found {len(buying_power)} asset classes")
        for bp in buying_power:
            print(f"   - {bp.asset_class}: ${bp.symphony_buying_power:,.2f} buying power")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 10: get_investor_documents
    print("\n10. get_investor_documents")
    try:
        docs = client.accounts.get_investor_documents(account_id, category="STATEMENT", year=2025)
        print(f"   SUCCESS: Found {len(docs)} documents")
        for d in docs[:3]:
            print(f"   - {d.date}: {d.url}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 11: get_holdings with position_type
    print("\n11. get_holdings (position_type='direct')")
    try:
        holdings = client.accounts.get_holdings(account_id, position_type="direct")
        print(f"   SUCCESS: Found {len(holdings)} direct holdings")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
