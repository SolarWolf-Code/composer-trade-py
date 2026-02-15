from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MarketHoursEntry(BaseModel):
    """Market hours for a specific date."""

    is_market_open: bool = Field(description="Whether the market is open on this date")
    nyse_market_date: str = Field(description="The NYSE market date (YYYY-MM-DD)")
    market_open: Optional[str] = Field(None, description="Market open time (ISO 8601)")
    market_close: Optional[str] = Field(
        None, description="Market close time (ISO 8601)"
    )


class MarketHoursResponse(BaseModel):
    """Response containing market hours for the upcoming week."""

    market_hours: List[MarketHoursEntry] = Field(
        description="List of market hours entries"
    )


class Deploy:
    def __init__(self, http_client):
        self.http_client = http_client

    def get_market_hours(self) -> MarketHoursResponse:
        """
        Get market hours for the upcoming week.

        Returns:
            MarketHoursResponse with schedule for each day
        """
        response = self.http_client.get("/api/v0.1/deploy/market-hours")
        return MarketHoursResponse.model_validate(response)

    def invest(
        self, account_id: str, symphony_id: str, amount: float
    ) -> Dict[str, Any]:
        """
        Invest amount into a symphony.
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/invest",
            json={"amount": amount},
        )

    def withdraw(
        self, account_id: str, symphony_id: str, amount: float
    ) -> Dict[str, Any]:
        """
        Withdraw amount from a symphony.
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/withdraw",
            json={"amount": amount},
        )

    def skip_automated_rebalance(
        self, account_id: str, symphony_id: str, skip: bool = True
    ) -> None:
        """
        Skip or resume automated rebalancing for a symphony.

        Args:
            account_id: UUID of the account
            symphony_id: UUID of the symphony
            skip: True to skip next rebalance, False to resume
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/skip-automated-rebalance",
            json={"skip": skip},
        )

    def rebalance(self, account_id: str, symphony_id: str) -> Dict[str, Any]:
        """
        Trigger a rebalance for a symphony.
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/rebalance"
        )

    def go_to_cash(self, account_id: str, symphony_id: str) -> Dict[str, Any]:
        """
        Move symphony assets to cash.
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/go-to-cash"
        )

    def liquidate(self, account_id: str, symphony_id: str) -> Dict[str, Any]:
        """
        Liquidate all assets in a symphony.
        """
        return self.http_client.post(
            f"/api/v0.1/deploy/accounts/{account_id}/symphonies/{symphony_id}/liquidate"
        )
