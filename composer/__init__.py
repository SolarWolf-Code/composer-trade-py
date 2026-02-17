"""Composer API Client."""

from .client import ComposerClient
from . import resources
from .models import (
    # Common stats
    Stats,
    BenchmarkStats,
    RegressionMetrics,
    # Common symphony types
    Function,
    RebalanceFrequency,
    WeightMap,
    BaseNode,
    Asset,
    Empty,
    If,
    IfChildTrue,
    IfChildFalse,
    Filter,
    WeightInverseVol,
    Group,
    WeightCashEqual,
    WeightCashSpecified,
    SymphonyScore,
    SymphonyDefinition,
    validate_symphony_score,
    # Backtest models
    BacktestVersion,
    Broker,
    ApplySubscription,
    SymphonyDefinition,
    BacktestRequest,
    BacktestExistingSymphonyRequest,
    Quote,
    SymphonyRebalanceState,
    RebalanceRequest,
    Costs,
    DataWarning,
    BacktestResult,
    RecommendedTrade,
    SymphonyRunResult,
    RebalanceResult,
    # Symphony response models
    UpdateSymphonyResponse,
    UpdateSymphonyNodesResponse,
    # Backward compatibility
    BacktestResponse,
)

__all__ = [
    # Client
    "ComposerClient",
    # Common stats
    "Stats",
    "BenchmarkStats",
    "RegressionMetrics",
    # Symphony types
    "Function",
    "RebalanceFrequency",
    "WeightMap",
    "BaseNode",
    "Asset",
    "Empty",
    "If",
    "IfChildTrue",
    "IfChildFalse",
    "Filter",
    "WeightInverseVol",
    "Group",
    "WeightCashEqual",
    "WeightCashSpecified",
    "SymphonyScore",
    "SymphonyDefinition",
    "validate_symphony_score",
    # Backtest enums
    "BacktestVersion",
    "Broker",
    "ApplySubscription",
    # Backtest models
    "SymphonyDefinition",
    "BacktestRequest",
    "BacktestExistingSymphonyRequest",
    "Quote",
    "SymphonyRebalanceState",
    "RebalanceRequest",
    "Costs",
    "DataWarning",
    "BacktestResult",
    "RecommendedTrade",
    "SymphonyRunResult",
    "RebalanceResult",
    # Symphony response models
    "UpdateSymphonyResponse",
    "UpdateSymphonyNodesResponse",
    # Backward compatibility
    "BacktestResponse",
]
