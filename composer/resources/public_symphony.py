"""Public Symphony resource - public endpoints for accessing symphony data."""

from typing import List, Optional, Dict, Any, Union
from ..http_client import HTTPClient
from ..models.backtest import (
    Indicator,
    SymphonyMeta,
    SymphonyMetaResponse,
    SymphonyDetail,
    SymphonyVersionInfo,
    TickersResponse,
    BacktestResult,
    BacktestVersion,
    Broker,
    ApplySubscription,
)
from ..models.common import SymphonyDefinition


class PublicSymphony:
    """
    Public symphony endpoints (no authentication required).

    These endpoints provide read-only access to publicly shared symphonies
    and technical indicators.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def get_indicators(self) -> List[Indicator]:
        """
        Get a list of all available technical indicators.

        Returns a list of indicators that can be used in symphony conditions,
        including moving averages, RSI, standard deviation, etc.

        Returns:
            List[Indicator]: List of available technical indicators with their
                parameters and metadata.

        Example:
             indicators = client.public_symphony.get_indicators()
             for indicator in indicators:
            ...     print(f"{indicator.name}: {indicator.description}")
        """
        response = self._client.get("/api/v1/public/symphony-scores/indicators")
        return [Indicator.model_validate(item) for item in response]

    def get_symphony_meta(self, symphony_ids: List[str]) -> List[SymphonyMeta]:
        """
        Get metadata for symphonies by their IDs.

        Args:
            symphony_ids: List of symphony IDs to look up.

        Returns:
            List[SymphonyMeta]: List of symphony metadata objects.

        Example:
             meta = client.public_symphony.get_symphony_meta(["sym-abc123"])
             for symphony in meta:
            ...     print(f"{symphony.name}: {symphony.rebalance_frequency}")
        """
        response = self._client.post(
            "/api/v1/public/meta/symphonies", json={"symphony_id": symphony_ids}
        )
        result = SymphonyMetaResponse.model_validate(response)
        return result.symphonies

    def get_symphony(self, symphony_id: str) -> SymphonyDetail:
        """
        Get detailed information about a symphony.

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            SymphonyDetail: Detailed symphony information including stats,
                backtest data, and metadata.

        Example:
             symphony = client.public_symphony.get_symphony("sym-abc123")
             print(f"Name: {symphony.name}")
             print(f"Sharpe: {symphony.stats_oos_sharpe_ratio}")
        """
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}")
        return SymphonyDetail.model_validate(response)

    def get_versions(self, symphony_id: str) -> List[SymphonyVersionInfo]:
        """
        Get all versions for a symphony.

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            List[SymphonyVersionInfo]: List of version information.

        Example:
             versions = client.public_symphony.get_versions("sym-abc123")
             for version in versions:
            ...     print(f"Version {version.version_id}: {version.created_at}")
        """
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/versions")
        return [SymphonyVersionInfo.model_validate(item) for item in response]

    def get_version_score(
        self, symphony_id: str, version_id: str, score_version: str = "v1"
    ) -> SymphonyDefinition:
        """
        Get an existing symphony version's EDN (score).

        Args:
            symphony_id: Unique identifier for the symphony.
            version_id: Unique identifier for the symphony version.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            SymphonyDefinition: The symphony score/parsed EDN structure.

        Example:
             score = client.public_symphony.get_version_score(
            ...     "sym-abc123",
            ...     "ver-xyz789"
            ... )
             print(score.name)
             print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(
            f"/api/v1/public/symphonies/{symphony_id}/versions/{version_id}/score", params=params
        )
        return SymphonyDefinition.model_validate(response)

    def get_score(self, symphony_id: str, score_version: str = "v1") -> SymphonyDefinition:
        """
        Get an existing symphony's EDN (score).

        Args:
            symphony_id: Unique identifier for the symphony.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            SymphonyDefinition: The symphony score/parsed EDN structure.

        Example:
             score = client.public_symphony.get_score("sym-abc123")
             print(score.name)
             print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/score", params=params)
        return SymphonyDefinition.model_validate(response)

    def get_tickers(self, symphony_id: str) -> List[str]:
        """
        Get all tickers used in a symphony.

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            List[str]: List of ticker symbols used in the symphony.

        Example:
             tickers = client.public_symphony.get_tickers("sym-abc123")
             print(f"Symphony uses: {', '.join(tickers)}")
        """
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/tickers")
        result = TickersResponse.model_validate(response)
        return result.tickers

    def backtest_symphony(
        self,
        symphony_id: str,
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
        Run a backtest for a public symphony by its ID.

        Args:
            symphony_id: The ID of the symphony to backtest.
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
            BacktestResult: Parsed backtest result with all statistics.

        Example:
            result = client.public_symphony.backtest_symphony("sym-abc123")
            print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = {
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

        raw_response = self._client.post(
            f"/api/v1/public/symphonies/{symphony_id}/backtest",
            json=payload,
        )
        return BacktestResult.model_validate(raw_response)

    def backtest(
        self,
        symphony: Union[SymphonyDefinition, Dict[str, Any]],
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
        Run a standalone backtest with a custom symphony definition.

        Args:
            symphony: Symphony definition to backtest (SymphonyDefinition model or dict).
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
            BacktestResult: Parsed backtest result with all statistics.

        Example:
             result = client.public_symphony.backtest(symphony=SymphonyDefinition(...))
             print(f"Sharpe: {result.stats.sharpe_ratio}")

        Example with dict:
             score_data = {"step": "root", "name": "My Strategy", ...}
             result = client.public_symphony.backtest(symphony=score_data)
        """
        if isinstance(symphony, dict):
            raw_value = symphony
        else:
            raw_value = symphony.model_dump(by_alias=True, exclude_none=True)

        payload = {
            "symphony": {"raw_value": raw_value},
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

        raw_response = self._client.post(
            "/api/v1/public/backtest",
            json=payload,
        )
        return BacktestResult.model_validate(raw_response)

    def backtest_symphony_v2(
        self,
        symphony_id: str,
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
        Run a backtest for a public symphony by its ID (v2).

        Args:
            symphony_id: The ID of the symphony to backtest.
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
            BacktestResult: Parsed backtest result with all statistics.

        Example:
             result = client.public_symphony.backtest_symphony_v2("sym-abc123")
             print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = {
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

        raw_response = self._client.post(
            f"/api/v2/public/symphonies/{symphony_id}/backtest",
            json=payload,
        )
        return BacktestResult.model_validate(raw_response)
