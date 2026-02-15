"""
Example: Portfolio statistics and history.

This example shows how to retrieve portfolio statistics, holdings,
symphony performance, and historical portfolio values.
"""

from datetime import datetime
from composer import ComposerClient
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )

    print("Fetching accounts...")
    accounts = client.accounts.list()

    if not accounts:
        print("No accounts found.")
        return

    account = accounts[0]
    account_id = account.account_uuid
    print(f"\nUsing account: {account_id} ({account.broker})\n")

    print("=" * 60)
    print("PORTFOLIO TOTAL STATS")
    print("=" * 60)
    total_stats = client.portfolio.get_total_stats(account_id)
    print(f"  Portfolio Value: ${total_stats.portfolio_value:,.2f}")
    print(f"  Simple Return: {total_stats.simple_return:.2%}")
    print(f"  Time-Weighted Return: {total_stats.time_weighted_return:.2%}")
    print(f"  Net Deposits: ${total_stats.net_deposits:,.2f}")
    print(
        f"  Today's Change: ${total_stats.todays_dollar_change:,.2f} ({total_stats.todays_percent_change:.2%})"
    )
    print(f"  Total Cash: ${total_stats.total_cash:,.2f}")
    print(f"  Unallocated Cash: ${total_stats.total_unallocated_cash:,.2f}")
    print(f"  Pending Deploys Cash: ${total_stats.pending_deploys_cash:,.2f}")
    print()

    print("=" * 60)
    print("HOLDING STATISTICS")
    print("=" * 60)
    holding_stats = client.portfolio.get_holding_stats(account_id)
    print(f"  Total holdings: {len(holding_stats.holdings)}\n")

    for holding in holding_stats.holdings:
        asset_class_str = holding.asset_class.value if holding.asset_class else "N/A"
        print(f"  {holding.symbol} ({asset_class_str})")
        print(f"    Price: ${holding.price:.2f}")
        print(
            f"    Today's Change: ${holding.price_todays_change:.2f} ({holding.price_todays_change_percent:.2%})"
        )
        print(
            f"    Direct Allocation: ${holding.direct.value:,.2f} ({holding.direct.allocation:.2%})"
        )
        print(
            f"    Symphony Allocation: ${holding.symphony.value:,.2f} ({holding.symphony.allocation:.2%})"
        )
        if holding.total_change_percent is not None:
            print(
                f"    Total Return: {holding.total_change_percent:.2%} (${holding.total_change:,.2f})"
            )
        print()

    print("=" * 60)
    print("SYMPHONY STATS METADATA")
    print("=" * 60)
    symphony_stats = client.portfolio.get_symphony_stats_meta(account_id)
    print(f"  Total symphonies: {len(symphony_stats.symphonies)}\n")

    for symphony in symphony_stats.symphonies:
        print(f"  {symphony.name}")
        print(f"    ID: {symphony.id}")
        print(f"    Value: ${symphony.value:,.2f}")
        print(f"    Simple Return: {symphony.simple_return:.2%}")
        print(f"    Time-Weighted Return: {symphony.time_weighted_return:.2%}")
        print(
            f"    Today's Change: ${symphony.last_dollar_change:,.2f} ({symphony.last_percent_change:.2%})"
        )
        print(f"    Cash: ${symphony.cash:,.2f}")
        print(f"    Holdings: {len(symphony.holdings)}")
        for h in symphony.holdings[:3]:
            print(f"      - {h.ticker}: ${h.value:,.2f} ({h.allocation:.2%})")
        if len(symphony.holdings) > 3:
            print(f"      ... and {len(symphony.holdings) - 3} more")
        print()

    print("=" * 60)
    print("PORTFOLIO HISTORY")
    print("=" * 60)
    history = client.portfolio.get_portfolio_history(account_id)
    print(f"  Data points: {len(history.epoch_ms)}")
    if history.epoch_ms:
        start_date = datetime.fromtimestamp(history.epoch_ms[0] / 1000)
        end_date = datetime.fromtimestamp(history.epoch_ms[-1] / 1000)
        print(f"  Date Range: {start_date.date()} to {end_date.date()}")
        print(f"  Starting Value: ${history.series[0]:,.2f}")
        print(f"  Ending Value: ${history.series[-1]:,.2f}")
        change = history.series[-1] - history.series[0]
        change_pct = change / history.series[0] if history.series[0] != 0 else 0
        print(f"  Total Change: ${change:,.2f} ({change_pct:.2%})")
    print()

    if symphony_stats.symphonies:
        symphony_id = symphony_stats.symphonies[0].id
        print("=" * 60)
        print(f"SYMPHONY HISTORY: {symphony_stats.symphonies[0].name}")
        print("=" * 60)
        symphony_history = client.portfolio.get_symphony_holdings(
            account_id, symphony_id
        )
        print(f"  Data points: {len(symphony_history.epoch_ms)}")
        if symphony_history.epoch_ms:
            start_date = datetime.fromtimestamp(symphony_history.epoch_ms[0] / 1000)
            end_date = datetime.fromtimestamp(symphony_history.epoch_ms[-1] / 1000)
            print(f"  Date Range: {start_date.date()} to {end_date.date()}")
            print(f"  Starting Value: ${symphony_history.series[0]:,.2f}")
            print(f"  Ending Value: ${symphony_history.series[-1]:,.2f}")
            if symphony_history.deposit_adjusted_series:
                print(
                    f"  Deposit-Adjusted Ending: ${symphony_history.deposit_adjusted_series[-1]:,.2f}"
                )


if __name__ == "__main__":
    main()
