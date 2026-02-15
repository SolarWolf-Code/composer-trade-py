from typing import List, Optional
from ..models.accounts import (
    Account,
    Holding,
    InvestorDocument,
    AccountsListResponse,
    InvestorDocumentCategory,
)


class Accounts:
    """Resource for managing brokerage accounts."""

    def __init__(self, http_client):
        self.http_client = http_client

    def list(self) -> List[Account]:
        """
        List all accounts for the authenticated user.

        Returns:
            List of Account objects with details about each account

        Example:
            accounts = client.accounts.list()
            for account in accounts:
                print(f"{account.account_type}: {account.status}")
        """
        response = self.http_client.get("/api/v0.1/accounts/list")
        parsed = AccountsListResponse.model_validate(response)
        return parsed.accounts

    def get_holdings(
        self, account_id: str, position_type: Optional[str] = None
    ) -> List[Holding]:
        """
        Get current holdings for an account.

        Args:
            account_id: UUID of the account
            position_type: Filter by position type (DEFAULT_DIRECT, SYMPHONY, ALL)

        Returns:
            List of Holding objects

        Example:
            holdings = client.accounts.get_holdings("account-uuid")
            for holding in holdings:
                print(f"{holding.ticker}: {holding.quantity} shares")
        """
        params = {}
        if position_type:
            params["position_type"] = position_type

        response = self.http_client.get(
            f"/api/v0.1/accounts/{account_id}/holdings", params=params
        )

        # Parse each holding in the list
        return [Holding.model_validate(h) for h in response]

    def get_investor_documents(
        self, account_id: str, category: InvestorDocumentCategory, year: int
    ) -> List[InvestorDocument]:
        """
        Get investor documents for Apex or Alpaca accounts.

        Includes tax documents (1099s), account statements, trade confirmations, etc.

        Args:
            account_id: UUID of the account
            category: Category of documents to retrieve
            year: Year of the documents to retrieve

        Returns:
            List of InvestorDocument objects

        Example:
            docs = client.accounts.get_investor_documents(
                "account-uuid", InvestorDocumentCategory.TAX_FORM
            )
            for doc in docs:
                print(f"{doc.type}: {doc.file_name}")
        """
        response = self.http_client.get(
            f"/api/v0.1/accounts/{account_id}/info/investor-documents",
            params={"category": category.value, "year": year},
        )

        return [InvestorDocument.model_validate(d) for d in response]
