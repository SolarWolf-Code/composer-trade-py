"""User Symphony resource - authenticated endpoints for symphony management."""

from typing import List, Optional, Dict, Any, Union
from ..http_client import HTTPClient
from ..models.backtest import (
    Indicator,
    SymphonyDetail,
    SymphonyVersionInfo,
    ModifySymphonyResponse,
    FindAndReplaceOperation,
    CompressNestedIfsModification,
    UpdateSymphonyResponse,
    UpdateSymphonyNodesResponse,
    BacktestResult,
    BacktestVersion,
    Broker,
    ApplySubscription,
    ScoreExtendedResponse,
    Modification,
)
from ..models.common import SymphonyDefinition
from ..models.symphony import (
    CreateSymphonyRequest,
    CreateSymphonyResponse,
    CopySymphonyRequest,
    CopySymphonyResponse,
)


class UserSymphony:
    """
    Authenticated symphony endpoints.

    These endpoints require authentication and provide access to the user's
    own symphonies as well as public symphonies with additional data.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def get_indicators(self) -> List[Indicator]:
        """
        Get a list of all available technical indicators (authenticated).

        Same as the public endpoint but may include additional indicators
        or data for authenticated users.

        Returns:
            List[Indicator]: List of available technical indicators with their
                parameters and metadata.

        Example:
             indicators = client.user_symphony.get_indicators()
             for indicator in indicators:
            ...     print(f"{indicator.name}: {indicator.description}")
        """
        response = self._client.get("/api/v1/symphony-scores/indicators")
        return [Indicator.model_validate(item) for item in response]

    def get_symphony(self, symphony_id: str) -> SymphonyDetail:
        """
        Get detailed information about a symphony (authenticated).

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            SymphonyDetail: Detailed symphony information including stats,
                backtest data, and metadata.

        Example:
             symphony = client.user_symphony.get_symphony("sym-abc123")
             print(f"Name: {symphony.name}")
             print(f"Sharpe: {symphony.stats_oos_sharpe_ratio}")
        """
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}")
        return SymphonyDetail.model_validate(response)

    def get_versions(self, symphony_id: str) -> List[SymphonyVersionInfo]:
        """
        Get all versions for a symphony (authenticated).

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            List[SymphonyVersionInfo]: List of version information.

        Example:
             versions = client.user_symphony.get_versions("sym-abc123")
             for version in versions:
            ...     print(f"Version {version.version_id}: {version.created_at}")
        """
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}/versions")
        return [SymphonyVersionInfo.model_validate(item) for item in response]

    def get_version_score(
        self, symphony_id: str, version_id: str, score_version: str = "v1"
    ) -> SymphonyDefinition:
        """
        Get an existing symphony version's EDN (score) - authenticated.

        Args:
            symphony_id: Unique identifier for the symphony.
            version_id: Unique identifier for the symphony version.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            SymphonyDefinition: The symphony score/parsed EDN structure.

        Example:
             score = client.user_symphony.get_version_score(
            ...     "sym-abc123",
            ...     "ver-xyz789"
            ... )
             print(score.name)
             print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(
            f"/api/v1/symphonies/{symphony_id}/versions/{version_id}/score", params=params
        )
        return SymphonyDefinition.model_validate(response)

    def get_score(self, symphony_id: str, score_version: str = "v1") -> SymphonyDefinition:
        """
        Get an existing symphony's EDN (score) - authenticated.

        Args:
            symphony_id: Unique identifier for the symphony.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            SymphonyDefinition: The symphony score/parsed EDN structure.

        Example:
             score = client.user_symphony.get_score("sym-abc123")
             print(score.name)
             print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}/score", params=params)
        print(response)
        return SymphonyDefinition.model_validate(response)

    def get_score_extended(self, symphony_id: str) -> ScoreExtendedResponse:
        """
        Get a symphony's score along with suggested modifications.

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            ScoreExtendedResponse: Contains the symphony score and suggested modifications.

        Example:
              result = client.user_symphony.get_score_extended("sym-abc123")
              print(result.score.name)
              for mod in result.modifications:
                  print(f"  Modification: {mod}")
        """
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}/score-extended")

        modifications = []
        for mod in response.get("modifications", []):
            op = mod.get("op")
            if op == "FIND_AND_REPLACE":
                modifications.append(FindAndReplaceOperation.model_validate(mod))
            elif op == "COMPRESS_NESTED_IFS":
                modifications.append(CompressNestedIfsModification.model_validate(mod))
            else:
                modifications.append(mod)

        return ScoreExtendedResponse(
            score=SymphonyDefinition.model_validate(response.get("score")),
            modifications=modifications,
        )

    def modify_symphony(
        self, symphony_id: str, old_ticker: str, new_ticker: str
    ) -> ModifySymphonyResponse:
        """
        Programmatically modify a symphony by finding and replacing a ticker.

        Args:
            symphony_id: Unique identifier for the symphony to modify.
            old_ticker: The ticker symbol to find (e.g., "SPY").
            new_ticker: The ticker symbol to replace with (e.g., "TQQQ").

        Returns:
            ModifySymphonyResponse: Contains the symphony_id and version_id of
                the modified symphony.

        Example:
             result = client.user_symphony.modify_symphony(
            ...     "fk6VGRDAAgiH120TfUPS",
            ...     "SPY",
            ...     "TQQQ"
            ... )
             print(f"Modified symphony: {result.symphony_id}, version: {result.version_id}")
        """
        request_body = {
            "op": "FIND_AND_REPLACE",
            "old_ticker": old_ticker,
            "new_ticker": new_ticker,
        }
        response = self._client.post(
            f"/api/v1/symphonies/{symphony_id}/modify",
            json=request_body,
        )
        return ModifySymphonyResponse.model_validate(response)

    def update_symphony(
        self,
        symphony_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None,
        hashtag: Optional[str] = None,
        tags: Optional[List[str]] = None,
        symphony: Optional[Dict[str, Any]] = None,
        benchmarks: Optional[List[Dict[str, Any]]] = None,
        share_with_everyone: Optional[bool] = None,
    ) -> UpdateSymphonyResponse:
        """
        Update an existing symphony.

        Args:
            symphony_id: Unique identifier for the symphony to update.
            name: Optional new name for the symphony.
            description: Optional new description.
            color: Optional new color (hex code).
            hashtag: Optional new hashtag.
            tags: Optional list of tags.
            symphony: Optional symphony score/EDN definition.
            benchmarks: Optional list of benchmark configurations.
            share_with_everyone: Optional whether to share with everyone.

        Returns:
            UpdateSymphonyResponse: Contains existing_version_id and version_id.

        Example:
             result = client.user_symphony.update_symphony(
            ...     "fk6VGRDAAgiH120TfUPS",
            ...     name="New Name",
            ...     description="New description"
            ... )
             print(f"New version: {result.version_id}")
        """
        request_body: Dict[str, Any] = {}
        if name is not None:
            request_body["name"] = name
        if description is not None:
            request_body["description"] = description
        if color is not None:
            request_body["color"] = color
        if hashtag is not None:
            request_body["hashtag"] = hashtag
        if tags is not None:
            request_body["tags"] = tags
        if symphony is not None:
            request_body["symphony"] = symphony
        if benchmarks is not None:
            request_body["benchmarks"] = benchmarks
        if share_with_everyone is not None:
            request_body["share_with_everyone"] = share_with_everyone

        response = self._client.put(
            f"/api/v1/symphonies/{symphony_id}",
            json=request_body,
        )
        return UpdateSymphonyResponse.model_validate(response)

    def delete_symphony(self, symphony_id: str) -> None:
        """
        Delete an existing symphony.

        Args:
            symphony_id: Unique identifier for the symphony to delete.

        Example:
             client.user_symphony.delete_symphony("fk6VGRDAAgiH120TfUPS")
        """
        self._client.delete(f"/api/v1/symphonies/{symphony_id}")

    def submit_to_community(self, symphony_id: str) -> Dict[str, Any]:
        """
        Submit a symphony to the Composer Community.

        Submitted symphonies will first be reviewed by an internal panel
        before being added to the Community search on Discover.

        Args:
            symphony_id: Unique identifier for the symphony to submit.

        Returns:
            Dict[str, Any]: Response from the API.

        Example:
             result = client.user_symphony.submit_to_community("fk6VGRDAAgiH120TfUPS")
             print(result)
        """
        response = self._client.put(f"/api/v1/symphonies/{symphony_id}/submit-to-community")
        return response

    def create_symphony(
        self,
        name: str,
        asset_class: str = "EQUITIES",
        description: Optional[str] = None,
        color: Optional[str] = None,
        hashtag: Optional[str] = None,
        tags: Optional[List[str]] = None,
        symphony: Optional[SymphonyDefinition] = None,
        benchmarks: Optional[List[Dict[str, Any]]] = None,
    ) -> CreateSymphonyResponse:
        """
        Create a new symphony.

        Args:
            name: Name of the symphony.
            asset_class: Asset class (EQUITIES or CRYPTO). Defaults to EQUITIES.
            description: Optional description.
            color: Optional color (hex code).
            hashtag: Optional hashtag.
            tags: Optional list of tags.
            symphony: Optional symphony definition (SymphonyDefinition model).
            benchmarks: Optional list of benchmark configurations.

        Returns:
            CreateSymphonyResponse: Contains symphony_id and version_id.

        Example:
             from composer.models.common import Asset, WeightCashEqual, SymphonyDefinition
             symphony = SymphonyDefinition(name="My Strategy", rebalance="daily", children=[...])
             result = client.user_symphony.create_symphony(
            ...     name="My Strategy",
            ...     symphony=symphony
            ... )
             print(f"Created: {result.symphony_id}")
        """
        request_body: Dict[str, Any] = {"name": name, "asset_class": asset_class}
        if description is not None:
            request_body["description"] = description
        if color is not None:
            request_body["color"] = color
        if hashtag is not None:
            request_body["hashtag"] = hashtag
        if tags is not None:
            request_body["tags"] = tags
        if symphony is not None:
            request_body["symphony"] = {
                "raw_value": symphony.model_dump(by_alias=True, mode="json", exclude_none=True)
            }
        if benchmarks is not None:
            request_body["benchmarks"] = benchmarks

        response = self._client.post("/api/v1/symphonies", json=request_body)
        return CreateSymphonyResponse.model_validate(response)

    def copy_symphony(
        self,
        symphony_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        hashtag: Optional[str] = None,
        benchmarks: Optional[List[Dict[str, Any]]] = None,
    ) -> CopySymphonyResponse:
        """
        Copy an existing symphony.

        Args:
            symphony_id: ID of the symphony to copy.
            name: Optional new name for the copied symphony.
            color: Optional color for the copied symphony.
            hashtag: Optional hashtag for the copied symphony.
            benchmarks: Optional benchmark configurations.

        Returns:
            CopySymphonyResponse: Contains the new symphony_id and version_id.

        Example:
             result = client.user_symphony.copy_symphony(
            ...     "fk6VGRDAAgiH120TfUPS",
            ...     name="My Copy"
            ... )
             print(f"Copied: {result.symphony_id}")
        """
        request_body: Dict[str, Any] = {}
        if name is not None:
            request_body["name"] = name
        if color is not None:
            request_body["color"] = color
        if hashtag is not None:
            request_body["hashtag"] = hashtag
        if benchmarks is not None:
            request_body["benchmarks"] = benchmarks

        response = self._client.post(
            f"/api/v1/symphonies/{symphony_id}/copy",
            json=request_body,
        )
        return CopySymphonyResponse.model_validate(response)

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
        Run a backtest for an existing symphony by its ID.

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
             result = client.user_symphony.backtest_symphony("fk6VGRDAAgiH120TfUPS")
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
            f"/api/v1/symphonies/{symphony_id}/backtest",
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
        Run a backtest for an existing symphony by its ID (v2).

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
             result = client.user_symphony.backtest_symphony_v2("fk6VGRDAAgiH120TfUPS")
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
            f"/api/v2/symphonies/{symphony_id}/backtest",
            json=payload,
        )
        return BacktestResult.model_validate(raw_response)

    def update_symphony_nodes(
        self,
        symphony_id: str,
        version_id: str,
        updates: List[Dict[str, Any]],
    ) -> UpdateSymphonyNodesResponse:
        """
        Partially update nodes of a symphony version's EDN.

        Args:
            symphony_id: Unique identifier for the symphony.
            version_id: Unique identifier for the symphony version (must be latest).
            updates: List of node updates to apply.

        Returns:
            UpdateSymphonyNodesResponse: Response containing symphony_id and version_id.

        Example:
             result = client.user_symphony.update_symphony_nodes(
            ...     "fk6VGRDAAgiH120TfUPS",
            ...     "v1",
            ...     [{"id": "node-123", "ticker": "QQQ"}]
            ... )
             print(result.symphony_id, result.version_id)
        """
        request_body = {"updates": updates}
        response = self._client.patch(
            f"/api/v1/symphonies/{symphony_id}/versions/{version_id}/score/nodes",
            json=request_body,
        )
        return UpdateSymphonyNodesResponse.model_validate(response)
