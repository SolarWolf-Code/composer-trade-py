"""Composer API models organized by endpoint sections."""

# Common models (shared across all sections)
from .common import (
    Stats,
    BenchmarkStats,
    RegressionMetrics,
    # Symphony types
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
)

# Accounts section
from .accounts import (
    AssetClass,
    DirectTradableAssetClasses,
    Account,
    OptionsDetails,
    Holding,
    InvestorDocument,
    InvestorDocumentCategory,
    AccountsListResponse,
)

# Portfolio section
from .portfolio import (
    PositionDirection,
    HoldingAllocation,
    SymphonyAllocation,
    SymphonyHoldingAllocation,
    HoldingStats,
    HoldingStatsResponse,
    TotalStats,
    SymphonyHolding,
    SymphonyStatsMeta,
    SymphonyStatsMetaResponse,
    TimeSeries,
    PortfolioHistory,
)

# Reports section
from .reports import ReportType

# Search section
from .search import (
    AssetClass as SearchAssetClass,
    SymphonyAIDescription,
    SearchSymphonyResult,
    SearchSymphoniesRequest,
)

# Symphony section
from .symphony import (
    AssetClass,
    BenchmarkType,
    Benchmark,
    CreateSymphonyRequest,
    CreateSymphonyResponse,
    CopySymphonyResponse,
    UpdateSymphonyResponse,
    UpdateSymphonyNodesResponse,
    SymphonyVersion,
)

# Trading section
from .trading import (
    OrderStatus,
    OrderSide,
    OrderType,
    TimeInForce,
    PositionIntent,
    AssetClass as TradingAssetClass,
    OrderSource,
    OptionsDetails,
    OrderRequest,
    CreateOrderRequest,
    CreateOrderResponse,
    ListOrdersResponse,
)

# Market Data section
from .market_data import (
    ContractType,
    PayoffStatus,
    OptionSortBy,
    SortOrder,
    OptionGreeks,
    QuotePrice,
    OptionDayData,
    OptionContractDetails,
    OptionContract,
    OptionsChainResponse,
    OptionsContractResponse,
    OptionsOverview,
)

# Dry Run section
from .dry_run import (
    TradeSide,
    RecommendedTrade,
    PreviewRecommendedTrade,
    DryRunResult,
    TradePreviewResult,
    AccountDryRunResult,
    DryRunRequest,
    TradePreviewRequest,
)

# Backtest section
from .backtest import (
    # Enums
    BacktestVersion,
    Broker,
    ApplySubscription,
    ParameterType,
    AssetClass as BacktestAssetClass,
    # Symphony models
    SymphonyDefinition,
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
    # Request models
    BacktestParams,
    BacktestRequest,
    BacktestExistingSymphonyRequest,
    Quote,
    SymphonyRebalanceState,
    RebalanceRequest,
    # Response models
    Costs,
    DataWarning,
    LegendEntry,
    BacktestResult,
    RecommendedTrade,
    SymphonyRunResult,
    RebalanceResult,
)

# For backward compatibility, also export old model names
# These are deprecated and will be removed in a future version
BacktestResponse = BacktestResult

__all__ = [
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
    # Accounts
    "AssetClass",
    "DirectTradableAssetClasses",
    "Account",
    "OptionsDetails",
    "Holding",
    "InvestorDocument",
    "InvestorDocumentCategory",
    "AccountsListResponse",
    # Portfolio
    "PositionDirection",
    "HoldingAllocation",
    "SymphonyAllocation",
    "SymphonyHoldingAllocation",
    "HoldingStats",
    "HoldingStatsResponse",
    "TotalStats",
    "SymphonyHolding",
    "SymphonyStatsMeta",
    "SymphonyStatsMetaResponse",
    "TimeSeries",
    "PortfolioHistory",
    # Reports
    "ReportType",
    # Search
    "SymphonyAIDescription",
    "SearchSymphonyResult",
    "SearchSymphoniesRequest",
    # Symphony
    "AssetClass",
    "BenchmarkType",
    "Benchmark",
    "CreateSymphonyRequest",
    "CreateSymphonyResponse",
    "CopySymphonyRequest",
    "CopySymphonyResponse",
    "UpdateSymphonyResponse",
    "UpdateSymphonyNodesResponse",
    "SymphonyVersion",
    # Trading
    "OrderStatus",
    "OrderSide",
    "OrderType",
    "TimeInForce",
    "PositionIntent",
    "TradingAssetClass",
    "OrderSource",
    "OptionsDetails",
    "OrderRequest",
    "CreateOrderRequest",
    "CreateOrderResponse",
    "ListOrdersResponse",
    # Market Data
    "ContractType",
    "PayoffStatus",
    "OptionSortBy",
    "SortOrder",
    "OptionGreeks",
    "QuotePrice",
    "OptionDayData",
    "OptionContractDetails",
    "OptionContract",
    "OptionsChainResponse",
    "OptionsContractResponse",
    "OptionsOverview",
    # Dry Run
    "TradeSide",
    "RecommendedTrade",
    "PreviewRecommendedTrade",
    "DryRunResult",
    "TradePreviewResult",
    "AccountDryRunResult",
    "DryRunRequest",
    "TradePreviewRequest",
    # Backtest enums
    "BacktestVersion",
    "Broker",
    "ApplySubscription",
    "ParameterType",
    "BacktestAssetClass",
    # Backtest symphony models
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
    # Backtest models
    "SymphonyDefinition",
    "BacktestParams",
    "BacktestRequest",
    "BacktestExistingSymphonyRequest",
    "Quote",
    "SymphonyRebalanceState",
    "RebalanceRequest",
    "Costs",
    "DataWarning",
    "LegendEntry",
    "BacktestResult",
    "RecommendedTrade",
    "SymphonyRunResult",
    "RebalanceResult",
    # Backward compatibility
    "BacktestResponse",
]
