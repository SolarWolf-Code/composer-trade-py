"""
Example: Testing Cash endpoints.

This demonstrates all cash GET endpoints:
- get_transfer_constraints
- get_ach_relationships
- get_ach_limits
- get_tax_withholding_federal
- get_ach_transfers
- get_recurring_deposits
- get_recurring_deposits_meta
- get_recurring_deposits_projection
- get_all_recurring_deposits

Usage:
    # Set up credentials
    export COMPOSER_API_KEY="your-api-key"
    export COMPOSER_API_SECRET="your-api-secret"

    # Optionally set specific account ID
    export COMPOSER_ACCOUNT_ID="account-uuid"

    python examples/test_cash_endpoints.py
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
    print("CASH ENDPOINTS")
    print("=" * 60)

    # Test 1: get_transfer_constraints
    print("\n1. get_transfer_constraints")
    try:
        constraints = client.cash.get_transfer_constraints()
        print(f"   SUCCESS: Got constraints for {len(constraints)} accounts")
        for acc_id, constraint in list(constraints.items())[:3]:
            print(f"   - {acc_id[:8]}...: withdrawable=${constraint.cash_withdrawable}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 2: get_ach_relationships
    print("\n2. get_ach_relationships")
    try:
        relationships = client.cash.get_ach_relationships(include_plaid_account_details=False)
        print(f"   SUCCESS: Found {len(relationships.ach_relationships)} ACH relationships")
        print(f"   - Plaid link required: {relationships.plaid_link_required}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 3: get_ach_limits
    print("\n3. get_ach_limits")
    try:
        limits = client.cash.get_ach_limits(account_id)
        print(f"   SUCCESS: ACH limits retrieved")
        print(f"   - Cash withdrawable: ${limits.cash_withdrawable}")
        print(f"   - Depositable today: ${limits.cash_depositable_today}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 4: get_tax_withholding_federal
    print("\n4. get_tax_withholding_federal")
    try:
        tax = client.cash.get_tax_withholding_federal(account_id)
        print(f"   SUCCESS: Tax withholding info retrieved")
        print(f"   - Default rate: {tax.default_rate}%")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 5: get_ach_transfers
    print("\n5. get_ach_transfers")
    try:
        transfers = client.cash.get_ach_transfers(account_id, 2025)
        print(f"   SUCCESS: Found {len(transfers)} ACH transfers")
        for t in transfers[:3]:
            print(f"   - {t.direction}: ${t.amount} ({t.status})")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 6: get_recurring_deposits
    print("\n6. get_recurring_deposits")
    try:
        deposits = client.cash.get_recurring_deposits(account_id, n=10)
        print(f"   SUCCESS: Found {len(deposits.recurring_deposits)} recurring deposits")
        for d in deposits.recurring_deposits[:3]:
            print(f"   - {d.frequency}: ${d.amount} ({d.status})")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 7: get_recurring_deposits_meta
    print("\n7. get_recurring_deposits_meta")
    try:
        meta = client.cash.get_recurring_deposits_meta(account_id)
        print(f"   SUCCESS: Recurring deposit meta retrieved")
        if meta.MONTHLY:
            print(f"   - MONTHLY: ${meta.MONTHLY.amount}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 8: get_recurring_deposits_projection
    print("\n8. get_recurring_deposits_projection")
    try:
        projection = client.cash.get_recurring_deposits_projection(
            account_id, amount=500, frequency="MONTHLY"
        )
        print(f"   SUCCESS: Projection retrieved")
        print(f"   - Reason: {projection.reason}")
        print(f"   - Limit date: {projection.limit_date}")
    except Exception as e:
        print(f"   ERROR: {e}")

    # Test 9: get_all_recurring_deposits
    print("\n9. get_all_recurring_deposits")
    try:
        all_deposits = client.cash.get_all_recurring_deposits(n=10)
        print(f"   SUCCESS: Found {len(all_deposits.recurring_deposits)} total recurring deposits")
    except Exception as e:
        print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
