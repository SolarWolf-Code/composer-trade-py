"""Backtest response models (output models)."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from ..common.stats import Stats


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
