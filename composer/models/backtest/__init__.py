"""Backtest models - request and response models for backtest endpoints."""

from .requests import (
    BacktestVersion,
    Broker,
    ApplySubscription,
    SymphonyDefinition,
    BacktestParams,
    BacktestRequest,
    BacktestExistingSymphonyRequest,
)
from .responses import (
    Costs,
    DataWarning,
    LegendEntry,
    BacktestResult,
)
from .symphony import (
    # Enums
    ParameterType,
    AssetClass,
    # Models
    IndicatorParameter,
    Indicator,
    SymphonyMeta,
    SymphonyMetaResponse,
    SymphonyDetail,
    SymphonyVersionInfo,
    TickersResponse,
    AISymphonyDescription,
    UserSymphony,
    DraftSymphony,
    WatchlistSymphony,
    UserSymphoniesResponse,
    DraftSymphoniesResponse,
    WatchlistResponse,
    SymphonyTickersResponse,
)

__all__ = [
    # Enums - Backtest
    "BacktestVersion",
    "Broker",
    "ApplySubscription",
    # Enums - Symphony
    "ParameterType",
    "AssetClass",
    # Symphony models
    "IndicatorParameter",
    "Indicator",
    "SymphonyMeta",
    "SymphonyMetaResponse",
    "SymphonyDetail",
    "SymphonyVersionInfo",
    "TickersResponse",
    "AISymphonyDescription",
    "UserSymphony",
    "DraftSymphony",
    "WatchlistSymphony",
    "UserSymphoniesResponse",
    "DraftSymphoniesResponse",
    "WatchlistResponse",
    "SymphonyTickersResponse",
    # Symphony models (old backtest)
    "SymphonyDefinition",
    # Request models
    "BacktestParams",
    "BacktestRequest",
    "BacktestExistingSymphonyRequest",
    # Response models
    "Costs",
    "DataWarning",
    "LegendEntry",
    "BacktestResult",
]
