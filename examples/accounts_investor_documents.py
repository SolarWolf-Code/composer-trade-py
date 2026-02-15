"""
Example: Get investor documents.

This example shows how to retrieve investor documents (statements, tax forms,
trade confirmations) for Apex or Alpaca accounts.
"""

from composer import ComposerClient
from composer.models.accounts import InvestorDocumentCategory
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    import datetime

    client = ComposerClient(
        api_key=os.getenv("COMPOSER_API_KEY"),
        api_secret=os.getenv("COMPOSER_API_SECRET"),
    )
    current_year = datetime.datetime.now().year

    print("Fetching accounts...")
    accounts = client.accounts.list()

    if not accounts:
        print("No accounts found.")
        return

    account = accounts[0]
    print(f"\nUsing account: {account.account_uuid} ({account.broker})\n")

    categories = [
        InvestorDocumentCategory.STATEMENT,
        InvestorDocumentCategory.TAX_FORM,
        InvestorDocumentCategory.TRADE_CONFIRMATION,
    ]

    for category in categories:
        print(f"Fetching {category.value} documents for {current_year}...")
        try:
            docs = client.accounts.get_investor_documents(
                account.account_uuid, category, current_year
            )

            if docs:
                print(f"\n  {category.value} ({len(docs)} documents):\n")
                for doc in docs:
                    print(f"    {doc.file_name}")
                    print(f"      ID: {doc.id}")
                    print(f"      Type: {doc.type}")
                    print(f"      Date: {doc.date}")
                    print(f"      URL: {doc.url}")
                    if doc.tax_ids:
                        print(f"      Tax IDs: {doc.tax_ids}")
                    print()
            else:
                print(f"  No {category.value} documents found.\n")
        except Exception as e:
            print(f"  Error fetching {category.value} documents: {e}")


if __name__ == "__main__":
    main()
