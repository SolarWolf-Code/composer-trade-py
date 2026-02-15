"""
Example: List accounts and get holdings.

This example shows how to retrieve all brokerage accounts associated with
the authenticated user and view their current holdings.
"""

from composer import ComposerClient
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    client = ComposerClient(api_key=os.getenv("COMPOSER_API_KEY"), api_secret=os.getenv("COMPOSER_API_SECRET"))

    print("Fetching accounts...")
    accounts = client.accounts.list()

    print(f"\nFound {len(accounts)} accounts:\n")
    for account in accounts:
        print(f"  Account UUID: {account.account_uuid}")
        print(f"  Type: {account.account_type}")
        print(f"  Broker: {account.broker}")
        print(f"  Status: {account.status}")
        print(f"  Asset Classes: {[a.value for a in account.asset_classes]}")
        print(
            f"  Direct Tradable: buy={[a.value for a in account.direct_tradable_asset_classes.buy]}, sell={[a.value for a in account.direct_tradable_asset_classes.sell]}"
        )
        print(
            f"  Symphony Tradable: {[a.value for a in account.symphony_tradable_asset_classes]}"
        )
        print(f"  Created At: {account.created_at}")
        print(f"  Has Active Position: {account.has_active_position}")
        print()

        print(f"Fetching holdings for {account.account_uuid}...")
        holdings = client.accounts.get_holdings(account.account_uuid)

        if holdings:
            print(f"\n  Holdings ({len(holdings)} positions):\n")
            for holding in holdings:
                print(f"    {holding.ticker}")
                print(f"      Quantity: {holding.quantity}")
                print(f"      Asset Class: {holding.asset_class.value}")
                if holding.options_details:
                    print(f"      Options Details:")
                    print(
                        f"        Underlying: {holding.options_details.underlying_asset_symbol}"
                    )
                    print(f"        Strike: ${holding.options_details.strike_price}")
                    print(f"        Expiry: {holding.options_details.expiry}")
                    print(f"        Type: {holding.options_details.contract_type}")
                print()
        else:
            print("  No holdings found.\n")


if __name__ == "__main__":
    main()
