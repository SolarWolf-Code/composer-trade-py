"""
Example: Testing Reports endpoints.

This demonstrates the reports endpoint:
- get

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    python examples/test_reports_endpoints.py
"""

import os
from composer import ComposerClient
from composer.models.reports import ReportType
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
        print("\nFetching accounts list to get account_id...")
        try:
            accounts_response = client.accounts.list()
            if accounts_response.accounts:
                account_id = accounts_response.accounts[0].account_uuid
                print(f"Using first account: {account_id}")
            else:
                print("ERROR: No accounts found")
                return
        except Exception as e:
            print(f"ERROR: {e}")
            return

    print("\n" + "=" * 60)
    print("REPORTS ENDPOINTS")
    print("=" * 60)

    # Test: get report
    print("\n1. get (trade-activity report)")
    try:
        report = client.reports.get(
            account_id,
            since="2025-10-01",
            until="2025-12-31",
            report_type=ReportType.TRADE_ACTIVITY,
        )
        print(f"   SUCCESS: Got trade activity report")
        print(f"   Type: {type(report)}")
        if isinstance(report, dict):
            print(f"   Keys: {list(report.keys())[:10]}")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n2. get (non-trade-activity report)")
    try:
        report = client.reports.get(
            account_id,
            since="2025-10-01",
            until="2025-12-31",
            report_type=ReportType.NON_TRADE_ACTIVITY,
        )
        print(f"   SUCCESS: Got non-trade activity report")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n3. get (without report-type)")
    try:
        report = client.reports.get(
            account_id,
            since="2025-10-01",
            until="2025-12-31",
        )
        print(f"   SUCCESS: Got report without report-type")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
