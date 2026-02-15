from typing import List
from ..models.accounts import InvestorDocument, InvestorDocumentCategory
from ..models.reports import ReportType


class Reports:
    def __init__(self, http_client):
        self.http_client = http_client

    def get_activity_report(
        self,
        account_id: str,
        since: str,
        until: str,
        report_type: ReportType = ReportType.TRADE_ACTIVITY,
    ) -> str:
        """
        Get activity report for an account.

        Args:
            account_id: UUID of the account
            since: Start date for the report period (ISO 8601 format, e.g., "2024-01-01")
            until: End date for the report period (ISO 8601 format, e.g., "2024-12-31")
            report_type: Type of report to generate

        Returns:
            CSV content as a string
        """
        params = {"since": since, "until": until, "report-type": report_type.value}
        return self.http_client.get(f"/api/v0.1/reports/{account_id}", params=params)

    def get_investor_documents(
        self, account_id: str, category: InvestorDocumentCategory, year: int
    ) -> List[InvestorDocument]:
        """
        Get investor documents for Apex or Alpaca accounts.

        Args:
            account_id: UUID of the account
            category: Category of documents to retrieve
            year: Year of the documents to retrieve

        Returns:
            List of InvestorDocument objects
        """
        response = self.http_client.get(
            f"/api/v0.1/accounts/{account_id}/info/investor-documents",
            params={"category": category.value, "year": year},
        )
        return [InvestorDocument.model_validate(d) for d in response]
