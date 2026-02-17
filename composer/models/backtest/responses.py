"""Backtest response models (output models)."""

from datetime import date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, field_validator

from ..common.stats import Stats


def _epoch_day_to_date_string(epoch_day: int) -> str:
    """Convert Java LocalDate.ofEpochDay integer to ISO date string."""
    d = date.fromordinal(epoch_day + date(1970, 1, 1).toordinal())
    return d.isoformat()


def _transform_dvm_to_by_date(
    dvm: Optional[Dict[str, Dict[str, float]]],
) -> Optional[Dict[str, Dict[str, float]]]:
    """Transform DVM from {series: {epoch_day: value}} to {date: {series: value}}."""
    if dvm is None:
        return None

    result: Dict[str, Dict[str, float]] = {}

    for series, values in dvm.items():
        for epoch_day_str, value in values.items():
            epoch_day = int(epoch_day_str)
            date_str = _epoch_day_to_date_string(epoch_day)

            if date_str not in result:
                result[date_str] = {}
            result[date_str][series] = value

    return dict(sorted(result.items()))


class Costs(BaseModel):
    """
    Fee and cost breakdown from a backtest.

    Shows all the costs incurred during the backtest including
    regulatory fees, TAF fees, slippage, spread markup, and subscription costs.
    """

    reg_fee: float
    taf_fee: float
    slippage: float
    spread_markup: float
    subscription: float


class DataWarning(BaseModel):
    """Data quality warning for a specific ticker."""

    message: str
    recommended_start_date: Optional[str] = None
    recommended_end_date: Optional[str] = None


class LegendEntry(BaseModel):
    """Legend entry with symphony/ticker name."""

    name: str


class BacktestResult(BaseModel):
    """
    Complete backtest result.

    This is the main response model returned by both backtest endpoints:
    - POST /api/v0.1/backtest (backtest by definition)
    - POST /api/v0.1/symphonies/{symphony-id}/backtest (backtest existing symphony)

    Contains performance metrics, holdings history, costs, and statistics.
    """

    # Timing and metadata
    last_semantic_update_at: Optional[str] = None
    sparkgraph_url: Optional[str] = None
    first_day: Optional[int] = None
    last_market_day: Optional[int] = None

    # Daily Value Metrics (DVM)
    dvm_capital: Optional[Dict[str, Dict[str, float]]] = None

    # Time-Dependent Value Metrics (TDVM) weights
    tdvm_weights: Optional[Dict[str, Dict[str, float]]] = None

    @field_validator("dvm_capital", mode="before")
    @classmethod
    def transform_dvm_capital(cls, v):
        return _transform_dvm_to_by_date(v)

    @field_validator("tdvm_weights", mode="before")
    @classmethod
    def transform_tdvm_weights(cls, v):
        return _transform_dvm_to_by_date(v)

    # Rebalancing information
    rebalance_days: Optional[List[int]] = None
    active_asset_nodes: Optional[Dict[str, float]] = None

    # Costs breakdown
    costs: Optional[Costs] = None

    # Final state
    last_market_days_value: Optional[float] = None
    last_market_days_holdings: Optional[Dict[str, float]] = None

    # Legend and warnings
    legend: Optional[Dict[str, LegendEntry]] = None
    data_warnings: Optional[Dict[str, List[DataWarning]]] = None
    benchmark_errors: Optional[List[str]] = None

    # Performance statistics
    stats: Optional[Stats] = None

    def __repr__(self) -> str:
        parts = []
        if self.stats:
            parts.append(f"stats={self.stats}")
        if self.last_market_days_value is not None:
            parts.append(f"final_value={self.last_market_days_value:,.2f}")
        if self.first_day is not None and self.last_market_day is not None:
            parts.append(f"days={self.last_market_day - self.first_day}")
        return f"BacktestResult({', '.join(parts)})"

    def __str__(self) -> str:
        return self.__repr__()


class RecommendedTrade(BaseModel):
    """Recommended trade from rebalance."""

    ticker: str
    action: str
    quantity: float
    estimated_price: Optional[float] = None
    estimated_value: Optional[float] = None


class SymphonyRunResult(BaseModel):
    """Result of running a single symphony during rebalance."""

    next_rebalanced_after: Optional[str] = None
    rebalanced: bool = False
    active_asset_nodes: Optional[Dict[str, float]] = None
    recommended_trades: Optional[List[RecommendedTrade]] = None


class RebalanceResult(BaseModel):
    """
    Result from a rebalance request.

    Contains quotes, fractionability info, and run results for each symphony.
    """

    quotes: Optional[Dict[str, Any]] = None
    fractionability: Optional[Dict[str, bool]] = None
    adjusted_for_dtbp: bool = False
    run_results: Optional[Dict[str, SymphonyRunResult]] = None
