"""Backtest request models (input models)."""

from enum import Enum
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, model_validator

from ..common.symphony import Root as SymphonyScoreRoot


class BacktestVersion(str, Enum):
    """Backtest version enum."""

    V1 = "v1"
    V2 = "v2"


class Broker(str, Enum):
    """Broker enum."""

    ALPACA_OAUTH = "ALPACA_OAUTH"
    ALPACA_WHITE_LABEL = "ALPACA_WHITE_LABEL"
    APEX_LEGACY = "APEX_LEGACY"
    ALPACA = "alpaca"
    APEX = "apex"


class ApplySubscription(str, Enum):
    """Subscription type enum."""

    NONE = "none"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SymphonyDefinition(BaseModel):
    """
    Wrapper for symphony score definition.

    Can be provided either as:
    1. raw_value: Full symphony object as Root model
    2. encoded_value + encoding_type: Transit-encoded string
    """

    model_config = {"populate_by_name": True}

    raw_value: Optional[SymphonyScoreRoot] = Field(
        None, description="Full symphony definition as structured object"
    )
    encoded_value: Optional[str] = Field(None, description="Transit-encoded symphony string")
    encoding_type: Optional[Literal["transit_json"]] = Field(
        None,
        description="Encoding format (must be 'transit_json' if using encoded_value)",
    )

    @model_validator(mode="after")
    def validate_symphony_definition(self):
        """Ensure exactly one of raw_value or encoded_value is provided."""
        has_raw = self.raw_value is not None
        has_encoded = self.encoded_value is not None

        if not has_raw and not has_encoded:
            raise ValueError("Must provide either raw_value or encoded_value")
        if has_raw and has_encoded:
            raise ValueError("Cannot provide both raw_value and encoded_value")
        if has_encoded and self.encoding_type != "transit_json":
            raise ValueError('encoding_type must be "transit_json" when using encoded_value')

        return self


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
    abbreviate_days: Optional[int] = Field(
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
    start_date: Optional[str] = Field(
        None,
        description="Backtest start date (YYYY-MM-DD). Defaults to earliest available data.",
    )
    end_date: Optional[str] = Field(
        None,
        description="Backtest end date (YYYY-MM-DD). Defaults to latest available data.",
    )
    broker: Broker = Field(
        default=Broker.ALPACA_WHITE_LABEL,
        description="Broker to simulate for fee calculations",
    )
    benchmark_symphonies: Optional[List[str]] = Field(
        None, description="List of symphony IDs to use as benchmarks"
    )
    benchmark_tickers: Optional[List[str]] = Field(
        None,
        description="List of ticker symbols to use as benchmarks (e.g., ['SPY', 'QQQ'])",
    )
    sparkgraph_color: Optional[str] = Field(None, description="Custom color for performance chart")


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
    close: Optional[float] = None
    low: float
    high: float
    volume: int
    bid: Optional[Dict[str, Any]] = None
    ask: Optional[Dict[str, Any]] = None
    last: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    timestamp: Optional[str] = None


class SymphonyRebalanceState(BaseModel):
    """State of a single symphony for rebalance."""

    last_rebalanced_on: Optional[str] = None
    cash: float
    unsettled_cash: float = 0.0
    shares: Dict[str, float]


class RebalanceRequest(BaseModel):
    """
    Request body for the rebalance endpoint.

    Used to run a rebalance for specified symphonies given a starting state.
    """

    dry_run: bool = False
    broker: Broker = Broker.ALPACA_WHITE_LABEL
    adjust_for_dtbp: bool = False
    disable_fractional_trading: bool = False
    fractionability: Optional[Dict[str, bool]] = None
    end_date: Optional[str] = None
    quotes: Optional[Dict[str, Quote]] = None
    symphonies: Dict[str, SymphonyRebalanceState]
