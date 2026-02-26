"""Backtest response models (output models)."""

from datetime import date, datetime
from enum import Enum
from typing import Optional, Dict, Any, List, Union

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..common.stats import Stats
from ..common.symphony import SymphonyDefinition
from .symphony import FindAndReplaceOperation, CompressNestedIfsModification


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


class _DateSeriesDict(dict):
    """Dict subclass with .df property for date-indexed series data."""

    def __init__(self, *args, fill_value=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill_value = fill_value

    @property
    def df(self) -> pd.DataFrame:
        """Convert to DataFrame with dates as index and series as columns."""
        if not self:
            return pd.DataFrame()

        sorted_dates = sorted(self.keys())
        all_series = set()
        for series_dict in self.values():
            all_series.update(series_dict.keys())

        data = {series: [] for series in all_series}
        for d in sorted_dates:
            series_dict = self.get(d, {})
            for series in all_series:
                data[series].append(series_dict.get(series, self.fill_value))

        df = pd.DataFrame(data, index=sorted_dates)
        df.index.name = "date"
        return df


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

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Timing and metadata
    last_semantic_update_at: Optional[str] = None
    sparkgraph_url: Optional[str] = None
    first_day: Optional[str] = None
    last_market_day: Optional[str] = None

    # Daily Value Metrics (DVM)
    dvm_capital: Optional[_DateSeriesDict] = None

    # Time-Dependent Value Metrics (TDVM) weights
    tdvm_weights: Optional[_DateSeriesDict] = None

    @field_validator("dvm_capital", mode="before")
    @classmethod
    def transform_dvm_capital(cls, v):
        transformed = _transform_dvm_to_by_date(v)
        if transformed is None:
            return None
        return _DateSeriesDict(transformed)

    @field_validator("tdvm_weights", mode="before")
    @classmethod
    def transform_tdvm_weights(cls, v):
        transformed = _transform_dvm_to_by_date(v)
        if transformed is None:
            return None
        result = _DateSeriesDict(transformed, fill_value=False)
        for date in result:
            for ticker in result[date]:
                result[date][ticker] = bool(result[date][ticker])
        return result

    @field_validator("first_day", mode="before")
    @classmethod
    def transform_first_day(cls, v):
        if v is None:
            return None
        return _epoch_day_to_date_string(v)

    @field_validator("last_market_day", mode="before")
    @classmethod
    def transform_last_market_day(cls, v):
        if v is None:
            return None
        return _epoch_day_to_date_string(v)

    @field_validator("rebalance_days", mode="before")
    @classmethod
    def transform_rebalance_days(cls, v):
        if v is None:
            return None
        return [_epoch_day_to_date_string(d) for d in v]

    # Rebalancing information
    rebalance_days: Optional[List[str]] = None
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
            first = datetime.strptime(self.first_day, "%Y-%m-%d").date()
            last = datetime.strptime(self.last_market_day, "%Y-%m-%d").date()
            parts.append(f"days={(last - first).days}")
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


class ConfigKey(str, Enum):
    """Valid config keys for the configs endpoints."""

    CONSTANTS = "constants"
    DEPOSIT_PRESETS_CONFIG = "deposit_presets_config"
    OPENAI_PROMPT = "openai-prompt"
    OPENAI_CONFIG = "openai_config"


class ConstantsConfig(BaseModel):
    """Config model for the 'constants' config key."""

    model_config = ConfigDict(populate_by_name=True)

    discord_url: str = Field(alias="discord-url")
    referral_bonus: int = Field(alias="referral-bonus")
    referral_bonus_percent: int = Field(alias="referral-bonus-percent")
    suggested_deposits: List[int]


class DepositPresetsConfig(BaseModel):
    """Config model for the 'deposit_presets_config' config key."""

    first_individual: List[int]
    first_ira: List[int]


class OpenAIPromptConfig(BaseModel):
    """Config model for the 'openai-prompt' config key."""

    data: str


class OpenAIConfig(BaseModel):
    """Config model for the 'openai_config' config key."""

    model_config = ConfigDict(populate_by_name=True)

    system_prompt: str = Field(alias="system-prompt")
    crypto_prompt: str = Field(alias="crypto-prompt")
    hybrid_prompt: str = Field(alias="hybrid-prompt")
    crypto_unavailable_prompt: str = Field(alias="crypto-unavailable-prompt")
    temperature: float
    limit: int
    max_free_create_with_ai_requests: int
    suggestions: List[str]
    crypto_suggestions: List[str] = Field(alias="crypto-suggestions")
    hybrid_suggestions: List[str] = Field(alias="hybrid-suggestions")


ConfigType = Union[ConstantsConfig, DepositPresetsConfig, OpenAIPromptConfig, OpenAIConfig]


class ConfigEntry(BaseModel):
    """
    Config entry returned from the configs endpoints.

    Contains the config key, the config data (varies by key), and timestamps.
    """

    config_key: ConfigKey
    config: ConfigType
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigEntry":
        """Create ConfigEntry from dictionary, using config_key to parse the correct config type."""
        config_key_str = data.get("config_key")
        config_data = data.get("config", {})

        config_key = ConfigKey(config_key_str)

        if config_key == ConfigKey.CONSTANTS:
            config = ConstantsConfig.model_validate(config_data)
        elif config_key == ConfigKey.DEPOSIT_PRESETS_CONFIG:
            config = DepositPresetsConfig.model_validate(config_data)
        elif config_key == ConfigKey.OPENAI_PROMPT:
            config = OpenAIPromptConfig.model_validate(config_data)
        elif config_key == ConfigKey.OPENAI_CONFIG:
            config = OpenAIConfig.model_validate(config_data)
        else:
            config = config_data

        return cls(
            config_key=config_key,
            config=config,
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )


Modification = Union[FindAndReplaceOperation, CompressNestedIfsModification]


class ScoreExtendedResponse(BaseModel):
    """
    Response from the score-extended endpoint.

    Contains the symphony score along with suggested modifications.
    """

    score: SymphonyDefinition
    modifications: List[Modification]
