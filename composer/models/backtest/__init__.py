"""Backtest models - request and response models for backtest endpoints."""

from .requests import (
    BacktestVersion,
    Broker,
    ApplySubscription,
    SymphonyDefinition,
    BacktestRequest,
    BacktestExistingSymphonyRequest,
    Quote,
    SymphonyRebalanceState,
    RebalanceRequest,
)
from .responses import (
    Costs,
    DataWarning,
    LegendEntry,
    BacktestResult,
    RecommendedTrade,
    SymphonyRunResult,
    RebalanceResult,
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
    WatchlistSymphonyItem,
    UserSymphoniesResponse,
    DraftSymphoniesResponse,
    WatchlistResponse,
    SymphonyTickersResponse,
    ModifySymphonyResponse,
    FindAndReplaceOperation,
    BulkModifySymphoniesRequest,
    UpdateSymphonyResponse,
    UpdateSymphonyNodesResponse,
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
    "WatchlistSymphonyItem",
    "UserSymphoniesResponse",
    "DraftSymphoniesResponse",
    "WatchlistResponse",
    "SymphonyTickersResponse",
    "ModifySymphonyResponse",
    "FindAndReplaceOperation",
    "BulkModifySymphoniesRequest",
    "UpdateSymphonyResponse",
    "UpdateSymphonyNodesResponse",
    # Symphony models (old backtest)
    "SymphonyDefinition",
    # Request models
    "BacktestRequest",
    "BacktestExistingSymphonyRequest",
    "Quote",
    "SymphonyRebalanceState",
    "RebalanceRequest",
    # Response models
    "Costs",
    "DataWarning",
    "LegendEntry",
    "BacktestResult",
    "RecommendedTrade",
    "SymphonyRunResult",
    "RebalanceResult",
]
