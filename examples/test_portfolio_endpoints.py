"""
Example: Testing Portfolio endpoints.

This demonstrates all portfolio endpoints:
- get_account_holdings
- get_total_stats
- get_symphony_stats
- get_symphony_stats_meta
- get_portfolio_history
- get_symphony_value_history
- get_symphony_holdings
- get_holdings_by_position
- get_activity_history
- get_deploy_details
- get_holding_stats

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    # Optionally set specific account/symphony IDs
    export COMPOSER_ACCOUNT_ID="account-uuid"
    export COMPOSER_SYMPHONY_ID="symphony-uuid"
    export COMPOSER_POSITION_ID="position-uuid"

    python examples/test_portfolio_endpoints.py
"""

import os
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
    symphony_id = os.environ.get("COMPOSER_SYMPHONY_ID")
    position_id = os.environ.get("COMPOSER_POSITION_ID")

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

    # Try to get symphony_id from symphony_stats if not provided
    if not symphony_id:
        print("\n2. Fetching symphony stats to get symphony_id...")
        try:
            stats = client.portfolio.get_symphony_stats(account_id)
            symphony_ids = list(stats.stats.keys())
            if symphony_ids:
                symphony_id = symphony_ids[0]
                print(f"   Using first symphony: {symphony_id}")
                # Get position_id from the stats dict
                position_id = stats.stats[symphony_ids[0]].get("position_id")
                if position_id:
                    print(f"   Got position_id: {position_id}")
            else:
                print("   No symphonies found for this account")
        except Exception as e:
            print(f"   ERROR: {e}")

    # Try to get position_id from symphony_stats if not provided
    if not position_id and symphony_id:
        try:
            stats = client.portfolio.get_symphony_stats(account_id)
            if symphony_id in stats.stats:
                position_id = stats.stats[symphony_id].get("position_id")
                if position_id:
                    print(f"   Got position_id: {position_id}")
        except Exception as e:
            print(f"   Could not get position_id: {e}")

    print("\n" + "=" * 60)
    print("PORTFOLIO ENDPOINTS")
    print("=" * 60)

    # Test 1: get_account_holdings
    print("\n1. get_account_holdings")
    try:
        holdings = client.portfolio.get_account_holdings(account_id)
        print(f"   SUCCESS: Found {len(holdings)} holdings")
        for h in holdings[:3]:
            print(f"   - {h.ticker}: {h.quantity} shares")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get_total_stats
    print("\n2. get_total_stats")
    try:
        stats = client.portfolio.get_total_stats(account_id)
        print(f"   SUCCESS: Portfolio value: ${stats.portfolio_value:,.2f}")
        print(
            f"   - Today's change: ${stats.todays_dollar_change:,.2f} ({stats.todays_percent_change:.2f}%)"
        )
        print(f"   - Total cash: ${stats.total_cash:,.2f}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_symphony_stats
    print("\n3. get_symphony_stats")
    try:
        stats = client.portfolio.get_symphony_stats(account_id)
        print(f"   SUCCESS: Got stats for {len(stats.stats)} symphonies")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 4: get_symphony_stats_meta
    print("\n4. get_symphony_stats_meta")
    try:
        stats = client.portfolio.get_symphony_stats_meta(account_id)
        print(f"   SUCCESS: Got stats for {len(stats.symphonies)} symphonies")
        for s in stats.symphonies[:3]:
            print(f"   - {s.name}: ${s.value:,.2f}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 5: get_portfolio_history
    print("\n5. get_portfolio_history")
    try:
        history = client.portfolio.get_portfolio_history(account_id)
        print(f"   SUCCESS: Got {len(history.epoch_ms)} data points")
        if history.series:
            print(f"   - Latest value: ${history.series[-1]:,.2f}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 6: get_symphony_value_history
    if symphony_id:
        print("\n6. get_symphony_value_history")
        try:
            history = client.portfolio.get_symphony_value_history(account_id, symphony_id)
            print(f"   SUCCESS: Got {len(history.epoch_ms)} data points")
            if history.series:
                print(f"   - Latest value: ${history.series[-1]:,.2f}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n6. get_symphony_value_history - SKIPPED (no symphony_id)")

    # Test 7: get_symphony_holdings
    if symphony_id:
        print("\n7. get_symphony_holdings")
        try:
            holdings = client.portfolio.get_symphony_holdings(account_id, symphony_id)
            print(f"   SUCCESS: Symphony ID: {holdings.symphony_id}")
            print(f"   - Cash: ${holdings.cash:,.2f}")
            print(f"   - Net deposits: ${holdings.net_deposits:,.2f}")
            print(f"   - Liquidated: {holdings.liquidated}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n7. get_symphony_holdings - SKIPPED (no symphony_id)")

    # Test 8: get_holdings_by_position
    if position_id:
        print("\n8. get_holdings_by_position")
        try:
            holdings = client.portfolio.get_holdings_by_position(position_id)
            print(f"   SUCCESS: Symphony ID: {holdings.symphony_id}")
            print(f"   - Cash: ${holdings.cash:,.2f}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n8. get_holdings_by_position - SKIPPED (no position_id)")

    # Test 9: get_activity_history
    if symphony_id:
        print("\n9. get_activity_history")
        try:
            activity = client.portfolio.get_activity_history(
                account_id, symphony_id, limit=10, offset=0
            )
            print(f"   SUCCESS: Got {len(activity.data)} activities")
            for a in activity.data[:3]:
                print(f"   - {a.type}: {a.symphony_name}")
        except Exception as e:
            print(f"   ERROR: {e}")
    else:
        print("\n9. get_activity_history - SKIPPED (no symphony_id)")

    # Test 10: get_deploy_details
    # This requires a specific deploy_id which we can't easily guess
    print("\n10. get_deploy_details")
    print("   SKIPPED (requires specific deploy_id)")

    # Test 11: get_holding_stats
    print("\n11. get_holding_stats")
    try:
        stats = client.portfolio.get_holding_stats(account_id)
        print(f"   SUCCESS: Got stats for {len(stats.holdings)} holdings")
        for h in stats.holdings[:3]:
            print(f"   - {h.symbol}: ${h.notional_value if h.notional_value else 0:,.2f}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test with position_type filter
    print("\n12. get_account_holdings (with position_type='direct')")
    try:
        holdings = client.portfolio.get_account_holdings(account_id, position_type="direct")
        print(f"   SUCCESS: Found {len(holdings)} direct holdings")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
