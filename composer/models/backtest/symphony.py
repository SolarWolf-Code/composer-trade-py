"""Backtest API models - indicators, symphonies, versions, watchlist."""

from enum import StrEnum

from pydantic import BaseModel, Field


class ParameterType(StrEnum):
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

    Examples
    --------
        - Moving average of price
        - Relative strength index
        - Standard deviation
    """

    key: str
    composer_code_name: str = Field(alias="composer_code_name")
    name: str
    builder_format_string: str = Field(alias="builder_format_string")
    url: str | None = None
    description: str | None = None
    beta: bool = False
    parameters: list[IndicatorParameter]
    unit: str  # "dollars" or "percent"
    asset_only: bool = Field(alias="asset_only")


class AssetClass(StrEnum):
    """Asset class enum."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class SymphonyMeta(BaseModel):
    """Basic symphony metadata."""

    id: str
    asset_class: AssetClass = Field(default=AssetClass.EQUITIES)
    asset_classes: list[AssetClass]
    name: str | None = None
    color: str
    description: str | None = None
    last_semantic_update_at: str = Field(alias="last_semantic_update_at")
    tags: list[str]
    rebalance_frequency: str = Field(alias="rebalance_frequency")
    is_shared: bool = Field(alias="is_shared")
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)


class SymphonyMetaResponse(BaseModel):
    """Response for getting symphony metadata."""

    symphonies: list[SymphonyMeta]


class SymphonyDetail(BaseModel):
    """Detailed symphony information."""

    symphony_id: int | None = Field(alias="symphony_id", default=None)
    id: str | None = Field(alias="id", default=None)
    created_at: str | None = Field(alias="created_at", default=None)
    updated_at: str | None = Field(alias="updated_at", default=None)
    asset_class: AssetClass | None = None
    asset_classes: list[AssetClass] | None = Field(default_factory=list)
    user_id: int | None = Field(alias="user_id", default=None)
    user_sid: str | None = Field(alias="user_sid", default=None)
    community_review_status: str | None = Field(alias="community_review_status", default=None)
    copied_from_symphony_id: int | None = Field(alias="copied_from_symphony_id", default=None)
    copied_from_symphony_sid: str | None = Field(alias="copied_from_symphony_sid", default=None)
    is_discover_symphony: bool | None = Field(alias="is_discover_symphony", default=None)
    is_deleted: bool | None = Field(alias="is_deleted", default=None)
    last_semantic_update_at: str | None = Field(alias="last_semantic_update_at", default=None)
    name: str | None = None
    description: str | None = None
    rebalance_frequency: str | None = Field(alias="rebalance_frequency", default=None)
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)
    is_shared: bool | None = Field(alias="is_shared", default=None)
    is_searchable: bool | None = Field(alias="is_searchable", default=None)
    is_searchable_updated_at: str | None = Field(alias="is_searchable_updated_at", default=None)
    investor_count: int | None = Field(alias="investor_count", default=None)
    watcher_count: int | None = Field(alias="watcher_count", default=None)
    color: str | None = None
    hashtag: str | None = None
    tags: list[str] | None = Field(default_factory=list)
    sparkgraph_gcs_url: str | None = Field(alias="sparkgraph_gcs_url", default=None)
    last_backtest_first_market_day: str | None = Field(
        alias="last_backtest_first_market_day", default=None
    )
    last_backtest_last_market_day: str | None = Field(
        alias="last_backtest_last_market_day", default=None
    )
    last_backtest_holdings: dict[str, float] | None = Field(
        alias="last_backtest_holdings", default=None
    )
    last_backtest_value: float | None = Field(alias="last_backtest_value", default=None)
    stats_trailing_one_month_return: float | None = Field(
        alias="stats_trailing_one_month_return", default=None
    )
    stats_trailing_three_month_return: float | None = Field(
        alias="stats_trailing_three_month_return", default=None
    )
    stats_trailing_one_year_return: float | None = Field(
        alias="stats_trailing_one_year_return", default=None
    )
    stats_annualized_rate_of_return: float | None = Field(
        alias="stats_annualized_rate_of_return", default=None
    )
    stats_cumulative_return: float | None = Field(alias="stats_cumulative_return", default=None)
    stats_max_drawdown: float | None = Field(alias="stats_max_drawdown", default=None)
    stats_standard_deviation: float | None = Field(alias="stats_standard_deviation", default=None)
    stats_min: float | None = Field(alias="stats_min", default=None)
    stats_max: float | None = Field(alias="stats_max", default=None)
    stats_mean: float | None = Field(alias="stats_mean", default=None)
    stats_size: int | None = Field(alias="stats_size", default=None)
    stats_median: float | None = Field(alias="stats_median", default=None)
    stats_sharpe_ratio: float | None = Field(alias="stats_sharpe_ratio", default=None)
    stats_calmar_ratio: float | None = Field(alias="stats_calmar_ratio", default=None)
    stats_oos_spy_beta: float | None = Field(alias="stats_oos_spy_beta", default=None)
    stats_oos_spy_alpha: float | None = Field(alias="stats_oos_spy_alpha", default=None)
    stats_oos_spy_pearson_r: float | None = Field(alias="stats_oos_spy_pearson_r", default=None)
    stats_oos_btcusd_beta: float | None = Field(alias="stats_oos_btcusd_beta", default=None)
    stats_oos_btcusd_alpha: float | None = Field(alias="stats_oos_btcusd_alpha", default=None)
    stats_oos_btcusd_pearson_r: float | None = Field(
        alias="stats_oos_btcusd_pearson_r", default=None
    )
    stats_oos_skewness: float | None = Field(alias="stats_oos_skewness", default=None)
    stats_oos_kurtosis: float | None = Field(alias="stats_oos_kurtosis", default=None)
    stats_oos_sortino_ratio: float | None = Field(alias="stats_oos_sortino_ratio", default=None)
    stats_oos_annualized_turnover: float | None = Field(
        alias="stats_oos_annualized_turnover", default=None
    )
    stats_oos_trailing_one_day_return: float | None = Field(
        alias="stats_oos_trailing_one_day_return", default=None
    )
    stats_oos_trailing_one_week_return: float | None = Field(
        alias="stats_oos_trailing_one_week_return", default=None
    )
    stats_oos_trailing_two_week_return: float | None = Field(
        alias="stats_oos_trailing_two_week_return", default=None
    )
    stats_oos_top_one_day_contribution: float | None = Field(
        alias="stats_oos_top_one_day_contribution", default=None
    )
    stats_oos_top_five_percent_day_contribution: float | None = Field(
        alias="stats_oos_top_five_percent_day_contribution", default=None
    )
    stats_oos_top_ten_percent_day_contribution: float | None = Field(
        alias="stats_oos_top_ten_percent_day_contribution", default=None
    )
    stats_oos_herfindahl_index: float | None = Field(
        alias="stats_oos_herfindahl_index", default=None
    )
    stats_oos_win_rate: float | None = Field(alias="stats_oos_win_rate", default=None)
    stats_oos_tail_ratio: float | None = Field(alias="stats_oos_tail_ratio", default=None)
    youtube_url: str | None = None
    categories: list[str] | None = None
    risk_rating: str | None = None
    risk_rationale: str | None = None
    twitter_handle: str | None = None
    owner_name: str | None = None
    owner_link_url: str | None = None
    owner_link_text: str | None = None
    version_id: int = Field(alias="version_id")
    version_sid: str = Field(alias="version_sid")


class SymphonyVersionInfo(BaseModel):
    """Symphony version information."""

    version_id: str = Field(alias="version_id")
    created_at: str = Field(alias="created_at")


class TickersResponse(BaseModel):
    """Response for symphony tickers endpoint."""

    tickers: list[str]


class AISymphonyDescription(BaseModel):
    """AI-generated description for a symphony."""

    summary: str
    categories: str
    how_it_works: str = Field(alias="how_it_works")
    value_proposition: str = Field(alias="value_proposition")


class UserSymphony(BaseModel):
    """Symphony in user's library."""

    id: str | None = Field(alias="id", default=None)
    name: str | None = None
    description: str | None = None
    asset_classes: list[AssetClass] | None = Field(default_factory=list)
    rebalance_frequency: str | None = Field(alias="rebalance_frequency", default=None)
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)
    sparkgraph_gcs_url: str | None = Field(alias="sparkgraph_gcs_url", default=None)
    color: str | None = None
    num_node_asset: int | None = Field(alias="num_node_asset", default=None)
    num_node_filter: int | None = Field(alias="num_node_filter", default=None)
    num_node_group: int | None = Field(alias="num_node_group", default=None)
    num_node_if: int | None = Field(alias="num_node_if", default=None)
    num_node_if_child: int | None = Field(alias="num_node_if_child", default=None)
    num_node_wt_cash_equal: int | None = Field(alias="num_node_wt_cash_equal", default=None)
    num_node_wt_cash_specified: int | None = Field(alias="num_node_wt_cash_specified", default=None)
    num_node_wt_inverse_vol: int | None = Field(alias="num_node_wt_inverse_vol", default=None)
    oos_annualized_rate_of_return: float | None = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: float | None = Field(alias="oos_annualized_turnover", default=None)
    oos_btcusd_alpha: float | None = Field(alias="oos_btcusd_alpha", default=None)
    oos_btcusd_annualized_rate_of_return: float | None = Field(
        alias="oos_btcusd_annualized_rate_of_return", default=None
    )
    oos_btcusd_beta: float | None = Field(alias="oos_btcusd_beta", default=None)
    oos_btcusd_calmar_ratio: float | None = Field(alias="oos_btcusd_calmar_ratio", default=None)
    oos_btcusd_cumulative_return: float | None = Field(
        alias="oos_btcusd_cumulative_return", default=None
    )
    oos_btcusd_max_drawdown: float | None = Field(alias="oos_btcusd_max_drawdown", default=None)
    oos_btcusd_pearson_r: float | None = Field(alias="oos_btcusd_pearson_r", default=None)
    oos_btcusd_r_square: float | None = Field(alias="oos_btcusd_r_square", default=None)
    oos_btcusd_sharpe_ratio: float | None = Field(alias="oos_btcusd_sharpe_ratio", default=None)
    oos_btcusd_standard_deviation: float | None = Field(
        alias="oos_btcusd_standard_deviation", default=None
    )
    oos_btcusd_trailing_one_month_return: float | None = Field(
        alias="oos_btcusd_trailing_one_month_return", default=None
    )
    oos_btcusd_trailing_one_year_return: float | None = Field(
        alias="oos_btcusd_trailing_one_year_return", default=None
    )
    oos_btcusd_trailing_three_month_return: float | None = Field(
        alias="oos_btcusd_trailing_three_month_return", default=None
    )
    oos_calmar_ratio: float | None = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: float | None = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: float | None = Field(alias="oos_herfindahl_index", default=None)
    oos_kurtosis: float | None = Field(alias="oos_kurtosis", default=None)
    oos_max_drawdown: float | None = Field(alias="oos_max_drawdown", default=None)
    oos_num_backtest_days: int | None = Field(alias="oos_num_backtest_days", default=None)
    oos_sharpe_ratio: float | None = Field(alias="oos_sharpe_ratio", default=None)
    oos_skewness: float | None = Field(alias="oos_skewness", default=None)
    oos_sortino_ratio: float | None = Field(alias="oos_sortino_ratio", default=None)
    oos_spy_alpha: float | None = Field(alias="oos_spy_alpha", default=None)
    oos_spy_annualized_rate_of_return: float | None = Field(
        alias="oos_spy_annualized_rate_of_return", default=None
    )
    oos_spy_beta: float | None = Field(alias="oos_spy_beta", default=None)
    oos_spy_calmar_ratio: float | None = Field(alias="oos_spy_calmar_ratio", default=None)
    oos_spy_cumulative_return: float | None = Field(alias="oos_spy_cumulative_return", default=None)
    oos_spy_max_drawdown: float | None = Field(alias="oos_spy_max_drawdown", default=None)
    oos_spy_pearson_r: float | None = Field(alias="oos_spy_pearson_r", default=None)
    oos_spy_r_square: float | None = Field(alias="oos_spy_r_square", default=None)
    oos_spy_sharpe_ratio: float | None = Field(alias="oos_spy_sharpe_ratio", default=None)
    oos_spy_standard_deviation: float | None = Field(
        alias="oos_spy_standard_deviation", default=None
    )
    oos_spy_trailing_one_month_return: float | None = Field(
        alias="oos_spy_trailing_one_month_return", default=None
    )
    oos_spy_trailing_one_year_return: float | None = Field(
        alias="oos_spy_trailing_one_year_return", default=None
    )
    oos_spy_trailing_three_month_return: float | None = Field(
        alias="oos_spy_trailing_three_month_return", default=None
    )
    oos_standard_deviation: float | None = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: float | None = Field(alias="oos_tail_ratio", default=None)
    oos_top_five_percent_day_contribution: float | None = Field(
        alias="oos_top_five_percent_day_contribution", default=None
    )
    oos_top_one_day_contribution: float | None = Field(
        alias="oos_top_one_day_contribution", default=None
    )
    oos_top_ten_percent_day_contribution: float | None = Field(
        alias="oos_top_ten_percent_day_contribution", default=None
    )
    oos_trailing_one_day_return: float | None = Field(
        alias="oos_trailing_one_day_return", default=None
    )
    oos_trailing_one_month_return: float | None = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_week_return: float | None = Field(
        alias="oos_trailing_one_week_return", default=None
    )
    oos_trailing_one_year_return: float | None = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: float | None = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_trailing_two_week_return: float | None = Field(
        alias="oos_trailing_two_week_return", default=None
    )
    oos_win_rate: float | None = Field(alias="oos_win_rate", default=None)
    ai_description: AISymphonyDescription | None = Field(alias="ai_description", default=None)


class DraftSymphony(BaseModel):
    """Draft symphony with statistics."""

    symphony_sid: str | None = Field(alias="symphony_sid", default=None)
    name: str | None = None
    description: str | None = None
    asset_classes: list[AssetClass] | None = Field(default_factory=list)
    rebalance_frequency: str | None = Field(alias="rebalance_frequency", default=None)
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)
    sparkgraph_gcs_url: str | None = Field(alias="sparkgraph_gcs_url", default=None)
    color: str | None = None
    num_node_asset: int | None = Field(alias="num_node_asset", default=None)
    num_node_filter: int | None = Field(alias="num_node_filter", default=None)
    num_node_group: int | None = Field(alias="num_node_group", default=None)
    num_node_if: int | None = Field(alias="num_node_if", default=None)
    num_node_if_child: int | None = Field(alias="num_node_if_child", default=None)
    num_node_wt_cash_equal: int | None = Field(alias="num_node_wt_cash_equal", default=None)
    num_node_wt_cash_specified: int | None = Field(alias="num_node_wt_cash_specified", default=None)
    num_node_wt_inverse_vol: int | None = Field(alias="num_node_wt_inverse_vol", default=None)
    oos_annualized_rate_of_return: float | None = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: float | None = Field(alias="oos_annualized_turnover", default=None)
    oos_calmar_ratio: float | None = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: float | None = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: float | None = Field(alias="oos_herfindahl_index", default=None)
    oos_kurtosis: float | None = Field(alias="oos_kurtosis", default=None)
    oos_max_drawdown: float | None = Field(alias="oos_max_drawdown", default=None)
    oos_num_backtest_days: int | None = Field(alias="oos_num_backtest_days", default=None)
    oos_sharpe_ratio: float | None = Field(alias="oos_sharpe_ratio", default=None)
    oos_skewness: float | None = Field(alias="oos_skewness", default=None)
    oos_sortino_ratio: float | None = Field(alias="oos_sortino_ratio", default=None)
    oos_standard_deviation: float | None = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: float | None = Field(alias="oos_tail_ratio", default=None)
    oos_top_five_percent_day_contribution: float | None = Field(
        alias="oos_top_five_percent_day_contribution", default=None
    )
    oos_top_one_day_contribution: float | None = Field(
        alias="oos_top_one_day_contribution", default=None
    )
    oos_top_ten_percent_day_contribution: float | None = Field(
        alias="oos_top_ten_percent_day_contribution", default=None
    )
    oos_trailing_one_day_return: float | None = Field(
        alias="oos_trailing_one_day_return", default=None
    )
    oos_trailing_one_month_return: float | None = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_week_return: float | None = Field(
        alias="oos_trailing_one_week_return", default=None
    )
    oos_trailing_one_year_return: float | None = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: float | None = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_trailing_two_week_return: float | None = Field(
        alias="oos_trailing_two_week_return", default=None
    )
    oos_win_rate: float | None = Field(alias="oos_win_rate", default=None)
    ai_description: AISymphonyDescription | None = Field(alias="ai_description", default=None)


class WatchlistSymphony(BaseModel):
    """Symphony on user's watchlist."""

    id: str | None = Field(alias="id", default=None)
    name: str | None = None
    description: str | None = None
    asset_classes: list[AssetClass] | None = Field(default_factory=list)
    rebalance_frequency: str | None = Field(alias="rebalance_frequency", default=None)
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)
    sparkgraph_gcs_url: str | None = Field(alias="sparkgraph_gcs_url", default=None)
    color: str | None = None
    num_node_asset: int | None = Field(alias="num_node_asset", default=None)
    num_node_filter: int | None = Field(alias="num_node_filter", default=None)
    num_node_group: int | None = Field(alias="num_node_group", default=None)
    num_node_if: int | None = Field(alias="num_node_if", default=None)
    num_node_if_child: int | None = Field(alias="num_node_if_child", default=None)
    num_node_wt_cash_equal: int | None = Field(alias="num_node_wt_cash_equal", default=None)
    num_node_wt_cash_specified: int | None = Field(alias="num_node_wt_cash_specified", default=None)
    num_node_wt_inverse_vol: int | None = Field(alias="num_node_wt_inverse_vol", default=None)
    oos_annualized_rate_of_return: float | None = Field(
        alias="oos_annualized_rate_of_return", default=None
    )
    oos_annualized_turnover: float | None = Field(alias="oos_annualized_turnover", default=None)
    oos_calmar_ratio: float | None = Field(alias="oos_calmar_ratio", default=None)
    oos_cumulative_return: float | None = Field(alias="oos_cumulative_return", default=None)
    oos_herfindahl_index: float | None = Field(alias="oos_herfindahl_index", default=None)
    oos_max_drawdown: float | None = Field(alias="oos_max_drawdown", default=None)
    oos_sharpe_ratio: float | None = Field(alias="oos_sharpe_ratio", default=None)
    oos_sortino_ratio: float | None = Field(alias="oos_sortino_ratio", default=None)
    oos_standard_deviation: float | None = Field(alias="oos_standard_deviation", default=None)
    oos_tail_ratio: float | None = Field(alias="oos_tail_ratio", default=None)
    oos_trailing_one_month_return: float | None = Field(
        alias="oos_trailing_one_month_return", default=None
    )
    oos_trailing_one_year_return: float | None = Field(
        alias="oos_trailing_one_year_return", default=None
    )
    oos_trailing_three_month_return: float | None = Field(
        alias="oos_trailing_three_month_return", default=None
    )
    oos_win_rate: float | None = Field(alias="oos_win_rate", default=None)
    ai_description: AISymphonyDescription | None = Field(alias="ai_description", default=None)


class UserSymphoniesResponse(BaseModel):
    """Response for user's symphonies."""

    symphonies: list[UserSymphony]


class DraftSymphoniesResponse(BaseModel):
    """Response for user's draft symphonies."""

    symphonies: list[DraftSymphony]


class WatchlistResponse(BaseModel):
    """Response for watchlist."""

    symphonies: list[WatchlistSymphony] | None = Field(default_factory=list)
    watchlist: list[WatchlistSymphony] | None = Field(default_factory=list)

    def __init__(self, **data):
        if "symphonies" in data and "watchlist" not in data:
            data["watchlist"] = data.pop("symphonies")
        super().__init__(**data)


class SymphonyTickersResponse(BaseModel):
    """Response for symphony tickers."""

    tickers: list[str]


class WatchlistSymphonyItem(BaseModel):
    """Symphony item when adding to watchlist."""

    id: str | None = None
    asset_classes: list[AssetClass] | None = Field(default_factory=list)
    tickers: list[str] | None = Field(default_factory=list)
    name: str | None = None
    color: str | None = None
    description: str | None = None
    last_semantic_update_at: str | None = Field(alias="last_semantic_update_at", default=None)
    tags: list[str] | None = Field(default_factory=list)
    rebalance_frequency: str | None = Field(alias="rebalance_frequency", default=None)
    is_shared: bool | None = Field(alias="is_shared", default=None)
    rebalance_corridor_width: float | None = Field(alias="rebalance_corridor_width", default=None)
    annualized_rate_of_return: float | None = Field(alias="annualized_rate_of_return", default=None)
    simple_return: float | None = Field(alias="simple_return", default=None)
    sharpe_ratio: float | None = Field(alias="sharpe_ratio", default=None)
    calmar_ratio: float | None = Field(alias="calmar_ratio", default=None)
    standard_deviation: float | None = Field(alias="standard_deviation", default=None)
    trailing_one_month_return: float | None = Field(alias="trailing_one_month_return", default=None)
    trailing_three_month_return: float | None = Field(
        alias="trailing_three_month_return", default=None
    )
    max_drawdown: float | None = Field(alias="max_drawdown", default=None)
    last_backtest_holdings: dict[str, float] | None = Field(
        alias="last_backtest_holdings", default=None
    )
    last_backtest_value: float | None = Field(alias="last_backtest_value", default=None)
    owns_symphony: bool | None = Field(alias="owns_symphony", default=None)
    watched_since: str | None = Field(alias="watched_since", default=None)
    created_at: str | None = Field(alias="created_at", default=None)


class ModifySymphonyResponse(BaseModel):
    """Response for modify symphony operation."""

    symphony_id: str = Field(alias="symphony_id")
    version_id: str = Field(alias="version_id")


class FindAndReplaceOperation(BaseModel):
    """Find and replace operation for modifying symphonies."""

    op: str = Field(default="FIND_AND_REPLACE")
    old_ticker: str = Field(alias="old_ticker")
    new_ticker: str = Field(alias="new_ticker")


class CompressNestedIfsModification(BaseModel):
    """Compress nested ifs operation for modifying symphonies."""

    op: str = Field(default="COMPRESS_NESTED_IFS")
    node_id: str | None = Field(
        None,
        description=(
            "If provided, compress only the subtree rooted at this node. "
            "If omitted, compress the entire symphony."
        ),
    )


class BulkModifySymphoniesRequest(BaseModel):
    """Request for bulk modifying user symphonies."""

    op: str = Field(default="FIND_AND_REPLACE")
    user_id: str | None = Field(alias="user_id", default=None)
    old_ticker: str = Field(alias="old_ticker")
    new_ticker: str = Field(alias="new_ticker")


class UpdateSymphonyResponse(BaseModel):
    """Response for updating a symphony."""

    existing_version_id: str = Field(alias="existing_version_id")
    version_id: str = Field(alias="version_id")


class UpdateSymphonyNodesResponse(BaseModel):
    """Response for updating symphony nodes."""

    symphony_id: str = Field(alias="symphony_id")
    version_id: str = Field(alias="version_id")
