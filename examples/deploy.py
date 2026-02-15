"""
Example: Deploy operations - managing symphony investments.

This example demonstrates:
1. Get market hours
2. Invest $1000 into the first symphony
3. Withdraw $100
4. Skip automated rebalancing
5. Sell all assets (go to cash)
6. Rebalance now
7. Sell all assets again (go to cash)
8. Liquidate the symphony
"""

import os
from dotenv import load_dotenv

from composer import ComposerClient

load_dotenv()


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    print("=" * 60)
    print("1. GET MARKET HOURS")
    print("=" * 60)

    try:
        market_hours = client.deploy.get_market_hours()
        print(f"Market hours for the upcoming week:\n")
        for day in market_hours.market_hours[:5]:  # Show first 5 days
            status = "OPEN" if day.is_market_open else "CLOSED"
            print(f"  {day.nyse_market_date}: {status}")
            if day.market_open and day.market_close:
                print(f"    Hours: {day.market_open} - {day.market_close}")
        print()
    except Exception as e:
        print(f"  Error fetching market hours: {e}\n")

    print("=" * 60)
    print("2. GET ACCOUNT AND SYMPHONY")
    print("=" * 60)

    accounts = client.accounts.list()
    if not accounts:
        print("No accounts found. Please create an account first.")
        return

    account = accounts[0]
    account_id = account.account_uuid
    print(f"Using account: {account_id} ({account.broker})")

    symphony_stats = client.portfolio.get_symphony_stats_meta(account_id)
    if not symphony_stats.symphonies:
        print("No symphonies found in this account. Please create a symphony first.")
        return

    symphony = symphony_stats.symphonies[0]
    symphony_id = symphony.id
    print(f"Using symphony: {symphony.name} ({symphony_id})")
    print(f"Current value: ${symphony.value:,.2f}")
    print()

    print("=" * 60)
    print("3. INVEST $1000")
    print("=" * 60)

    try:
        result = client.deploy.invest(account_id, symphony_id, 1000.0)
        print(f"  Invested $1000 into {symphony.name}")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error investing: {e}\n")

    print("=" * 60)
    print("4. WITHDRAW $100")
    print("=" * 60)

    try:
        result = client.deploy.withdraw(account_id, symphony_id, -100.0)
        print(f"  Withdrew $100 from {symphony.name}")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error withdrawing: {e}\n")

    print("=" * 60)
    print("5. SKIP AUTOMATED REBALANCING")
    print("=" * 60)

    try:
        client.deploy.skip_automated_rebalance(account_id, symphony_id, skip=True)
        print(f"  Skipped next automated rebalance for {symphony.name}\n")
    except Exception as e:
        print(f"  Error skipping rebalance: {e}\n")

    print("=" * 60)
    print("6. SELL ALL ASSETS (GO TO CASH)")
    print("=" * 60)

    try:
        result = client.deploy.go_to_cash(account_id, symphony_id)
        print(f"  Moved {symphony.name} to cash")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error going to cash: {e}\n")

    print("=" * 60)
    print("7. REBALANCE NOW")
    print("=" * 60)

    try:
        # Note: rebalance_now typically requires a rebalance_request_uuid from preview
        # This is a simplified example
        result = client.deploy.rebalance(account_id, symphony_id)
        print(f"  Triggered rebalance for {symphony.name}")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error rebalancing: {e}\n")

    print("=" * 60)
    print("8. SELL ALL ASSETS AGAIN (GO TO CASH)")
    print("=" * 60)

    try:
        result = client.deploy.go_to_cash(account_id, symphony_id)
        print(f"  Moved {symphony.name} to cash again")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error going to cash: {e}\n")

    print("=" * 60)
    print("9. LIQUIDATE SYMPHONY")
    print("=" * 60)

    try:
        result = client.deploy.liquidate(account_id, symphony_id)
        print(f"  Liquidated {symphony.name}")
        print(f"  Response: {result}\n")
    except Exception as e:
        print(f"  Error liquidating: {e}\n")

    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print("Deploy operations completed.")


if __name__ == "__main__":
    main()
