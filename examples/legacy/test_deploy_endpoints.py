"""Example file to test deploy endpoints."""

import os
from composer import ComposerClient
from dotenv import load_dotenv

load_dotenv()

SYMPHONY_ID = "SvfHiUshxXcHUfoCyvn5"


def main():
    api_key = os.environ.get("COMPOSER_API_KEY")
    api_secret = os.environ.get("COMPOSER_API_SECRET")

    if not api_key or not api_secret:
        print("Error: COMPOSER_API_KEY and COMPOSER_API_SECRET must be set")
        return

    client = ComposerClient(api_key, api_secret)

    print("=" * 60)
    print("Testing Deploy Endpoints")
    print("=" * 60)

    # Get accounts
    print("\n1. Get Accounts:")
    print("-" * 40)
    try:
        accounts = client.accounts.list()
        print(f"   Number of accounts: {len(accounts.accounts)}")
        if not accounts.accounts:
            print("   No accounts found!")
            return
        account_id = accounts.accounts[0].account_uuid
        print(f"   Using account_id: {account_id}")
    except Exception as e:
        print(f"   Error: {e}")
        return

    # Test: Invest (create a deploy)
    print("\n2. Invest (create deploy):")
    print("-" * 40)
    try:
        amount = 100.0  # $100
        result = client.deploy.invest(account_id, SYMPHONY_ID, amount)
        print(f"   Deploy ID: {result.deploy_id}")
        print(f"   Deploy time: {result.deploy_time}")
        deploy_id = result.deploy_id
    except Exception as e:
        print(f"   Error: {e}")
        deploy_id = None

    if deploy_id:
        # Test: Cancel the deploy
        print("\n3. Cancel Deploy (delete):")
        print("-" * 40)
        try:
            client.deploy.delete_deploy(account_id, deploy_id)
            print(f"   Deploy {deploy_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    # Test: Get deploys to see what's queued
    print("\n4. Get Deploys:")
    print("-" * 40)
    try:
        deploys = client.deploy.get_deploys(account_id, status="QUEUED")
        print(f"   Number of queued deploys: {len(deploys.deploys)}")
        for d in deploys.deploys[:3]:
            print(f"   - {d.deploy_id}: {d.type} ({d.status})")
    except Exception as e:
        print(f"   Error: {e}")

    # Test: Withdraw
    print("\n5. Withdraw:")
    print("-" * 40)
    try:
        amount = 50.0  # $50
        result = client.deploy.withdraw(account_id, SYMPHONY_ID, amount)
        print(f"   Deploy ID: {result.deploy_id}")
        print(f"   Deploy time: {result.deploy_time}")
        deploy_id = result.deploy_id
    except Exception as e:
        print(f"   Error: {e}")
        deploy_id = None

    if deploy_id:
        print("\n5b. Cancel Withdraw:")
        print("-" * 40)
        try:
            client.deploy.delete_deploy(account_id, deploy_id)
            print(f"   Deploy {deploy_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    # Test: Go to cash
    print("\n6. Go to Cash:")
    print("-" * 40)
    try:
        result = client.deploy.go_to_cash(account_id, SYMPHONY_ID)
        print(f"   Deploy ID: {result.deploy_id}")
        print(f"   Deploy time: {result.deploy_time}")
        deploy_id = result.deploy_id
    except Exception as e:
        print(f"   Error: {e}")
        deploy_id = None

    if deploy_id:
        print("\n6b. Cancel Go to Cash:")
        print("-" * 40)
        try:
            client.deploy.delete_deploy(account_id, deploy_id)
            print(f"   Deploy {deploy_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    # Test: Liquidate
    print("\n7. Liquidate:")
    print("-" * 40)
    try:
        result = client.deploy.liquidate(account_id, SYMPHONY_ID)
        print(f"   Deploy ID: {result.deploy_id}")
        print(f"   Deploy time: {result.deploy_time}")
        deploy_id = result.deploy_id
    except Exception as e:
        print(f"   Error: {e}")
        deploy_id = None

    if deploy_id:
        print("\n7b. Cancel Liquidate:")
        print("-" * 40)
        try:
            client.deploy.delete_deploy(account_id, deploy_id)
            print(f"   Deploy {deploy_id} cancelled successfully")
        except Exception as e:
            print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
