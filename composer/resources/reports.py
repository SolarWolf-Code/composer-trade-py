"""Reports resource for account reports endpoints."""

from ..models.reports import ReportType


class Reports:
    """Resource for account reports endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get(
        self,
        account_id: str,
        since: str,
        until: str,
        report_type: ReportType | None = None,
    ) -> str:
        """
        Get a report for the given account.

        Args:
            account_id: The account UUID
            since: Start date for the report (ISO format)
            until: End date for the report (ISO format)
            report_type: Type of report (trade-activity or non-trade-activity)

        Returns
        -------
            CSV report data as a string
        """
        params = {
            "since": since,
            "until": until,
        }
        if report_type:
            params["report-type"] = report_type.value

        response = self._client.get(
            f"/api/v1/reports/{account_id}",
            params=params,
            headers={"Accept": "text/csv"},
        )
        return response
