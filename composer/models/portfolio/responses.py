"""Portfolio response models."""

from datetime import UTC, datetime, timedelta
from enum import StrEnum

import pandas as pd
from pydantic import BaseModel, model_validator

EST_OFFSET = timedelta(hours=5)


def _epoch_ms_to_date_string(epoch_ms: int) -> str:
    """Convert epoch milliseconds to ISO date string (assuming EST timestamp from API)."""
    dt = datetime.fromtimestamp(epoch_ms / 1000, tz=UTC) + EST_OFFSET
    return dt.date().isoformat()


def _transform_epoch_series_to_by_date(
    epoch_ms: list[int],
    series: list[float],
    deposit_adjusted_series: list[float] | None = None,
) -> "dict[str, TimeSeriesEntry]":
    """Transform epoch_ms + series to {date: TimeSeriesEntry} format."""
    result: dict[str, TimeSeriesEntry] = {}

    for i, epoch in enumerate(epoch_ms):
        date_str = _epoch_ms_to_date_string(epoch)
        entry: dict[str, float] = {"series": series[i]}
        if deposit_adjusted_series:
            entry["deposit_adjusted_series"] = deposit_adjusted_series[i]
        result[date_str] = TimeSeriesEntry(**entry)

    return dict(sorted(result.items()))


class AssetClass(StrEnum):
    """Asset class types."""

    CRYPTO = "CRYPTO"
    EQUITIES = "EQUITIES"
    OPTIONS = "OPTIONS"


class PositionDirection(StrEnum):
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
    underlying_price: float | None = None
    underlying_price_todays_change: float | None = None
    underlying_price_todays_change_percent: float | None = None


class HoldingAllocation(BaseModel):
    """Allocation details for a holding."""

    model_config = {"populate_by_name": True}

    allocation: float
    amount: float
    value: float
    direction: PositionDirection | None = None


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
    direction: PositionDirection | None = None
    symphonies: list[SymphonyAllocation] = []


class HoldingStats(BaseModel):
    """Detailed statistics for a holding."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: str | None = None
    asset_class: AssetClass | None = None
    options_details: OptionsDetails | None = None
    price: float
    price_todays_change: float
    price_todays_change_percent: float
    direct: HoldingAllocation
    symphony: SymphonyHoldingAllocation
    notional_value: float | None = None
    delta_dollars: float | None = None
    todays_change_percent: float
    todays_change: float
    total_change_percent: float | None = None
    total_change: float | None = None
    cost_basis: float | None = None
    average_cost_basis: float | None = None


class HoldingStatsResponse(BaseModel):
    """Response from getting holding statistics."""

    model_config = {"populate_by_name": True}

    holdings: list[HoldingStats] = []


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
    pending_withdrawals: float | None = None
    pending_net_deposits: float | None = None
    pending_deploys_cash: float


class SymphonyHolding(BaseModel):
    """A holding within a symphony."""

    model_config = {"populate_by_name": True}

    ticker: str
    price: float
    allocation: float
    amount: float
    value: float
    last_percent_change: float | None = None


class SymphonyStatsMeta(BaseModel):
    """Metadata and stats for a symphony."""

    model_config = {"populate_by_name": True}

    id: str
    position_id: str
    as_of: str | None = None
    holdings: list[SymphonyHolding] = []
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
    last_rebalance_on: str | None = None
    last_rebalance_attempted_on: str | None = None
    name: str
    asset_class: AssetClass
    asset_classes: list[AssetClass]
    color: str
    community_review_status: str | None = None
    description: str
    last_semantic_update_at: str
    tags: list[str] = []
    rebalance_frequency: str
    is_shared: bool
    tickers: list[dict] = []
    rebalance_corridor_width: float | None = None
    next_rebalance_on: str | None = None
    may_rebalance_today: bool
    skip_rebalance_today: bool


class SymphonyStatsMetaResponse(BaseModel):
    """Response from getting symphony stats metadata."""

    model_config = {"populate_by_name": True}

    symphonies: list[SymphonyStatsMeta] = []


class TimeSeriesEntry(BaseModel):
    """A single time series data point."""

    series: float
    deposit_adjusted_series: float | None = None


class TimeSeries(BaseModel):
    """Portfolio value over time."""

    model_config = {"populate_by_name": True}

    dates: dict[str, TimeSeriesEntry] = {}

    @model_validator(mode="before")
    @classmethod
    def transform_epoch_to_dates(cls, v):
        """Transform epoch_ms timestamps to date-indexed dict."""
        if isinstance(v, dict) and "epoch_ms" in v:
            epoch_ms = v.get("epoch_ms", [])
            series = v.get("series", [])
            deposit_adjusted_series = v.get("deposit_adjusted_series")
            dates = _transform_epoch_series_to_by_date(epoch_ms, series, deposit_adjusted_series)
            return {"dates": dates}
        return v

    @property
    def df(self) -> pd.DataFrame:
        """Convert dates to DataFrame with dates as index."""
        if not self.dates:
            return pd.DataFrame()

        sorted_dates = sorted(self.dates.keys())
        data = {"series": [], "deposit_adjusted_series": []}
        for d in sorted_dates:
            entry = self.dates[d]
            data["series"].append(entry.series)
            data["deposit_adjusted_series"].append(entry.deposit_adjusted_series)

        df = pd.DataFrame(data, index=sorted_dates)
        df.index.name = "date"
        return df


class PortfolioHistory(BaseModel):
    """Account portfolio history."""

    model_config = {"populate_by_name": True}

    dates: dict[str, TimeSeriesEntry] = {}

    @model_validator(mode="before")
    @classmethod
    def transform_epoch_to_dates(cls, v):
        """Transform epoch_ms timestamps to date-indexed dict."""
        if isinstance(v, dict) and "epoch_ms" in v:
            epoch_ms = v.get("epoch_ms", [])
            series = v.get("series", [])
            dates = _transform_epoch_series_to_by_date(epoch_ms, series)
            return {"dates": dates}
        return v

    @property
    def df(self) -> pd.DataFrame:
        """Convert dates to DataFrame with dates as index."""
        if not self.dates:
            return pd.DataFrame()

        sorted_dates = sorted(self.dates.keys())
        data = {"series": []}
        has_deposit_adjusted = False

        for d in sorted_dates:
            entry = self.dates[d]
            data["series"].append(entry.series)
            if entry.deposit_adjusted_series is not None:
                has_deposit_adjusted = True
                if "deposit_adjusted_series" not in data:
                    data["deposit_adjusted_series"] = []
            if has_deposit_adjusted:
                data["deposit_adjusted_series"].append(entry.deposit_adjusted_series)

        df = pd.DataFrame(data, index=sorted_dates)
        df.index.name = "date"
        return df


class SymphonyHoldings(BaseModel):
    """Current holdings of a symphony."""

    model_config = {"populate_by_name": True}

    cash: float
    last_rebalance_on: str | None = None
    liquidated: bool
    net_deposits: float
    shares: dict | None = None
    symphony_id: str


class SymphonyStats(BaseModel):
    """Stats for a symphony in the stats endpoint."""

    model_config = {"populate_by_name": True}

    id: str
    position_id: str
    as_of: str | None = None
    holdings: list[SymphonyHolding] = []
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
    version_id: str | None = None
    at: str | None = None


class ActivityHistoryResponse(BaseModel):
    """Response from getting activity history."""

    model_config = {"populate_by_name": True}

    data: list[ActivityHistoryItem] = []


class DeployHistoryItem(BaseModel):
    """A deploy history item."""

    model_config = {"populate_by_name": True}

    type: str
    symphony_id: str
    symphony_name: str
    version_id: str
    at: str | None = None


class DeployHistoryResponse(BaseModel):
    """Response from getting deploy history."""

    model_config = {"populate_by_name": True}

    deploy_history: list[DeployHistoryItem] = []
