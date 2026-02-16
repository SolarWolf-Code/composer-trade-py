"""Dry run models."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class TradeSide(str, Enum):
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
    name: Optional[str] = None
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
    recommended_trades: List[RecommendedTrade]
    queued_cash_change: float
    symphony_value: float
    symphony_name: str
    next_rebalance_date: Optional[str] = None


class TradePreviewResult(BaseModel):
    """Trade preview result for a symphony."""

    model_config = {"populate_by_name": True}

    rebalanced: bool
    next_rebalance_after: str
    recommended_trades: List[PreviewRecommendedTrade]
    queued_cash_change: float
    rebalance_frequency_override: bool
    rebalance_request_uuid: Optional[str] = None
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
    dry_run_missing_symphonies: Optional[dict] = None
    dry_run_total_symphonies: int


class DryRunRequest(BaseModel):
    """Request body for dry run endpoint."""

    model_config = {"populate_by_name": True}

    account_uuids: Optional[List[str]] = None
    send_segment_event: bool = False


class TradePreviewRequest(BaseModel):
    """Request body for trade preview endpoint."""

    model_config = {"populate_by_name": True}

    amount: Optional[float] = None
    broker_account_uuid: Optional[str] = None


class AccountSource(str, Enum):
    """Account source for dry run."""

    QUEUED = "queued"
    DEPLOYABLE = "deployable"
    ALL_TRADABLE = "all_tradable"


class CreateDryRunRequest(BaseModel):
    """Request body for rebalance dry run endpoint."""

    account_source: AccountSource = Field(
        default=AccountSource.QUEUED, description="Account source to include in dry run"
    )
    dry_run_time: Optional[str] = Field(
        None, description="Time to run the dry run (ISO 8601 format)"
    )


class DryRunEnqueueResponse(BaseModel):
    """Response from enqueuing a dry run."""

    num_accounts: int = Field(description="Number of accounts included in dry run")
    dry_run_time: str = Field(description="Time the dry run was triggered")
