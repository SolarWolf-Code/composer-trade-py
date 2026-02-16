"""Search models."""

from typing import List, Optional, Any, Dict
from enum import Enum
from pydantic import BaseModel, Field


class AssetClass(str, Enum):
    """Asset class for symphony."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"


class SymphonyAIDescription(BaseModel):
    """AI-generated description of a symphony."""

    model_config = {"populate_by_name": True}

    summary: Optional[str] = None
    categories: Optional[str] = None
    how_it_works: Optional[str] = None
    value_proposition: Optional[str] = None


class SearchSymphonyResult(BaseModel):
    """A symphony returned from search."""

    model_config = {"populate_by_name": True}

    symphony_sid: str
    name: Optional[str] = None
    description: Optional[str] = None
    asset_classes: List[AssetClass] = []
    rebalance_frequency: str
    rebalance_corridor_width: Optional[float] = None
    sparkgraph_gcs_url: Optional[str] = None
    color: Optional[str] = None
    num_node_asset: int = 0
    num_node_filter: int = 0
    num_node_group: int = 0
    num_node_if: int = 0
    num_node_if_child: int = 0
    num_node_wt_cash_equal: int = 0
    num_node_wt_cash_specified: int = 0
    num_node_wt_inverse_vol: int = 0
    oos_annualized_rate_of_return: Optional[float] = None
    oos_annualized_turnover: Optional[float] = None
    oos_btcusd_alpha: Optional[float] = None
    oos_btcusd_annualized_rate_of_return: Optional[float] = None
    oos_btcusd_beta: Optional[float] = None
    oos_btcusd_calmar_ratio: Optional[float] = None
    oos_btcusd_cumulative_return: Optional[float] = None
    oos_btcusd_max_drawdown: Optional[float] = None
    oos_btcusd_pearson_r: Optional[float] = None
    oos_btcusd_r_square: Optional[float] = None
    oos_btcusd_sharpe_ratio: Optional[float] = None
    oos_btcusd_standard_deviation: Optional[float] = None
    oos_btcusd_trailing_one_month_return: Optional[float] = None
    oos_btcusd_trailing_one_year_return: Optional[float] = None
    oos_btcusd_trailing_three_month_return: Optional[float] = None
    oos_calmar_ratio: Optional[float] = None
    oos_cumulative_return: Optional[float] = None
    oos_herfindahl_index: Optional[float] = None
    oos_kurtosis: Optional[float] = None
    oos_max_drawdown: Optional[float] = None
    oos_num_backtest_days: Optional[int] = None
    oos_sharpe_ratio: Optional[float] = None
    oos_skewness: Optional[float] = None
    oos_sortino_ratio: Optional[float] = None
    oos_spy_alpha: Optional[float] = None
    oos_spy_annualized_rate_of_return: Optional[float] = None
    oos_spy_beta: Optional[float] = None
    oos_spy_calmar_ratio: Optional[float] = None
    oos_spy_cumulative_return: Optional[float] = None
    oos_spy_max_drawdown: Optional[float] = None
    oos_spy_pearson_r: Optional[float] = None
    oos_spy_r_square: Optional[float] = None
    oos_spy_sharpe_ratio: Optional[float] = None
    oos_spy_standard_deviation: Optional[float] = None
    oos_spy_trailing_one_month_return: Optional[float] = None
    oos_spy_trailing_one_year_return: Optional[float] = None
    oos_spy_trailing_three_month_return: Optional[float] = None
    oos_standard_deviation: Optional[float] = None
    oos_tail_ratio: Optional[float] = None
    oos_top_five_percent_day_contribution: Optional[float] = None
    oos_top_one_day_contribution: Optional[float] = None
    oos_top_ten_percent_day_contribution: Optional[float] = None
    oos_trailing_one_day_return: Optional[float] = None
    oos_trailing_one_month_return: Optional[float] = None
    oos_trailing_one_week_return: Optional[float] = None
    oos_trailing_one_year_return: Optional[float] = None
    oos_trailing_three_month_return: Optional[float] = None
    oos_trailing_two_week_return: Optional[float] = None
    oos_win_rate: Optional[float] = None
    ai_description: Optional[SymphonyAIDescription] = None


class SearchSymphoniesRequest(Dict):
    """Request body for search symphonies endpoint."""

    def __init__(
        self,
        where: Optional[List[Any]] = None,
        order_by: Optional[List[List[str]]] = None,
        offset: int = 0,
    ):
        super().__init__()
        if where is not None:
            self["where"] = where
        if order_by is not None:
            self["order_by"] = order_by
        self["offset"] = offset
