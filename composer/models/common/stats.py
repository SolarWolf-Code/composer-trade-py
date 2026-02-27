"""Common statistics models shared across all API sections."""

from pydantic import BaseModel, Field


class RegressionMetrics(BaseModel):
    """Regression metrics for benchmark comparison (alpha, beta, etc.)."""

    alpha: float | None = None
    beta: float | None = None
    r_square: float | None = Field(None, alias="r_square")
    pearson_r: float | None = None


class BenchmarkStats(BaseModel):
    """Statistics for a benchmark comparison."""

    calmar_ratio: float | None = None
    cumulative_return: float | None = None
    max_: float | None = Field(None, alias="max")
    max_drawdown: float | None = None
    mean: float | None = None
    median: float | None = None
    min_: float | None = Field(None, alias="min")
    skewness: float | None = None
    kurtosis: float | None = None
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    size: int | None = None
    standard_deviation: float | None = None
    annualized_rate_of_return: float | None = None
    annualized_turnover: float | None = None
    trailing_one_day_return: float | None = None
    trailing_one_week_return: float | None = None
    trailing_two_week_return: float | None = None
    trailing_one_month_return: float | None = None
    trailing_three_month_return: float | None = None
    trailing_one_year_return: float | None = None
    top_one_day_contribution: float | None = None
    top_five_percent_day_contribution: float | None = None
    top_ten_percent_day_contribution: float | None = None
    herfindahl_index: float | None = None
    win_rate: float | None = None
    tail_ratio: float | None = None
    percent: RegressionMetrics | None = None
    log: RegressionMetrics | None = None

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True


class Stats(BaseModel):
    """
    Performance statistics for portfolios, backtests, and symphonies.

    Contains all key performance metrics like Sharpe ratio, cumulative return,
    max drawdown, and various trailing returns.
    """

    calmar_ratio: float | None = None
    cumulative_return: float | None = None
    max_: float | None = Field(None, alias="max")
    max_drawdown: float | None = None
    mean: float | None = None
    median: float | None = None
    min_: float | None = Field(None, alias="min")
    skewness: float | None = None
    kurtosis: float | None = None
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    size: int | None = None
    standard_deviation: float | None = None
    annualized_rate_of_return: float | None = None
    annualized_turnover: float | None = None
    trailing_one_day_return: float | None = None
    trailing_one_week_return: float | None = None
    trailing_two_week_return: float | None = None
    trailing_one_month_return: float | None = None
    trailing_three_month_return: float | None = None
    trailing_one_year_return: float | None = None
    top_one_day_contribution: float | None = None
    top_five_percent_day_contribution: float | None = None
    top_ten_percent_day_contribution: float | None = None
    herfindahl_index: float | None = None
    win_rate: float | None = None
    tail_ratio: float | None = None
    benchmarks: dict[str, BenchmarkStats] | None = None

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True

    def __repr__(self) -> str:
        """Return string representation of Stats."""
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
        """Return string representation of Stats."""
        return self.__repr__()
        return self.__repr__()
