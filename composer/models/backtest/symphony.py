"""Backtest API models - indicators, symphonies, versions, watchlist."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ParameterType(str, Enum):
    """Type of indicator parameter."""

    DOUBLE = "double"
    INT = "int"


class IndicatorParameter(BaseModel):
    """Parameter definition for a technical indicator."""

    key: str
    name: str
    type: ParameterType
    default_value: float = Field(alias="default_value")
    min_value: float = Field(alias="min_value")
    max_value: float = Field(alias="max_value")


class Indicator(BaseModel):
    """
    Technical indicator available for symphony conditions.

    Examples:
        - Moving average of price
        - Relative strength index
        - Standard deviation
    """

    key: str
    composer_code_name: str = Field(alias="composer_code_name")
    name: str
    builder_format_string: str = Field(alias="builder_format_string")
    url: Optional[str] = None
    description: Optional[str] = None
    beta: bool = False
    parameters: List[IndicatorParameter]
    unit: str  # "dollars" or "percent"
    asset_only: bool = Field(alias="asset_only")


class AssetClass(str, Enum):
    """Asset class enum."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class SymphonyMeta(BaseModel):
    """Basic symphony metadata."""

    id: str
    asset_class: AssetClass = Field(default=AssetClass.EQUITIES)
    asset_classes: List[AssetClass]
    name: Optional[str] = None
    color: str
    description: Optional[str] = None
    last_semantic_update_at: str = Field(alias="last_semantic_update_at")
    tags: List[str]
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    is_shared: bool = Field(alias="is_shared")
    rebalance_corridor_width: Optional[float] = Field(
        alias="rebalance_corridor_width", default=None
    )


class SymphonyMetaResponse(BaseModel):
    """Response for getting symphony metadata."""

    symphonies: List[SymphonyMeta]


class SymphonyDetail(BaseModel):
    """Detailed symphony information."""

    symphony_id: int = Field(alias="symphony_id")
    symphony_sid: str = Field(alias="symphony_sid")
    created_at: str = Field(alias="created_at")
    updated_at: str = Field(alias="updated_at")
    asset_class: AssetClass
    asset_classes: List[AssetClass]
    user_id: Optional[int] = Field(alias="user_id", default=None)
    user_sid: Optional[str] = Field(alias="user_sid", default=None)
    community_review_status: Optional[str] = Field(alias="community_review_status", default=None)
    copied_from_symphony_id: Optional[int] = Field(alias="copied_from_symphony_id", default=None)
    copied_from_symphony_sid: Optional[str] = Field(alias="copied_from_symphony_sid", default=None)
    is_discover_symphony: bool = Field(alias="is_discover_symphony")
    is_deleted: bool = Field(alias="is_deleted")
    last_semantic_update_at: str = Field(alias="last_semantic_update_at")
    name: Optional[str] = None
    description: Optional[str] = None
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    rebalance_corridor_width: Optional[float] = Field(
        alias="rebalance_corridor_width", default=None
    )
    is_shared: bool = Field(alias="is_shared")
    is_searchable: bool = Field(alias="is_searchable")
    is_searchable_updated_at: Optional[str] = Field(alias="is_searchable_updated_at", default=None)
    investor_count: Optional[int] = Field(alias="investor_count", default=None)
    watcher_count: Optional[int] = Field(alias="watcher_count", default=None)
    color: str
    hashtag: Optional[str] = None
    tags: List[str]
    sparkgraph_gcs_url: Optional[str] = Field(alias="sparkgraph_gcs_url", default=None)
    last_backtest_first_market_day: Optional[str] = Field(
        alias="last_backtest_first_market_day", default=None
    )
    last_backtest_last_market_day: Optional[str] = Field(
        alias="last_backtest_last_market_day", default=None
    )
    last_backtest_holdings: Optional[Dict[str, float]] = Field(
        alias="last_backtest_holdings", default=None
    )
    last_backtest_value: Optional[float] = Field(alias="last_backtest_value", default=None)
    stats_trailing_one_month_return: Optional[float] = Field(
        alias="stats_trailing_one_month_return", default=None
    )
    stats_trailing_three_month_return: Optional[float] = Field(
        alias="stats_trailing_three_month_return", default=None
    )
    stats_trailing_one_year_return: Optional[float] = Field(
        alias="stats_trailing_one_year_return", default=None
    )
    stats_annualized_rate_of_return: Optional[float] = Field(
        alias="stats_annualized_rate_of_return", default=None
    )
    stats_cumulative_return: Optional[float] = Field(alias="stats_cumulative_return", default=None)
    stats_max_drawdown: Optional[float] = Field(alias="stats_max_drawdown", default=None)
    stats_standard_deviation: Optional[float] = Field(
        alias="stats_standard_deviation", default=None
    )
    stats_min: Optional[float] = Field(alias="stats_min", default=None)
    stats_max: Optional[float] = Field(alias="stats_max", default=None)
    stats_mean: Optional[float] = Field(alias="stats_mean", default=None)
    stats_size: Optional[int] = Field(alias="stats_size", default=None)
    stats_median: Optional[float] = Field(alias="stats_median", default=None)
    stats_sharpe_ratio: Optional[float] = Field(alias="stats_sharpe_ratio", default=None)
    stats_calmar_ratio: Optional[float] = Field(alias="stats_calmar_ratio", default=None)
    stats_oos_spy_beta: Optional[float] = Field(alias="stats_oos_spy_beta", default=None)
    stats_oos_spy_alpha: Optional[float] = Field(alias="stats_oos_spy_alpha", default=None)
    stats_oos_spy_pearson_r: Optional[float] = Field(alias="stats_oos_spy_pearson_r", default=None)
    stats_oos_btcusd_beta: Optional[float] = Field(alias="stats_oos_btcusd_beta", default=None)
    stats_oos_btcusd_alpha: Optional[float] = Field(alias="stats_oos_btcusd_alpha", default=None)
    stats_oos_btcusd_pearson_r: Optional[float] = Field(
        alias="stats_oos_btcusd_pearson_r", default=None
    )
    stats_oos_skewness: Optional[float] = Field(alias="stats_oos_skewness", default=None)
    stats_oos_kurtosis: Optional[float] = Field(alias="stats_oos_kurtosis", default=None)
    stats_oos_sortino_ratio: Optional[float] = Field(alias="stats_oos_sortino_ratio", default=None)
    stats_oos_annualized_turnover: Optional[float] = Field(
        alias="stats_oos_annualized_turnover", default=None
    )
    stats_oos_trailing_one_day_return: Optional[float] = Field(
        alias="stats_oos_trailing_one_day_return", default=None
    )
    stats_oos_trailing_one_week_return: Optional[float] = Field(
        alias="stats_oos_trailing_one_week_return", default=None
    )
    stats_oos_trailing_two_week_return: Optional[float] = Field(
        alias="stats_oos_trailing_two_week_return", default=None
    )
    stats_oos_top_one_day_contribution: Optional[float] = Field(
        alias="stats_oos_top_one_day_contribution", default=None
    )
    stats_oos_top_five_percent_day_contribution: Optional[float] = Field(
        alias="stats_oos_top_five_percent_day_contribution", default=None
    )
    stats_oos_top_ten_percent_day_contribution: Optional[float] = Field(
        alias="stats_oos_top_ten_percent_day_contribution", default=None
    )
    stats_oos_herfindahl_index: Optional[float] = Field(
        alias="stats_oos_herfindahl_index", default=None
    )
    stats_oos_win_rate: Optional[float] = Field(alias="stats_oos_win_rate", default=None)
    stats_oos_tail_ratio: Optional[float] = Field(alias="stats_oos_tail_ratio", default=None)
    youtube_url: Optional[str] = None
    categories: Optional[List[str]] = None
    risk_rating: Optional[str] = None
    risk_rationale: Optional[str] = None
    twitter_handle: Optional[str] = None
    owner_name: Optional[str] = None
    owner_link_url: Optional[str] = None
    owner_link_text: Optional[str] = None
    version_id: int = Field(alias="version_id")
    version_sid: str = Field(alias="version_sid")


class SymphonyVersionInfo(BaseModel):
    """Symphony version information."""

    version_id: str = Field(alias="version_id")
    created_at: str = Field(alias="created_at")


class TickersResponse(BaseModel):
    """Response for symphony tickers endpoint."""

    tickers: List[str]


class AISymphonyDescription(BaseModel):
    """AI-generated description for a symphony."""

    summary: str
    categories: str
    how_it_works: str = Field(alias="how_it_works")
    value_proposition: str = Field(alias="value_proposition")


class UserSymphony(BaseModel):
    """Symphony in user's library."""

    symphony_sid: str = Field(alias="symphony_sid")
    name: Optional[str] = None
    description: Optional[str] = None
    asset_classes: List[AssetClass]
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    rebalance_corridor_width: Optional[float] = Field(
        alias="rebalance_corridor_width", default=None
    )
    sparkgraph_gcs_url: Optional[str] = Field(alias="sparkgraph_gcs_url", default=None)
    color: str
    num_node_asset: int = Field(alias="num_node_asset")
    num_node_filter: int = Field(alias="num_node_filter")
    num_node_group: int = Field(alias="num_node_group")
    num_node_if: int = Field(alias="num_node_if")
    num_node_if_child: int = Field(alias="num_node_if_child")
    num_node_wt_cash_equal: int = Field(alias="num_node_wt_cash_equal")
    num_node_wt_cash_specified: int = Field(alias="num_node_wt_cash_specified")
    num_node_wt_inverse_vol: int = Field(alias="num_node_wt_inverse_vol")
    oos_annualized_rate_of_return: Optional[float] = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: Optional[float] = Field(alias="oos_annualized_turnover", default=None)
    oos_btcusd_alpha: Optional[float] = Field(alias="oos_btcusd_alpha", default=None)
    oos_btcusd_annualized_rate_of_return: Optional[float] = Field(
        alias="oos_btcusd_annualized_rate_of_return", default=None
    )
    oos_btcusd_beta: Optional[float] = Field(alias="oos_btcusd_beta", default=None)
    oos_btcusd_calmar_ratio: Optional[float] = Field(alias="oos_btcusd_calmar_ratio", default=None)
    oos_btcusd_cumulative_return: Optional[float] = Field(
        alias="oos_btcusd_cumulative_return", default=None
    )
    oos_btcusd_max_drawdown: Optional[float] = Field(alias="oos_btcusd_max_drawdown", default=None)
    oos_btcusd_pearson_r: Optional[float] = Field(alias="oos_btcusd_pearson_r", default=None)
    oos_btcusd_r_square: Optional[float] = Field(alias="oos_btcusd_r_square", default=None)
    oos_btcusd_sharpe_ratio: Optional[float] = Field(alias="oos_btcusd_sharpe_ratio", default=None)
    oos_btcusd_standard_deviation: Optional[float] = Field(
        alias="oos_btcusd_standard_deviation", default=None
    )
    oos_btcusd_trailing_one_month_return: Optional[float] = Field(
        alias="oos_btcusd_trailing_one_month_return", default=None
    )
    oos_btcusd_trailing_one_year_return: Optional[float] = Field(
        alias="oos_btcusd_trailing_one_year_return", default=None
    )
    oos_btcusd_trailing_three_month_return: Optional[float] = Field(
        alias="oos_btcusd_trailing_three_month_return", default=None
    )
    oos_calmar_ratio: Optional[float] = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: Optional[float] = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: Optional[float] = Field(alias="oos_herfindahl_index", default=None)
    oos_kurtosis: Optional[float] = Field(alias="oos_kurtosis", default=None)
    oos_max_drawdown: Optional[float] = Field(alias="oos_max_drawdown", default=None)
    oos_num_backtest_days: Optional[int] = Field(alias="oos_num_backtest_days", default=None)
    oos_sharpe_ratio: Optional[float] = Field(alias="oos_sharpe_ratio", default=None)
    oos_skewness: Optional[float] = Field(alias="oos_skewness", default=None)
    oos_sortino_ratio: Optional[float] = Field(alias="oos_sortino_ratio", default=None)
    oos_spy_alpha: Optional[float] = Field(alias="oos_spy_alpha", default=None)
    oos_spy_annualized_rate_of_return: Optional[float] = Field(
        alias="oos_spy_annualized_rate_of_return", default=None
    )
    oos_spy_beta: Optional[float] = Field(alias="oos_spy_beta", default=None)
    oos_spy_calmar_ratio: Optional[float] = Field(alias="oos_spy_calmar_ratio", default=None)
    oos_spy_cumulative_return: Optional[float] = Field(
        alias="oos_spy_cumulative_return", default=None
    )
    oos_spy_max_drawdown: Optional[float] = Field(alias="oos_spy_max_drawdown", default=None)
    oos_spy_pearson_r: Optional[float] = Field(alias="oos_spy_pearson_r", default=None)
    oos_spy_r_square: Optional[float] = Field(alias="oos_spy_r_square", default=None)
    oos_spy_sharpe_ratio: Optional[float] = Field(alias="oos_spy_sharpe_ratio", default=None)
    oos_spy_standard_deviation: Optional[float] = Field(
        alias="oos_spy_standard_deviation", default=None
    )
    oos_spy_trailing_one_month_return: Optional[float] = Field(
        alias="oos_spy_trailing_one_month_return", default=None
    )
    oos_spy_trailing_one_year_return: Optional[float] = Field(
        alias="oos_spy_trailing_one_year_return", default=None
    )
    oos_spy_trailing_three_month_return: Optional[float] = Field(
        alias="oos_spy_trailing_three_month_return", default=None
    )
    oos_standard_deviation: Optional[float] = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: Optional[float] = Field(alias="oos_tail_ratio", default=None)
    oos_top_five_percent_day_contribution: Optional[float] = Field(
        alias="oos_top_five_percent_day_contribution", default=None
    )
    oos_top_one_day_contribution: Optional[float] = Field(
        alias="oos_top_one_day_contribution", default=None
    )
    oos_top_ten_percent_day_contribution: Optional[float] = Field(
        alias="oos_top_ten_percent_day_contribution", default=None
    )
    oos_trailing_one_day_return: Optional[float] = Field(
        alias="oos_trailing_one_day_return", default=None
    )
    oos_trailing_one_month_return: Optional[float] = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_week_return: Optional[float] = Field(
        alias="oos_trailing_one_week_return", default=None
    )
    oos_trailing_one_year_return: Optional[float] = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: Optional[float] = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_trailing_two_week_return: Optional[float] = Field(
        alias="oos_trailing_two_week_return", default=None
    )
    oos_win_rate: Optional[float] = Field(alias="oos_win_rate", default=None)
    ai_description: Optional[AISymphonyDescription] = Field(alias="ai_description", default=None)


class DraftSymphony(BaseModel):
    """Draft symphony with statistics."""

    symphony_sid: str = Field(alias="symphony_sid")
    name: Optional[str] = None
    description: Optional[str] = None
    asset_classes: List[AssetClass]
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    rebalance_corridor_width: Optional[float] = Field(
        alias="rebalance_corridor_width", default=None
    )
    sparkgraph_gcs_url: Optional[str] = Field(alias="sparkgraph_gcs_url", default=None)
    color: Optional[str] = None
    num_node_asset: int = Field(alias="num_node_asset")
    num_node_filter: int = Field(alias="num_node_filter")
    num_node_group: int = Field(alias="num_node_group")
    num_node_if: int = Field(alias="num_node_if")
    num_node_if_child: int = Field(alias="num_node_if_child")
    num_node_wt_cash_equal: int = Field(alias="num_node_wt_cash_equal")
    num_node_wt_cash_specified: int = Field(alias="num_node_wt_cash_specified")
    num_node_wt_inverse_vol: int = Field(alias="num_node_wt_inverse_vol")
    oos_annualized_rate_of_return: Optional[float] = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: Optional[float] = Field(alias="oos_annualized_turnover", default=None)
    oos_calmar_ratio: Optional[float] = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: Optional[float] = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: Optional[float] = Field(alias="oos_herfindahl_index", default=None)
    oos_kurtosis: Optional[float] = Field(alias="oos_kurtosis", default=None)
    oos_max_drawdown: Optional[float] = Field(alias="oos_max_drawdown", default=None)
    oos_num_backtest_days: Optional[int] = Field(alias="oos_num_backtest_days", default=None)
    oos_sharpe_ratio: Optional[float] = Field(alias="oos_sharpe_ratio", default=None)
    oos_skewness: Optional[float] = Field(alias="oos_skewness", default=None)
    oos_sortino_ratio: Optional[float] = Field(alias="oos_sortino_ratio", default=None)
    oos_standard_deviation: Optional[float] = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: Optional[float] = Field(alias="oos_tail_ratio", default=None)
    oos_top_five_percent_day_contribution: Optional[float] = Field(
        alias="oos_top_five_percent_day_contribution", default=None
    )
    oos_top_one_day_contribution: Optional[float] = Field(
        alias="oos_top_one_day_contribution", default=None
    )
    oos_top_ten_percent_day_contribution: Optional[float] = Field(
        alias="oos_top_ten_percent_day_contribution", default=None
    )
    oos_trailing_one_day_return: Optional[float] = Field(
        alias="oos_trailing_one_day_return", default=None
    )
    oos_trailing_one_month_return: Optional[float] = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_week_return: Optional[float] = Field(
        alias="oos_trailing_one_week_return", default=None
    )
    oos_trailing_one_year_return: Optional[float] = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: Optional[float] = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_trailing_two_week_return: Optional[float] = Field(
        alias="oos_trailing_two_week_return", default=None
    )
    oos_win_rate: Optional[float] = Field(alias="oos_win_rate", default=None)
    ai_description: Optional[AISymphonyDescription] = Field(alias="ai_description", default=None)


class WatchlistSymphony(BaseModel):
    """Symphony on user's watchlist."""

    symphony_sid: str = Field(alias="symphony_sid")
    name: Optional[str] = None
    description: Optional[str] = None
    asset_classes: List[AssetClass]
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    rebalance_corridor_width: Optional[float] = Field(
        alias="rebalance_corridor_width", default=None
    )
    sparkgraph_gcs_url: Optional[str] = Field(alias="sparkgraph_gcs_url", default=None)
    color: str
    num_node_asset: int = Field(alias="num_node_asset")
    num_node_filter: int = Field(alias="num_node_filter")
    num_node_group: int = Field(alias="num_node_group")
    num_node_if: int = Field(alias="num_node_if")
    num_node_if_child: int = Field(alias="num_node_if_child")
    num_node_wt_cash_equal: int = Field(alias="num_node_wt_cash_equal")
    num_node_wt_cash_specified: int = Field(alias="num_node_wt_cash_specified")
    num_node_wt_inverse_vol: int = Field(alias="num_node_wt_inverse_vol")
    oos_annualized_rate_of_return: Optional[float] = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: Optional[float] = Field(alias="oos_annualized_turnover", default=None)
    oos_calmar_ratio: Optional[float] = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: Optional[float] = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: Optional[float] = Field(alias="oos_herfindahl_index", default=None)
    oos_max_drawdown: Optional[float] = Field(alias="oos_max_drawdown", default=None)
    oos_sharpe_ratio: Optional[float] = Field(alias="oos_sharpe_ratio", default=None)
    oos_sortino_ratio: Optional[float] = Field(alias="oos_sortino_ratio", default=None)
    oos_standard_deviation: Optional[float] = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: Optional[float] = Field(alias="oos_tail_ratio", default=None)
    oos_trailing_one_month_return: Optional[float] = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_year_return: Optional[float] = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: Optional[float] = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_win_rate: Optional[float] = Field(alias="oos_win_rate", default=None)
    ai_description: Optional[AISymphonyDescription] = Field(alias="ai_description", default=None)


class UserSymphoniesResponse(BaseModel):
    """Response for user's symphonies."""

    symphonies: List[UserSymphony]


class DraftSymphoniesResponse(BaseModel):
    """Response for user's draft symphonies."""

    symphonies: List[DraftSymphony]


class WatchlistResponse(BaseModel):
    """Response for watchlist."""

    watchlist: List[WatchlistSymphony]


class SymphonyTickersResponse(BaseModel):
    """Response for symphony tickers."""

    tickers: List[str]
