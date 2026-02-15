from ..models.portfolio import (
    HoldingStatsResponse,
    TotalStats,
    SymphonyStatsMetaResponse,
    TimeSeries,
    PortfolioHistory,
)


class Portfolio:
    def __init__(self, http_client):
        self.http_client = http_client

    def get_holding_stats(self, account_id: str) -> HoldingStatsResponse:
        """
        Get statistics for current holdings.

        Args:
            account_id: UUID of the account

        Returns:
            HoldingStatsResponse with detailed statistics for each holding
        """
        response = self.http_client.get(
            f"/api/v0.1/portfolio/accounts/{account_id}/holding-stats"
        )
        return HoldingStatsResponse.model_validate(response)

    def get_total_stats(self, account_id: str) -> TotalStats:
        """
        Get total portfolio statistics.

        Args:
            account_id: UUID of the account

        Returns:
            TotalStats with aggregate portfolio statistics
        """
        response = self.http_client.get(
            f"/api/v0.1/portfolio/accounts/{account_id}/total-stats"
        )
        return TotalStats.model_validate(response)

    def get_symphony_stats_meta(self, account_id: str) -> SymphonyStatsMetaResponse:
        """
        Get metadata stats for symphonies in the account.

        Args:
            account_id: UUID of the account

        Returns:
            SymphonyStatsMetaResponse with stats for each symphony
        """
        response = self.http_client.get(
            f"/api/v0.1/portfolio/accounts/{account_id}/symphony-stats-meta"
        )
        return SymphonyStatsMetaResponse.model_validate(response)

    def get_symphony_holdings(self, account_id: str, symphony_id: str) -> TimeSeries:
        """
        Get the value of a specific symphony position over time.

        Args:
            account_id: UUID of the account
            symphony_id: UUID of the symphony

        Returns:
            TimeSeries with value history for the symphony
        """
        response = self.http_client.get(
            f"/api/v0.1/portfolio/accounts/{account_id}/symphonies/{symphony_id}"
        )
        return TimeSeries.model_validate(response)

    def get_portfolio_history(self, account_id: str) -> PortfolioHistory:
        """
        Get historical performance of the portfolio.

        Args:
            account_id: UUID of the account

        Returns:
            PortfolioHistory with account value over time
        """
        response = self.http_client.get(
            f"/api/v0.1/portfolio/accounts/{account_id}/portfolio-history"
        )
        return PortfolioHistory.model_validate(response)
