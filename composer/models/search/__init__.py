"""Search models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel


class AssetClass(StrEnum):
    """Asset class for symphony."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class SymphonyAIDescription(BaseModel):
    """AI-generated description of a symphony."""

    model_config = {"populate_by_name": True}

    summary: str | None = None
    categories: str | None = None
    how_it_works: str | None = None
    value_proposition: str | None = None


class SearchSymphonyResult(BaseModel):
    """A symphony returned from search."""

    model_config = {"populate_by_name": True}

    symphony_sid: str
    name: str | None = None
    description: str | None = None
    asset_classes: list[AssetClass] = []
    rebalance_frequency: str
    rebalance_corridor_width: float | None = None
    sparkgraph_gcs_url: str | None = None
    color: str | None = None
    num_node_asset: int = 0
    num_node_filter: int = 0
    num_node_group: int = 0
    num_node_if: int = 0
    num_node_if_child: int = 0
    num_node_wt_cash_equal: int = 0
    num_node_wt_cash_specified: int = 0
    num_node_wt_inverse_vol: int = 0
    oos_annualized_rate_of_return: float | None = None
    oos_annualized_turnover: float | None = None
    oos_btcusd_alpha: float | None = None
    oos_btcusd_annualized_rate_of_return: float | None = None
    oos_btcusd_beta: float | None = None
    oos_btcusd_calmar_ratio: float | None = None
    oos_btcusd_cumulative_return: float | None = None
    oos_btcusd_max_drawdown: float | None = None
    oos_btcusd_pearson_r: float | None = None
    oos_btcusd_r_square: float | None = None
    oos_btcusd_sharpe_ratio: float | None = None
    oos_btcusd_standard_deviation: float | None = None
    oos_btcusd_trailing_one_month_return: float | None = None
    oos_btcusd_trailing_one_year_return: float | None = None
    oos_btcusd_trailing_three_month_return: float | None = None
    oos_calmar_ratio: float | None = None
    oos_cumulative_return: float | None = None
    oos_herfindahl_index: float | None = None
    oos_kurtosis: float | None = None
    oos_max_drawdown: float | None = None
    oos_num_backtest_days: int | None = None
    oos_sharpe_ratio: float | None = None
    oos_skewness: float | None = None
    oos_sortino_ratio: float | None = None
    oos_spy_alpha: float | None = None
    oos_spy_annualized_rate_of_return: float | None = None
    oos_spy_beta: float | None = None
    oos_spy_calmar_ratio: float | None = None
    oos_spy_cumulative_return: float | None = None
    oos_spy_max_drawdown: float | None = None
    oos_spy_pearson_r: float | None = None
    oos_spy_r_square: float | None = None
    oos_spy_sharpe_ratio: float | None = None
    oos_spy_standard_deviation: float | None = None
    oos_spy_trailing_one_month_return: float | None = None
    oos_spy_trailing_one_year_return: float | None = None
    oos_spy_trailing_three_month_return: float | None = None
    oos_standard_deviation: float | None = None
    oos_tail_ratio: float | None = None
    oos_top_five_percent_day_contribution: float | None = None
    oos_top_one_day_contribution: float | None = None
    oos_top_ten_percent_day_contribution: float | None = None
    oos_trailing_one_day_return: float | None = None
    oos_trailing_one_month_return: float | None = None
    oos_trailing_one_week_return: float | None = None
    oos_trailing_one_year_return: float | None = None
    oos_trailing_three_month_return: float | None = None
    oos_trailing_two_week_return: float | None = None
    oos_win_rate: float | None = None
    ai_description: SymphonyAIDescription | None = None


class SearchSymphoniesRequest(dict):
    """Request body for search symphonies endpoint."""

    def __init__(
        self,
        where: list[Any] | None = None,
        order_by: list[list[str]] | None = None,
        offset: int = 0,
    ):
        super().__init__()
        if where is not None:
            self["where"] = where
        if order_by is not None:
            self["order_by"] = order_by
        self["offset"] = offset
