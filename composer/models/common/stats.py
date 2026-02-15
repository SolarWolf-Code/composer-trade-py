"""Common statistics models shared across all API sections."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class RegressionMetrics(BaseModel):
    """Regression metrics for benchmark comparison (alpha, beta, etc.)."""

    alpha: Optional[float] = None
    beta: Optional[float] = None
    r_square: Optional[float] = Field(None, alias="r_square")
    pearson_r: Optional[float] = None


class BenchmarkStats(BaseModel):
    """Statistics for a benchmark comparison."""

    calmar_ratio: Optional[float] = None
    cumulative_return: Optional[float] = None
    max_: Optional[float] = Field(None, alias="max")
    max_drawdown: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    min_: Optional[float] = Field(None, alias="min")
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    size: Optional[int] = None
    standard_deviation: Optional[float] = None
    annualized_rate_of_return: Optional[float] = None
    annualized_turnover: Optional[float] = None
    trailing_one_day_return: Optional[float] = None
    trailing_one_week_return: Optional[float] = None
    trailing_two_week_return: Optional[float] = None
    trailing_one_month_return: Optional[float] = None
    trailing_three_month_return: Optional[float] = None
    trailing_one_year_return: Optional[float] = None
    top_one_day_contribution: Optional[float] = None
    top_five_percent_day_contribution: Optional[float] = None
    top_ten_percent_day_contribution: Optional[float] = None
    herfindahl_index: Optional[float] = None
    win_rate: Optional[float] = None
    tail_ratio: Optional[float] = None
    percent: Optional[RegressionMetrics] = None
    log: Optional[RegressionMetrics] = None

    class Config:
        populate_by_name = True


class Stats(BaseModel):
    """
    Performance statistics for portfolios, backtests, and symphonies.

    Contains all key performance metrics like Sharpe ratio, cumulative return,
    max drawdown, and various trailing returns.
    """

    calmar_ratio: Optional[float] = None
    cumulative_return: Optional[float] = None
    max_: Optional[float] = Field(None, alias="max")
    max_drawdown: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    min_: Optional[float] = Field(None, alias="min")
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    size: Optional[int] = None
    standard_deviation: Optional[float] = None
    annualized_rate_of_return: Optional[float] = None
    annualized_turnover: Optional[float] = None
    trailing_one_day_return: Optional[float] = None
    trailing_one_week_return: Optional[float] = None
    trailing_two_week_return: Optional[float] = None
    trailing_one_month_return: Optional[float] = None
    trailing_three_month_return: Optional[float] = None
    trailing_one_year_return: Optional[float] = None
    top_one_day_contribution: Optional[float] = None
    top_five_percent_day_contribution: Optional[float] = None
    top_ten_percent_day_contribution: Optional[float] = None
    herfindahl_index: Optional[float] = None
    win_rate: Optional[float] = None
    tail_ratio: Optional[float] = None
    benchmarks: Optional[Dict[str, BenchmarkStats]] = None

    class Config:
        populate_by_name = True

    def __repr__(self) -> str:
        parts = []
        if self.sharpe_ratio is not None:
            parts.append(f"sharpe={self.sharpe_ratio:.2f}")
        if self.cumulative_return is not None:
            parts.append(f"cumulative={self.cumulative_return:.2%}")
        if self.max_drawdown is not None:
            parts.append(f"drawdown={self.max_drawdown:.2%}")
        if self.annualized_rate_of_return is not None:
            parts.append(f"ann_return={self.annualized_rate_of_return:.2%}")
        return f"Stats({', '.join(parts)})"

    def __str__(self) -> str:
        return self.__repr__()
