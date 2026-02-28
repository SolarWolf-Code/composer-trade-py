"""Backtest response models (output models)."""

from datetime import date, datetime
from enum import StrEnum
from typing import Any

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..common.stats import Stats
from ..common.symphony import SymphonyDefinition
from .symphony import CompressNestedIfsModification, FindAndReplaceOperation


def _epoch_day_to_date_string(epoch_day: int) -> str:
    """Convert Java LocalDate.ofEpochDay integer to ISO date string."""
    d = date.fromordinal(epoch_day + date(1970, 1, 1).toordinal())
    return d.isoformat()


def _transform_dvm_to_by_date(
    dvm: dict[str, dict[str, float]] | None,
) -> dict[str, dict[str, float]] | None:
    """Transform DVM from {series: {epoch_day: value}} to {date: {series: value}}."""
    if dvm is None:
        return None

    result: dict[str, dict[str, float]] = {}

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
    recommended_start_date: str | None = None
    recommended_end_date: str | None = None


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
    last_semantic_update_at: str | None = None
    sparkgraph_url: str | None = None
    first_day: str | None = None
    last_market_day: str | None = None

    # Daily Value Metrics (DVM)
    dvm_capital: _DateSeriesDict | None = None

    # Time-Dependent Value Metrics (TDVM) weights
    tdvm_weights: _DateSeriesDict | None = None

    @field_validator("dvm_capital", mode="before")
    @classmethod
    def transform_dvm_capital(cls, v):
        """Transform dvm_capital field to date-indexed dict."""
        transformed = _transform_dvm_to_by_date(v)
        if transformed is None:
            return None
        return _DateSeriesDict(transformed)

    @field_validator("tdvm_weights", mode="before")
    @classmethod
    def transform_tdvm_weights(cls, v):
        """Transform tdvm_weights field to date-indexed dict."""
        transformed = _transform_dvm_to_by_date(v)
        if transformed is None:
            return None
        result = _DateSeriesDict(transformed, fill_value=False)
        for d in result:
            for ticker in result[d]:
                result[d][ticker] = bool(result[d][ticker])
        return result

    @field_validator("first_day", mode="before")
    @classmethod
    def transform_first_day(cls, v):
        """Transform first_day from epoch to date string."""
        if v is None:
            return None
        return _epoch_day_to_date_string(v)

    @field_validator("last_market_day", mode="before")
    @classmethod
    def transform_last_market_day(cls, v):
        """Transform last_market_day from epoch to date string."""
        if v is None:
            return None
        return _epoch_day_to_date_string(v)

    @field_validator("rebalance_days", mode="before")
    @classmethod
    def transform_rebalance_days(cls, v):
        """Transform rebalance_days from epochs to date strings."""
        if v is None:
            return None
        return [_epoch_day_to_date_string(d) for d in v]

    # Rebalancing information
    rebalance_days: list[str] | None = None
    active_asset_nodes: dict[str, float] | None = None

    # Costs breakdown
    costs: Costs | None = None

    # Final state
    last_market_days_value: float | None = None
    last_market_days_holdings: dict[str, float] | None = None

    # Legend and warnings
    legend: dict[str, LegendEntry] | None = None
    data_warnings: dict[str, list[DataWarning]] | None = None
    benchmark_errors: list[str] | None = None

    # Performance statistics
    stats: Stats | None = None

    def __repr__(self) -> str:
        """Return string representation of BacktestResult."""
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
        """Return string representation of BacktestResult."""
        return self.__repr__()


class RecommendedTrade(BaseModel):
    """Recommended trade from rebalance."""

    ticker: str
    action: str
    quantity: float
    estimated_price: float | None = None
    estimated_value: float | None = None


class SymphonyRunResult(BaseModel):
    """Result of running a single symphony during rebalance."""

    next_rebalanced_after: str | None = None
    rebalanced: bool = False
    active_asset_nodes: dict[str, float] | None = None
    recommended_trades: list[RecommendedTrade] | None = None


class RebalanceResult(BaseModel):
    """
    Result from a rebalance request.

    Contains quotes, fractionability info, and run results for each symphony.
    """

    quotes: dict[str, Any] | None = None
    fractionability: dict[str, bool] | None = None
    adjusted_for_dtbp: bool = False
    run_results: dict[str, SymphonyRunResult] | None = None


class ConfigKey(StrEnum):
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
    suggested_deposits: list[int]


class DepositPresetsConfig(BaseModel):
    """Config model for the 'deposit_presets_config' config key."""

    first_individual: list[int]
    first_ira: list[int]


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
    suggestions: list[str]
    crypto_suggestions: list[str] = Field(alias="crypto-suggestions")
    hybrid_suggestions: list[str] = Field(alias="hybrid-suggestions")


ConfigType = ConstantsConfig | DepositPresetsConfig | OpenAIPromptConfig | OpenAIConfig


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
    def from_dict(cls, data: dict[str, Any]) -> "ConfigEntry":
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


Modification = FindAndReplaceOperation | CompressNestedIfsModification


class ScoreExtendedResponse(BaseModel):
    """
    Response from the score-extended endpoint.

    Contains the symphony score along with suggested modifications.
    """

    score: SymphonyDefinition
    modifications: list[Modification]
