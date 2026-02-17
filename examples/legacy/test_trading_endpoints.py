"""Example file to test trading API endpoints."""

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
    print("Testing Trading API Endpoints")
    print("=" * 60)

    # Test 1: Get market hours
    print("\n1. Get Market Hours:")
    print("-" * 40)
    try:
        market_hours = client.deploy.get_market_hours()
        print(f"   Number of days: {len(market_hours.market_hours)}")
        for day in market_hours.market_hours[:3]:
            print(f"   - {day.nyse_market_date}: open={day.is_market_open}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 2: Get trading period
    print("\n2. Get Trading Period:")
    print("-" * 40)
    try:
        trading_period = client.trading.get_trading_period()
        print(f"   CRYPTO trading_day: {trading_period.CRYPTO.trading_day}")
        print(f"   EQUITIES trading_day: {trading_period.EQUITIES.trading_day}")
        print(f"   OPTIONS trading_day: {trading_period.OPTIONS.trading_day}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 3: Create dry run (using new dry_run resource)
    print("\n3. Create Dry Run:")
    print("-" * 40)
    try:
        dry_run_results = client.dry_run.create_dry_run(send_segment_event=False)
        print(f"   Number of accounts processed: {len(dry_run_results)}")
        if dry_run_results:
            print(f"   First account: {dry_run_results[0].account_name}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 4: Get accounts first (needed for trade preview)
    print("\n4. Get Accounts:")
    print("-" * 40)
    account_id = None
    try:
        accounts = client.accounts.list()
        print(f"   Number of accounts: {len(accounts.accounts)}")
        if accounts.accounts:
            account_id = accounts.accounts[0].account_uuid
            print(f"   Using account_id: {account_id}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 5: Create trade preview for a symphony
    print("\n5. Create Trade Preview:")
    print("-" * 40)
    symphony_id = "SvfHiUshxXcHUfoCyvn5"  # Replace with your symphony ID
    try:
        if account_id:
            preview = client.dry_run.create_trade_preview(
                symphony_id, broker_account_uuid=account_id
            )
            print(f"   Symphony name: {preview.symphony_name}")
            print(f"   Rebalanced: {preview.rebalanced}")
            print(f"   Recommended trades: {len(preview.recommended_trades)}")
        else:
            print("   Skipped: No account_id available")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 6: Get deploy symphonies
    print("\n6. Get Deploy Symphonies:")
    print("-" * 40)
    try:
        if account_id:
            symphonies = client.deploy.get_deploy_symphonies(account_id)
            print(f"   Number of symphonies: {len(symphonies.symphonies)}")
        else:
            print("   Skipped: No account_id available")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 7: Get deploys
    print("\n7. Get Deploys:")
    print("-" * 40)
    try:
        if account_id:
            deploys = client.deploy.get_deploys(account_id)
            print(f"   Number of deploys: {len(deploys.deploys)}")
            if deploys.deploys:
                deploy_id = deploys.deploys[0].deploy_id
                print(f"   First deploy status: {deploys.deploys[0].status}")

                # Test 8: Get single deploy
                print("\n8. Get Single Deploy:")
                print("-" * 40)
                try:
                    deploy = client.deploy.get_deploy(account_id, deploy_id)
                    print(f"   Deploy ID: {deploy.deploy_id}")
                    print(f"   Status: {deploy.status}")
                except Exception as e:
                    print(f"   Error: {e}")
        else:
            print("   Skipped: No account_id available")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 9: Get order requests
    print("\n9. Get Order Requests:")
    print("-" * 40)
    try:
        if account_id:
            order_requests = client.trading.get_order_requests(account_id)
            print(f"   Number of order requests: {len(order_requests.order_requests)}")
            if order_requests.order_requests:
                order_request_id = order_requests.order_requests[0].order_request_id
                print(f"   First order status: {order_requests.order_requests[0].status}")

                # Test 10: Get single order request
                print("\n10. Get Single Order Request:")
                print("-" * 40)
                try:
                    order_request = client.trading.get_order_request(account_id, order_request_id)
                    print(f"   Order ID: {order_request.order_request_id}")
                    print(f"   Symbol: {order_request.symbol}")
                    print(f"   Status: {order_request.status}")
                except Exception as e:
                    print(f"   Error: {e}")
        else:
            print("   Skipped: No account_id available")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
