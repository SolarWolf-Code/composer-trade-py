"""
Example: Dry run rebalances and trade preview.

This example shows how to preview trades and rebalancing actions before execution,
and generate trade previews for a single symphony.
"""

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
    print("DRY RUN REBALANCES")
    print("=" * 60)
    print("Running dry run for all accounts...")

    dry_run_results = client.dry_run.dry_run()

    print(f"\nResults for {len(dry_run_results)} accounts:\n")

    for result in dry_run_results:
        print(f"  Account: {result['account_name']} ({result['broker']})")
        print(f"    UUID: {result['broker_account_uuid']}")
        print(f"    Type: {result['account_type']}")
        print(f"    Total Symphonies: {result['dry_run_total_symphonies']}")

        dry_run = result.get("dry_run_result", {})
        if dry_run:
            for symphony_id, symphony_data in dry_run.items():
                print(
                    f"\n    Symphony: {symphony_data.get('symphony_name', symphony_id)}"
                )
                print(f"      Rebalanced: {symphony_data.get('rebalanced')}")
                print(f"      Value: ${symphony_data.get('symphony_value', 0):,.2f}")
                print(
                    f"      Queued Cash Change: ${symphony_data.get('queued_cash_change', 0):,.2f}"
                )

                trades = symphony_data.get("recommended_trades", [])
                if trades:
                    print(f"      Recommended Trades ({len(trades)}):")
                    for trade in trades[:3]:
                        print(
                            f"        - {trade['ticker']}: {trade.get('quantity', 0):.4f} shares "
                            f"(${trade.get('notional', 0):,.2f}) "
                            f"[{trade.get('prev_weight', 0):.1%} -> {trade.get('next_weight', 0):.1%}]"
                        )
                    if len(trades) > 3:
                        print(f"        ... and {len(trades) - 3} more trades")
        print()

    print("=" * 60)
    print("TRADE PREVIEW FOR SYMPHONY")
    print("=" * 60)

    symphony_stats = client.portfolio.get_symphony_stats_meta(account_id)
    if symphony_stats.symphonies:
        symphony_id = symphony_stats.symphonies[0].id
        symphony_name = symphony_stats.symphonies[0].name
        print(f"Generating trade preview for: {symphony_name}\n")

        preview = client.dry_run.trade_preview(
            symphony_id=symphony_id,
            broker_account_uuid=account_id,
        )

        print(f"  Symphony: {preview.get('symphony_name')}")
        print(f"  Rebalanced: {preview.get('rebalanced')}")
        print(f"  Symphony Value: ${preview.get('symphony_value', 0):,.2f}")
        print(f"  Next Rebalance After: {preview.get('next_rebalance_after')}")
        print(f"  Queued Cash Change: ${preview.get('queued_cash_change', 0):,.2f}")
        print(
            f"  Rebalance Frequency Override: {preview.get('rebalance_frequency_override')}"
        )
        print(f"  Adjusted for DTBP: {preview.get('adjusted_for_dtbp')}")

        trades = preview.get("recommended_trades", [])
        if trades:
            print(f"\n  Recommended Trades ({len(trades)}):\n")
            for trade in trades:
                print(f"    {trade['symbol']}")
                print(f"      Side: {trade['side']}")
                print(f"      Type: {trade['type']}")
                print(f"      Shares: {trade.get('share_change', 0):.4f}")
                print(f"      Cash Change: ${trade.get('cash_change', 0):,.2f}")
                print(f"      Average Price: ${trade.get('average_price', 0):.2f}")
                print(
                    f"      Weight: {trade.get('prev_weight', 0):.1%} -> {trade.get('next_weight', 0):.1%}"
                )
                print()
    else:
        print("  No symphonies found in this account.")


if __name__ == "__main__":
    main()
