"""Dry run models."""

from enum import StrEnum

from pydantic import BaseModel, Field


class TradeSide(StrEnum):
    """Trade side."""

    BUY = "BUY"
    SELL = "SELL"


class RecommendedTrade(BaseModel):
    """A recommended trade in a dry run or preview."""

    model_config = {"populate_by_name": True}

    ticker: str
    notional: float
    quantity: float
    prev_value: float
    prev_weight: float
    next_weight: float


class PreviewRecommendedTrade(BaseModel):
    """A recommended trade in a trade preview."""

    model_config = {"populate_by_name": True}

    at: str
    average_price: float
    cash_change: float
    share_change: float
    symbol: str
    name: str | None = None
    side: TradeSide
    type: str
    prev_value: float
    prev_weight: float
    next_weight: float


class DryRunResult(BaseModel):
    """Dry run result for a single symphony."""

    model_config = {"populate_by_name": True}

    rebalanced: bool
    next_rebalance_after: str
    recommended_trades: list[RecommendedTrade]
    queued_cash_change: float
    symphony_value: float
    symphony_name: str
    next_rebalance_date: str | None = None


class TradePreviewResult(BaseModel):
    """Trade preview result for a symphony."""

    model_config = {"populate_by_name": True}

    rebalanced: bool
    next_rebalance_after: str
    recommended_trades: list[PreviewRecommendedTrade]
    queued_cash_change: float
    rebalance_frequency_override: bool
    rebalance_request_uuid: str | None = None
    adjusted_for_dtbp: bool
    symphony_value: float
    symphony_name: str


class AccountDryRunResult(BaseModel):
    """Dry run result for an account."""

    model_config = {"populate_by_name": True}

    broker_account_uuid: str
    account_type: str
    account_name: str
    broker: str
    dry_run_result: dict
    dry_run_missing_symphonies: dict | None = None
    dry_run_total_symphonies: int


class DryRunRequest(BaseModel):
    """Request body for dry run endpoint."""

    model_config = {"populate_by_name": True}

    account_uuids: list[str] | None = None
    send_segment_event: bool = False


class TradePreviewRequest(BaseModel):
    """Request body for trade preview endpoint."""

    model_config = {"populate_by_name": True}

    amount: float | None = None
    broker_account_uuid: str | None = None


class AccountSource(StrEnum):
    """Account source for dry run."""

    QUEUED = "queued"
    DEPLOYABLE = "deployable"
    ALL_TRADABLE = "all_tradable"


class CreateDryRunRequest(BaseModel):
    """Request body for rebalance dry run endpoint."""

    account_source: AccountSource = Field(
        default=AccountSource.QUEUED, description="Account source to include in dry run"
    )
    dry_run_time: str | None = Field(None, description="Time to run the dry run (ISO 8601 format)")


class DryRunEnqueueResponse(BaseModel):
    """Response from enqueuing a dry run."""

    num_accounts: int = Field(description="Number of accounts included in dry run")
    dry_run_time: str = Field(description="Time the dry run was triggered")
