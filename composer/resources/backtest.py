from typing import Dict, Any, Union, Optional, List
from ..models.backtest import (
    BacktestRequest,
    BacktestParams,
    BacktestResult,
    RebalanceRequest,
    RebalanceResult,
)


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
        self, request: Union[BacktestRequest, BacktestParams, Dict[str, Any]]
    ) -> BacktestResult:
        """
        Run a generic backtest simulation (v2).

        Args:
            request: BacktestRequest or BacktestParams model, or dictionary matching the schema.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
            >>> result = client.backtest.run_v2(BacktestRequest(...))
            >>> print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = request
        if isinstance(request, (BacktestRequest, BacktestParams)):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            if "symphony" in payload and payload["symphony"]:
                payload["symphony"] = {"raw_value": payload["symphony"]}

        raw_response = self.http_client.post("/api/v2/backtest", json=payload)
        return BacktestResult.model_validate(raw_response)

    def run_public_v2(
        self, request: Union[BacktestRequest, BacktestParams, Dict[str, Any]]
    ) -> BacktestResult:
        """
        Run a public backtest simulation (v2).

        Args:
            request: BacktestRequest or BacktestParams model, or dictionary matching the schema.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
            >>> result = client.backtest.run_public_v2(BacktestRequest(...))
            >>> print(f"Sharpe: {result.stats.sharpe_ratio}")
        """
        payload = request
        if isinstance(request, (BacktestRequest, BacktestParams)):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")
            if "symphony" in payload and payload["symphony"]:
                payload["symphony"] = {"raw_value": payload["symphony"]}

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
            >>> request = RebalanceRequest(
            ...     symphonies={
            ...         "sym-123": SymphonyRebalanceState(cash=10000, shares={})
            ...     }
            ... )
            >>> result = client.backtest.rebalance(request)
            >>> print(result.run_results)
        """
        payload = request
        if isinstance(request, RebalanceRequest):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")

        raw_response = self.http_client.post("/api/v2/rebalance", json=payload)
        return RebalanceResult.model_validate(raw_response)
