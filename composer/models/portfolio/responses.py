"""Portfolio response models."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


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


class TimeSeries(BaseModel):
    """Portfolio value over time."""

    model_config = {"populate_by_name": True}

    epoch_ms: List[int]
    series: List[float]
    deposit_adjusted_series: Optional[List[float]] = None


class PortfolioHistory(BaseModel):
    """Account portfolio history."""

    model_config = {"populate_by_name": True}

    epoch_ms: List[int]
    series: List[float]
