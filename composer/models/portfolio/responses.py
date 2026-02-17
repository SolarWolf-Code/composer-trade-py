"""Portfolio response models."""

from datetime import date, datetime, timezone, timedelta
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator

EST_OFFSET = timedelta(hours=5)


def _epoch_ms_to_date_string(epoch_ms: int) -> str:
    """Convert epoch milliseconds to ISO date string (assuming EST timestamp from API)."""
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc) + EST_OFFSET
    return dt.date().isoformat()


def _transform_epoch_series_to_by_date(
    epoch_ms: List[int],
    series: List[float],
    deposit_adjusted_series: Optional[List[float]] = None,
) -> "Dict[str, TimeSeriesEntry]":
    """Transform epoch_ms + series to {date: TimeSeriesEntry} format."""
    result: "Dict[str, TimeSeriesEntry]" = {}

    for i, epoch in enumerate(epoch_ms):
        date_str = _epoch_ms_to_date_string(epoch)
        entry: Dict[str, float] = {"series": series[i]}
        if deposit_adjusted_series:
            entry["deposit_adjusted_series"] = deposit_adjusted_series[i]
        result[date_str] = TimeSeriesEntry(**entry)

    return dict(sorted(result.items()))


class AssetClass(str, Enum):
    """Asset class types."""

    CRYPTO = "CRYPTO"
    EQUITIES = "EQUITIES"
    OPTIONS = "OPTIONS"


class PositionDirection(str, Enum):
    """Position direction."""

    LONG = "LONG"
    SHORT = "SHORT"


class OptionsDetails(BaseModel):
    """Details for options contract holdings."""

    model_config = {"populate_by_name": True}

    underlying_asset_symbol: str
    strike_price: float
    expiry: str
    contract_type: str
    underlying_price: Optional[float] = None
    underlying_price_todays_change: Optional[float] = None
    underlying_price_todays_change_percent: Optional[float] = None


class HoldingAllocation(BaseModel):
    """Allocation details for a holding."""

    model_config = {"populate_by_name": True}

    allocation: float
    amount: float
    value: float
    direction: Optional[PositionDirection] = None


class SymphonyAllocation(BaseModel):
    """Symphony allocation details."""

    model_config = {"populate_by_name": True}

    symphony_id: str
    allocation: float
    value: float


class SymphonyHoldingAllocation(BaseModel):
    """Aggregate symphony allocation for a holding."""

    model_config = {"populate_by_name": True}

    allocation: float
    amount: float
    value: float
    direction: Optional[PositionDirection] = None
    symphonies: List[SymphonyAllocation] = []


class HoldingStats(BaseModel):
    """Detailed statistics for a holding."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: Optional[str] = None
    asset_class: Optional[AssetClass] = None
    options_details: Optional[OptionsDetails] = None
    price: float
    price_todays_change: float
    price_todays_change_percent: float
    direct: HoldingAllocation
    symphony: SymphonyHoldingAllocation
    notional_value: Optional[float] = None
    delta_dollars: Optional[float] = None
    todays_change_percent: float
    todays_change: float
    total_change_percent: Optional[float] = None
    total_change: Optional[float] = None
    cost_basis: Optional[float] = None
    average_cost_basis: Optional[float] = None


class HoldingStatsResponse(BaseModel):
    """Response from getting holding statistics."""

    model_config = {"populate_by_name": True}

    holdings: List[HoldingStats] = []


class TotalStats(BaseModel):
    """Aggregate portfolio statistics."""

    model_config = {"populate_by_name": True}

    portfolio_value: float
    simple_return: float
    time_weighted_return: float
    net_deposits: float
    todays_dollar_change: float
    todays_percent_change: float
    total_cash: float
    total_unallocated_cash: float
    pending_withdrawals: Optional[float] = None
    pending_net_deposits: Optional[float] = None
    pending_deploys_cash: float


class SymphonyHolding(BaseModel):
    """A holding within a symphony."""

    model_config = {"populate_by_name": True}

    ticker: str
    price: float
    allocation: float
    amount: float
    value: float
    last_percent_change: Optional[float] = None


class SymphonyStatsMeta(BaseModel):
    """Metadata and stats for a symphony."""

    model_config = {"populate_by_name": True}

    id: str
    position_id: str
    as_of: Optional[str] = None
    holdings: List[SymphonyHolding] = []
    simple_return: float
    time_weighted_return: float
    net_deposits: float
    last_dollar_change: float
    cash: float
    value: float
    deposit_adjusted_value: float
    annualized_rate_of_return: float
    sharpe_ratio: float
    max_drawdown: float
    last_percent_change: float
    invested_since: str
    last_rebalance_on: Optional[str] = None
    last_rebalance_attempted_on: Optional[str] = None
    name: str
    asset_class: AssetClass
    asset_classes: List[AssetClass]
    color: str
    community_review_status: Optional[str] = None
    description: str
    last_semantic_update_at: str
    tags: List[str] = []
    rebalance_frequency: str
    is_shared: bool
    tickers: List[dict] = []
    rebalance_corridor_width: Optional[float] = None
    next_rebalance_on: Optional[str] = None
    may_rebalance_today: bool
    skip_rebalance_today: bool


class SymphonyStatsMetaResponse(BaseModel):
    """Response from getting symphony stats metadata."""

    model_config = {"populate_by_name": True}

    symphonies: List[SymphonyStatsMeta] = []


class TimeSeriesEntry(BaseModel):
    """A single time series data point."""

    series: float
    deposit_adjusted_series: Optional[float] = None


class TimeSeries(BaseModel):
    """Portfolio value over time."""

    model_config = {"populate_by_name": True}

    dates: Dict[str, TimeSeriesEntry] = {}

    @model_validator(mode="before")
    @classmethod
    def transform_epoch_to_dates(cls, v):
        if isinstance(v, dict) and "epoch_ms" in v:
            epoch_ms = v.get("epoch_ms", [])
            series = v.get("series", [])
            deposit_adjusted_series = v.get("deposit_adjusted_series")
            dates = _transform_epoch_series_to_by_date(epoch_ms, series, deposit_adjusted_series)
            return {"dates": dates}
        return v


class PortfolioHistory(BaseModel):
    """Account portfolio history."""

    model_config = {"populate_by_name": True}

    dates: Dict[str, TimeSeriesEntry] = {}

    @model_validator(mode="before")
    @classmethod
    def transform_epoch_to_dates(cls, v):
        if isinstance(v, dict) and "epoch_ms" in v:
            epoch_ms = v.get("epoch_ms", [])
            series = v.get("series", [])
            dates = _transform_epoch_series_to_by_date(epoch_ms, series)
            return {"dates": dates}
        return v


class SymphonyHoldings(BaseModel):
    """Current holdings of a symphony."""

    model_config = {"populate_by_name": True}

    cash: float
    last_rebalance_on: Optional[str] = None
    liquidated: bool
    net_deposits: float
    shares: Optional[dict] = None
    symphony_id: str


class SymphonyStats(BaseModel):
    """Stats for a symphony in the stats endpoint."""

    model_config = {"populate_by_name": True}

    id: str
    position_id: str
    as_of: Optional[str] = None
    holdings: List[SymphonyHolding] = []
    simple_return: float
    time_weighted_return: float
    net_deposits: float
    last_dollar_change: float
    cash: float
    value: float
    deposit_adjusted_value: float
    annualized_rate_of_return: float
    sharpe_ratio: float
    max_drawdown: float
    last_percent_change: float
    invested_since: str


class SymphonyStatsResponse(BaseModel):
    """Response from getting symphony stats."""

    model_config = {"populate_by_name": True}

    stats: dict = {}


class ActivityHistoryItem(BaseModel):
    """An activity history item for a symphony."""

    model_config = {"populate_by_name": True}

    type: str
    symphony_id: str
    symphony_name: str
    version_id: Optional[str] = None
    at: Optional[str] = None


class ActivityHistoryResponse(BaseModel):
    """Response from getting activity history."""

    model_config = {"populate_by_name": True}

    data: List[ActivityHistoryItem] = []


class DeployHistoryItem(BaseModel):
    """A deploy history item."""

    model_config = {"populate_by_name": True}

    type: str
    symphony_id: str
    symphony_name: str
    version_id: str
    at: Optional[str] = None


class DeployHistoryResponse(BaseModel):
    """Response from getting deploy history."""

    model_config = {"populate_by_name": True}

    deploy_history: List[DeployHistoryItem] = []
