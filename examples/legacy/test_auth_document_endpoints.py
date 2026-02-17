"""Example file to test auth management and document endpoints."""

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
    print("Testing Auth Management & Document Endpoints")
    print("=" * 60)

    # Test 1: List API keys
    print("\n1. List API Keys:")
    print("-" * 40)
    try:
        result = client.auth_management.list_api_keys()
        print(f"   Number of API keys: {len(result.api_keys)}")
        for key in result.api_keys:
            print(f"   - {key.id}")
    except Exception as e:
        print(f"   Error: {e}")

    # NOTE: create_api_key is not included in tests because it destroys the existing key
    # (users can only have one key at a time)

    # Test 2: Get accounts
    print("\n3. Get Accounts:")
    print("-" * 40)
    try:
        accounts = client.accounts.list()
        print(f"   Number of accounts: {len(accounts.accounts)}")
        if accounts.accounts:
            account_id = accounts.accounts[0].account_uuid
            print(f"   Using account_id: {account_id}")

            # Test 4: Get investor documents
            print("\n4. Get Investor Documents:")
            print("-" * 40)
            try:
                docs = client.accounts.get_investor_documents(
                    account_id=account_id, category="STATEMENT", year=2024
                )
                print(f"   Number of documents: {len(docs)}")
                for doc in docs[:3]:
                    print(f"   - {doc.id}: {doc.name}")

                # Test 5: Download document (if we have documents)
                if docs:
                    print("\n5. Download Document:")
                    print("-" * 40)
                    try:
                        url = client.accounts.download_document(docs[0].id)
                        print(f"   Download URL: {url}")
                    except Exception as e:
                        print(f"   Error: {e}")
            except Exception as e:
                print(f"   Error: {e}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Tests Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
