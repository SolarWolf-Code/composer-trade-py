"""Deploy models - response models for deploy endpoints."""

from pydantic import BaseModel, Field


class MarketHoursItem(BaseModel):
    """Market hours for a single day."""

    is_market_open: bool = Field(description="Whether the market is open on this date")
    nyse_market_date: str = Field(description="NYSE market date (YYYY-MM-DD)")
    market_open: str | None = Field(None, description="Market open time (ISO 8601)")
    market_close: str | None = Field(None, description="Market close time (ISO 8601)")


class MarketHoursResponse(BaseModel):
    """Response containing market hours schedule."""

    market_hours: list[MarketHoursItem] = Field(description="List of market hours for the week")


class DeploySymphony(BaseModel):
    """Symphony with pending invests."""

    symphony_id: str = Field(description="Unique identifier of the symphony")
    name: str = Field(description="Name of the symphony")
    asset_class: str = Field(description="Deprecated. See asset_classes.")
    asset_classes: list[str] = Field(description="Asset classes for the symphony")
    description: str = Field(description="Description of the symphony")
    color: str = Field(description="Color associated with the symphony")
    community_review_status: str | None = Field(None, description="Community review status")
    last_semantic_update_at: str = Field(description="Last semantic update time (ISO 8601)")
    rebalance_frequency: str = Field(description="Rebalance frequency")
    rebalance_corridor_width: float | None = Field(None, description="Rebalance corridor width")
    is_shared: bool = Field(description="Whether the symphony is shared")


class DeploySymphoniesResponse(BaseModel):
    """Response containing symphonies with pending invests."""

    symphonies: list[DeploySymphony] = Field(description="List of symphonies with pending invests")


class Deploy(BaseModel):
    """A deployment of a symphony to an account."""

    position_id: str | None = Field(None, description="Position ID")
    symphony_id: str | None = Field(None, description="Symphony ID")
    deploy_created_by: str | None = Field(None, description="User who created the deploy")
    deploy_id: str = Field(description="Unique identifier for the deployment")
    type: str = Field(description="Type of deployment")
    status: str = Field(description="Status of the deployment")
    cash_change: float | None = Field(None, description="Cash change")
    requested_cash_change: float | None = Field(None, description="Requested cash change")
    pending_buying_power: bool = Field(description="Whether buying power is pending")
    created_at: str = Field(description="When the deploy was created (ISO 8601)")


class DeploysResponse(BaseModel):
    """Response containing list of deploys."""

    deploys: list[Deploy] = Field(description="List of deploys")


class DeployActionResponse(BaseModel):
    """Response from a deploy action (invest, withdraw, liquidate, etc.)."""

    deploy_id: str = Field(description="Unique identifier for the deployment")
    deploy_time: str | None = Field(None, description="When the deploy is scheduled")
    deploy_on_market_open: bool | None = Field(
        None, description="Whether deploy executes on market open"
    )
    symphony_id: str | None = Field(None, description="Symphony ID")


__all__ = [
    "MarketHoursItem",
    "MarketHoursResponse",
    "DeploySymphony",
    "DeploySymphoniesResponse",
    "Deploy",
    "DeploysResponse",
    "DeployActionResponse",
]
