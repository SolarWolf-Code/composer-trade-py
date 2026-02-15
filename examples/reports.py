"""
Example: Get activity reports.

This example shows how to retrieve activity reports (trade-activity or
non-trade-activity) for an account.
"""

from composer import ComposerClient
from composer.models.reports import ReportType
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
    print("TRADE ACTIVITY REPORT")
    print("=" * 60)
    print("Fetching trade activity for the last 30 days...")

    from datetime import datetime, timedelta

    until = datetime.now()
    since = until - timedelta(days=30)

    report = client.reports.get_activity_report(
        account_id=account_id,
        since=since.strftime("%Y-%m-%d"),
        until=until.strftime("%Y-%m-%d"),
        report_type=ReportType.TRADE_ACTIVITY,
    )

    print(f"\nReport (first 500 chars):\n")
    print(report[:500] if len(report) > 500 else report)
    if len(report) > 500:
        print(f"\n... ({len(report)} total characters)")
    print()

    print("=" * 60)
    print("NON-TRADE ACTIVITY REPORT")
    print("=" * 60)
    print("Fetching non-trade activity for the last 30 days...")

    report = client.reports.get_activity_report(
        account_id=account_id,
        since=since.strftime("%Y-%m-%d"),
        until=until.strftime("%Y-%m-%d"),
        report_type=ReportType.NON_TRADE_ACTIVITY,
    )

    print(f"\nReport (first 500 chars):\n")
    print(report[:500] if len(report) > 500 else report)
    if len(report) > 500:
        print(f"\n... ({len(report)} total characters)")


if __name__ == "__main__":
    main()
