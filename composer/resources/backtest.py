from typing import Dict, Any, Union, Optional, List
from ..models.backtest import (
    BacktestRequest,
    BacktestResult,
    RebalanceRequest,
    RebalanceResult,
    BacktestVersion,
    Broker,
    ApplySubscription,
)
from ..models.common import SymphonyDefinition


class Backtest:
    def __init__(self, http_client):
        self.http_client = http_client

    def run(self, request: Union[BacktestRequest, Dict[str, Any]]) -> BacktestResult:
        """
        Run a generic backtest simulation (v1).

        Args:
            request: BacktestRequest model or dictionary matching the schema.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
            # Backtest with full symphony definition
            result = client.backtest.run(
                BacktestRequest(
                    symphony=SymphonyDefinition(
                        name="My Strategy",
                        rebalance="daily",
                        children=[...]
                    )
                )
            )
        """
        payload = request
        if isinstance(request, BacktestRequest):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            if "symphony" in payload and payload["symphony"]:
                payload["symphony"] = {"raw_value": payload["symphony"]}

        raw_response = self.http_client.post("/api/v1/backtest", json=payload)
        return BacktestResult.model_validate(raw_response)

    def run_v2(
        self,
        symphony: Optional[SymphonyDefinition] = None,
        capital: float = 10000.0,
        abbreviate_days: Optional[int] = None,
        apply_reg_fee: bool = True,
        apply_taf_fee: bool = True,
        apply_subscription: ApplySubscription = ApplySubscription.NONE,
        backtest_version: BacktestVersion = BacktestVersion.V2,
        slippage_percent: float = 0.0001,
        spread_markup: float = 0.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        broker: Broker = Broker.ALPACA_WHITE_LABEL,
        benchmark_symphonies: Optional[List[str]] = None,
        benchmark_tickers: Optional[List[str]] = None,
        sparkgraph_color: Optional[str] = None,
    ) -> BacktestResult:
        """
        Run a generic backtest simulation (v2).

        Args:
            symphony: Symphony definition to backtest (optional).
            capital: Initial capital for the backtest (default: 10000.0).
            abbreviate_days: Number of days to abbreviate the backtest (for testing).
            apply_reg_fee: Whether to apply regulatory fees (SEC fees).
            apply_taf_fee: Whether to apply TAF (Trading Activity Fee).
            apply_subscription: Composer subscription level to simulate (affects fees).
            backtest_version: Backtest engine version to use.
            slippage_percent: Slippage assumption as decimal (0.0001 = 0.01%).
            spread_markup: Bid-ask spread markup as decimal (0.001 = 0.1%).
            start_date: Backtest start date (YYYY-MM-DD). Defaults to earliest available data.
            end_date: Backtest end date (YYYY-MM-DD). Defaults to latest available data.
            broker: Broker to simulate for fee calculations.
            benchmark_symphonies: List of symphony IDs to use as benchmarks.
            benchmark_tickers: List of ticker symbols to use as benchmarks (e.g., ['SPY', 'QQQ']).
            sparkgraph_color: Custom color for performance chart.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
             result = client.backtest.run_v2(symphony=SymphonyDefinition(...))
             print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = {
            "symphony": {"raw_value": symphony.model_dump(by_alias=True, exclude_none=True)}
            if symphony
            else None,
            "capital": capital,
            "abbreviate_days": abbreviate_days,
            "apply_reg_fee": apply_reg_fee,
            "apply_taf_fee": apply_taf_fee,
            "apply_subscription": apply_subscription.value if apply_subscription else None,
            "backtest_version": backtest_version.value if backtest_version else None,
            "slippage_percent": slippage_percent,
            "spread_markup": spread_markup,
            "start_date": start_date,
            "end_date": end_date,
            "broker": broker.value if broker else None,
            "benchmark_symphonies": benchmark_symphonies,
            "benchmark_tickers": benchmark_tickers,
            "sparkgraph_color": sparkgraph_color,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        raw_response = self.http_client.post("/api/v2/backtest", json=payload)
        return BacktestResult.model_validate(raw_response)

    def run_public_v2(
        self,
        symphony: Optional[SymphonyDefinition] = None,
        capital: float = 10000.0,
        abbreviate_days: Optional[int] = None,
        apply_reg_fee: bool = True,
        apply_taf_fee: bool = True,
        apply_subscription: ApplySubscription = ApplySubscription.NONE,
        backtest_version: BacktestVersion = BacktestVersion.V2,
        slippage_percent: float = 0.0001,
        spread_markup: float = 0.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        broker: Broker = Broker.ALPACA_WHITE_LABEL,
        benchmark_symphonies: Optional[List[str]] = None,
        benchmark_tickers: Optional[List[str]] = None,
        sparkgraph_color: Optional[str] = None,
    ) -> BacktestResult:
        """
        Run a public backtest simulation (v2).

        Args:
            symphony: Symphony definition to backtest (optional).
            capital: Initial capital for the backtest (default: 10000.0).
            abbreviate_days: Number of days to abbreviate the backtest (for testing).
            apply_reg_fee: Whether to apply regulatory fees (SEC fees).
            apply_taf_fee: Whether to apply TAF (Trading Activity Fee).
            apply_subscription: Composer subscription level to simulate (affects fees).
            backtest_version: Backtest engine version to use.
            slippage_percent: Slippage assumption as decimal (0.0001 = 0.01%).
            spread_markup: Bid-ask spread markup as decimal (0.001 = 0.1%).
            start_date: Backtest start date (YYYY-MM-DD). Defaults to earliest available data.
            end_date: Backtest end date (YYYY-MM-DD). Defaults to latest available data.
            broker: Broker to simulate for fee calculations.
            benchmark_symphonies: List of symphony IDs to use as benchmarks.
            benchmark_tickers: List of ticker symbols to use as benchmarks (e.g., ['SPY', 'QQQ']).
            sparkgraph_color: Custom color for performance chart.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
             result = client.backtest.run_public_v2(symphony=SymphonyDefinition(...))
             print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = {
            "symphony": {"raw_value": symphony.model_dump(by_alias=True, exclude_none=True)}
            if symphony
            else None,
            "capital": capital,
            "abbreviate_days": abbreviate_days,
            "apply_reg_fee": apply_reg_fee,
            "apply_taf_fee": apply_taf_fee,
            "apply_subscription": apply_subscription.value if apply_subscription else None,
            "backtest_version": backtest_version.value if backtest_version else None,
            "slippage_percent": slippage_percent,
            "spread_markup": spread_markup,
            "start_date": start_date,
            "end_date": end_date,
            "broker": broker.value if broker else None,
            "benchmark_symphonies": benchmark_symphonies,
            "benchmark_tickers": benchmark_tickers,
            "sparkgraph_color": sparkgraph_color,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        raw_response = self.http_client.post("/api/v2/public/backtest", json=payload)
        return BacktestResult.model_validate(raw_response)

    def rebalance(self, request: Union[RebalanceRequest, Dict[str, Any]]) -> RebalanceResult:
        """
        Run a rebalance for specified symphonies.

        Args:
            request: RebalanceRequest model or dictionary matching the schema.

        Returns:
            RebalanceResult: Rebalance result with quotes and run results.

        Example:
             request = RebalanceRequest(
            ...     symphonies={
            ...         "sym-123": SymphonyRebalanceState(cash=10000, shares={})
            ...     }
            ... )
             result = client.backtest.rebalance(request)
             print(result.run_results)
        """
        payload = request
        if isinstance(request, RebalanceRequest):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")

        raw_response = self.http_client.post("/api/v2/rebalance", json=payload)
        return RebalanceResult.model_validate(raw_response)
