"""Portfolio resource for portfolio and holdings endpoints."""

from typing import List, Optional
from ..models.portfolio import (
    HoldingStatsResponse,
    TotalStats,
    SymphonyStatsMetaResponse,
    SymphonyStatsResponse,
    PortfolioHistory,
    TimeSeries,
    SymphonyHoldings,
    ActivityHistoryResponse,
    DeployHistoryResponse,
)
from ..models.accounts import Holding


class Portfolio:
    """Resource for portfolio and holdings endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_account_holdings(
        self,
        account_id: str,
        position_type: Optional[str] = None,
    ) -> List[Holding]:
        """
        Get all current positions held in the specified account.

        Args:
            account_id: The account UUID
            position_type: Optional filter - 'direct', 'symphony', or 'all'

        Returns:
            List of holdings in the account
        """
        params = {}
        if position_type:
            position_type_map = {
                "direct": "DEFAULT_DIRECT",
                "symphony": "SYMPHONY",
                "all": "ALL",
            }
            params["position_type"] = position_type_map.get(
                position_type.lower(), position_type.upper()
            )
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/holdings",
            params=params if params else None,
        )
        return [Holding.model_validate(h) for h in response]

    def get_total_stats(self, account_id: str) -> TotalStats:
        """
        Get aggregate portfolio statistics for an account.

        Args:
            account_id: The account UUID

        Returns:
            Total portfolio statistics including value, returns, cash, etc.
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/total-stats",
        )
        return TotalStats.model_validate(response)

    def get_symphony_stats(self, account_id: str) -> SymphonyStatsResponse:
        """
        Get aggregate stats per symphony for an account.

        Args:
            account_id: The account UUID

        Returns:
            Stats for each symphony in the account
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphony-stats",
        )
        return SymphonyStatsResponse.model_validate(response)

    def get_symphony_stats_meta(self, account_id: str) -> SymphonyStatsMetaResponse:
        """
        Get aggregate stats per symphony with metadata for an account.

        Args:
            account_id: The account UUID

        Returns:
            Stats with metadata for each symphony in the account
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphony-stats-meta",
        )
        return SymphonyStatsMetaResponse.model_validate(response)

    def get_portfolio_history(self, account_id: str) -> PortfolioHistory:
        """
        Get the value of the account portfolio over time.

        Args:
            account_id: The account UUID

        Returns:
            Portfolio value history with timestamps and values
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/portfolio-history",
        )
        return PortfolioHistory.model_validate(response)

    def get_symphony_value_history(
        self,
        account_id: str,
        symphony_id: str,
    ) -> TimeSeries:
        """
        Get the value of a symphony position over time.

        Args:
            account_id: The account UUID
            symphony_id: The symphony UUID

        Returns:
            Symphony value history including deposit-adjusted series
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphonies/{symphony_id}",
        )
        return TimeSeries.model_validate(response)

    def get_symphony_holdings(
        self,
        account_id: str,
        symphony_id: str,
    ) -> SymphonyHoldings:
        """
        Get the current holdings of a symphony.

        Args:
            account_id: The account UUID
            symphony_id: The symphony UUID

        Returns:
            Current holdings including cash, shares, etc.
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphonies/{symphony_id}/holdings",
        )
        print(response)
        return SymphonyHoldings.model_validate(response)

    def get_holdings_by_position(self, position_id: str) -> SymphonyHoldings:
        """
        Get the current holdings of a symphony from position ID.

        Args:
            position_id: The position UUID

        Returns:
            Current holdings including cash, shares, etc.
        """
        response = self._client.get(
            f"/api/v1/portfolio/positions/{position_id}/holdings",
        )
        return SymphonyHoldings.model_validate(response)

    def get_activity_history(
        self,
        account_id: str,
        symphony_id: str,
        limit: int,
        offset: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> ActivityHistoryResponse:
        """
        Get the activity history for a symphony.

        Activity types include: edit, invest, withdraw, rebalance, etc.

        Args:
            account_id: The account UUID
            symphony_id: The symphony UUID
            limit: Maximum number of results to return
            offset: Offset for pagination
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)

        Returns:
            Activity history for the symphony
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphonies/{symphony_id}/activity-history",
            params=params,
        )
        return ActivityHistoryResponse.model_validate(response)

    def get_deploy_details(
        self,
        account_id: str,
        symphony_id: str,
        deploy_id: str,
    ) -> DeployHistoryResponse:
        """
        Get the details about a deploy from the perspective of the symphony.

        Args:
            account_id: The account UUID
            symphony_id: The symphony UUID
            deploy_id: The deploy UUID

        Returns:
            Deploy history including parent deploys
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/symphonies/{symphony_id}/deploys/{deploy_id}",
        )
        return DeployHistoryResponse.model_validate(response)

    def get_holding_stats(self, account_id: str) -> HoldingStatsResponse:
        """
        Get holding statistics for an account.

        Returns the direct and symphony allocations, amounts, and values by holding.
        Includes current prices, daily change percentages, and notional values.

        Args:
            account_id: The account UUID

        Returns:
            Detailed holding statistics
        """
        response = self._client.get(
            f"/api/v1/portfolio/accounts/{account_id}/holding-stats",
        )
        return HoldingStatsResponse.model_validate(response)
