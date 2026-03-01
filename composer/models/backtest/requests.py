"""Backtest request models (input models)."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from ..common.symphony import SymphonyDefinition


class BacktestVersion(StrEnum):
    """Backtest version enum."""

    V1 = "v1"
    V2 = "v2"


class Broker(StrEnum):
    """Broker enum."""

    ALPACA_OAUTH = "ALPACA_OAUTH"
    ALPACA_WHITE_LABEL = "ALPACA_WHITE_LABEL"
    APEX_LEGACY = "APEX_LEGACY"
    ALPACA = "alpaca"
    APEX = "apex"


class ApplySubscription(StrEnum):
    """Subscription type enum."""

    NONE = "none"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class BacktestParams(BaseModel):
    """
    Common parameters for all backtest requests.

    These parameters control how the backtest is run including
    capital amount, fees, slippage, and date range.

    All parameters have sensible defaults so you can run a backtest
    with minimal configuration.
    """

    model_config = {"populate_by_name": True}

    capital: float = Field(default=10000.0, description="Initial capital for the backtest")
    abbreviate_days: int | None = Field(
        None, description="Number of days to abbreviate the backtest (for testing)"
    )
    apply_reg_fee: bool = Field(
        default=True, description="Whether to apply regulatory fees (SEC fees)"
    )
    apply_taf_fee: bool = Field(
        default=True, description="Whether to apply TAF (Trading Activity Fee)"
    )
    apply_subscription: ApplySubscription = Field(
        default=ApplySubscription.NONE,
        description="Composer subscription level to simulate (affects fees)",
    )
    backtest_version: BacktestVersion = Field(
        default=BacktestVersion.V2, description="Backtest engine version to use"
    )
    slippage_percent: float = Field(
        default=0.0001, description="Slippage assumption as decimal (0.0001 = 0.01%)"
    )
    spread_markup: float = Field(
        default=0.0, description="Bid-ask spread markup as decimal (0.001 = 0.1%)"
    )
    start_date: str | None = Field(
        None,
        description="Backtest start date (YYYY-MM-DD). Defaults to earliest available data.",
    )
    end_date: str | None = Field(
        None,
        description="Backtest end date (YYYY-MM-DD). Defaults to latest available data.",
    )
    broker: Broker = Field(
        default=Broker.ALPACA_WHITE_LABEL,
        description="Broker to simulate for fee calculations",
    )
    benchmark_symphonies: list[str] | None = Field(
        None, description="List of symphony IDs to use as benchmarks"
    )
    benchmark_tickers: list[str] | None = Field(
        None,
        description="List of ticker symbols to use as benchmarks (e.g., ['SPY', 'QQQ'])",
    )
    sparkgraph_color: str | None = Field(None, description="Custom color for performance chart")


class BacktestRequest(BacktestParams):
    """
    Full backtest request with symphony definition.

    Use this when backtesting a new symphony by providing the full
    symphony definition in the request body.
    """

    symphony: SymphonyDefinition = Field(description="Symphony definition to backtest")


class BacktestExistingSymphonyRequest(BacktestParams):
    """
    Backtest request for an existing saved symphony.

    Use this when backtesting a symphony that has already been saved.
    The symphony_id is provided in the URL path, not the request body.
    """

    pass


class Quote(BaseModel):
    """Quote for a single ticker in rebalance."""

    ticker: str
    trading_halted: bool = False
    open: float
    close: float | None = None
    low: float
    high: float
    volume: int
    bid: dict[str, Any] | None = None
    ask: dict[str, Any] | None = None
    last: dict[str, Any] | None = None
    source: str | None = None
    timestamp: str | None = None


class SymphonyRebalanceState(BaseModel):
    """State of a single symphony for rebalance."""

    last_rebalanced_on: str | None = None
    cash: float
    unsettled_cash: float = 0.0
    shares: dict[str, float]


class RebalanceRequest(BaseModel):
    """
    Request body for the rebalance endpoint.

    Used to run a rebalance for specified symphonies given a starting state.
    """

    dry_run: bool = False
    broker: Broker = Broker.ALPACA_WHITE_LABEL
    adjust_for_dtbp: bool = False
    disable_fractional_trading: bool = False
    fractionability: dict[str, bool] | None = None
    end_date: str | None = None
    quotes: dict[str, Quote] | None = None
    symphonies: dict[str, SymphonyRebalanceState]
