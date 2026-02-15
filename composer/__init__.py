"""Composer API Client."""

from .client import ComposerClient
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
    Root,
    SymphonyScore,
    validate_symphony_score,
    # Backtest models
    BacktestVersion,
    Broker,
    ApplySubscription,
    SymphonyDefinition,
    BacktestParams,
    BacktestRequest,
    BacktestExistingSymphonyRequest,
    Costs,
    DataWarning,
    BacktestResult,
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
    "Root",
    "SymphonyScore",
    "validate_symphony_score",
    # Backtest enums
    "BacktestVersion",
    "Broker",
    "ApplySubscription",
    # Backtest models
    "SymphonyDefinition",
    "BacktestParams",
    "BacktestRequest",
    "BacktestExistingSymphonyRequest",
    "Costs",
    "DataWarning",
    "BacktestResult",
    # Backward compatibility
    "BacktestResponse",
]
