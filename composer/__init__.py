"""Composer API Client."""

from . import resources
from .client import ComposerClient
from .http_client import RetryConfig
from .models import (
    ApplySubscription,
    Asset,
    BacktestExistingSymphonyRequest,
    BacktestRequest,
    # Backward compatibility
    BacktestResponse,
    BacktestResult,
    # Backtest models
    BacktestVersion,
    BaseNode,
    BenchmarkStats,
    Broker,
    Costs,
    DataWarning,
    Empty,
    Filter,
    # Common symphony types
    Function,
    Group,
    If,
    IfChildFalse,
    IfChildTrue,
    Quote,
    RebalanceFrequency,
    RebalanceRequest,
    RebalanceResult,
    RecommendedTrade,
    RegressionMetrics,
    # Common stats
    Stats,
    SymphonyDefinition,
    SymphonyRebalanceState,
    SymphonyRunResult,
    SymphonyScore,
    UpdateSymphonyNodesResponse,
    # Symphony response models
    UpdateSymphonyResponse,
    WeightCashEqual,
    WeightCashSpecified,
    WeightInverseVol,
    WeightMap,
    validate_symphony_score,
)

__all__ = [
    # Client
    "ComposerClient",
    "RetryConfig",
    # Resources
    "resources",
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
