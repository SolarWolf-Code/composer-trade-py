from typing import Dict, Any, List, Optional, Union
from ..models.backtest import BacktestParams, BacktestResult
from ..models.symphony import (
    CreateSymphonyRequest,
    CreateSymphonyResponse,
    CopySymphonyRequest,
    CopySymphonyResponse,
    UpdateSymphonyResponse,
    SymphonyVersion,
)
from ..models.common.symphony import Root


class Symphony:
    def __init__(self, http_client):
        self.http_client = http_client

    def create_symphony(self, request: CreateSymphonyRequest) -> CreateSymphonyResponse:
        """
        Create a new symphony.

        Args:
            request: Symphony metadata including name, color, hashtag, and trading logic

        Returns:
            CreateSymphonyResponse with symphony_id and version_id

        Example:
            from composer.models.common.symphony import Root, Asset, WeightCashEqual
            from composer.models.symphony import CreateSymphonyRequest, AssetClass

            request = CreateSymphonyRequest(
                name="My Strategy",
                asset_class=AssetClass.EQUITIES,
                color="#FF6B6B",
                hashtag="#AAPL",
                symphony=Root(
                    name="My Strategy",
                    description="Buy AAPL",
                    rebalance="daily",
                    children=[
                        WeightCashEqual(children=[Asset(ticker="AAPL", name="Apple Inc")])
                    ]
                )
            )

            result = client.symphony.create_symphony(request)
            print(f"Created symphony: {result.symphony_id}")
        """
        payload = request.model_dump(exclude_none=True)
        # Wrap the symphony in raw_value structure as expected by API
        if "symphony" in payload:
            symphony_data = payload.pop("symphony")
            if hasattr(symphony_data, "model_dump"):
                symphony_data = symphony_data.model_dump(exclude_none=True)
            payload["symphony"] = {"raw_value": symphony_data}

        response = self.http_client.post("/api/v0.1/symphonies", json=payload)
        return CreateSymphonyResponse.model_validate(response)

    def search_symphonies(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for symphonies.
        """
        return self.http_client.get(
            "/api/v0.1/search/symphonies", params={"query": query}
        )

    def get_symphony_details(self, symphony_id: str) -> Dict[str, Any]:
        """
        Get details of a specific symphony.
        """
        return self.http_client.get(f"/api/v0.1/symphonies/{symphony_id}")

    def backtest_symphony_by_id(
        self,
        symphony_id: str,
        params: Optional[Union[Dict[str, Any], BacktestParams]] = None,
    ) -> BacktestResult:
        """
        Run a backtest for an existing symphony by its ID.

        Args:
            symphony_id: The ID of the symphony to backtest
            params: Backtest parameters as a dict or BacktestParams model.
                   If not provided, uses sensible defaults (capital=10000.0, etc.)

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
            # Simple usage with defaults
            result = client.symphony.backtest_symphony_by_id("symphony-id")
            print(result.stats.sharpe_ratio)

            # With custom params
            result = client.symphony.backtest_symphony_by_id(
                "symphony-id",
                params=BacktestParams(capital=50000.0, slippage_percent=0.01)
            )
        """
        if params is None:
            # Use default parameters
            params = BacktestParams()

        if isinstance(params, BacktestParams):
            payload = params.model_dump(by_alias=True, exclude_none=True, mode="json")
        else:
            payload = params

        raw_response = self.http_client.post(
            f"/api/v0.1/symphonies/{symphony_id}/backtest", json=payload
        )

        return BacktestResult.model_validate(raw_response)

    def copy_symphony(
        self, symphony_id: str, request: Optional[CopySymphonyRequest] = None
    ) -> CopySymphonyResponse:
        """
        Copy a symphony.

        Args:
            symphony_id: ID of the symphony to copy
            request: Optional copy settings (name, color, hashtag, etc.)

        Returns:
            CopySymphonyResponse with the new symphony_id and version_id
        """
        payload = request.model_dump(exclude_none=True) if request else {}
        response = self.http_client.post(
            f"/api/v0.1/symphonies/{symphony_id}/copy", json=payload
        )
        return CopySymphonyResponse.model_validate(response)

    def score_symphony(self, symphony_id: str) -> Root:
        """
        Get the score (EDN/trading logic) of a symphony.

        Args:
            symphony_id: ID of the symphony

        Returns:
            Root node representing the symphony's trading logic
        """
        response = self.http_client.get(f"/api/v0.1/symphonies/{symphony_id}/score")
        return Root.model_validate(response)

    def list_symphony_versions(self, symphony_id: str) -> List[SymphonyVersion]:
        """
        List versions of a symphony.

        Args:
            symphony_id: ID of the symphony

        Returns:
            List of SymphonyVersion objects
        """
        response = self.http_client.get(f"/api/v0.1/symphonies/{symphony_id}/versions")
        return [SymphonyVersion.model_validate(v) for v in response]

    def get_symphony_version_score(self, symphony_id: str, version_id: str) -> Root:
        """
        Get the score (EDN) of a specific version of a symphony.

        Args:
            symphony_id: ID of the symphony
            version_id: ID of the version

        Returns:
            Root node representing the version's trading logic
        """
        response = self.http_client.get(
            f"/api/v0.1/symphonies/{symphony_id}/versions/{version_id}/score"
        )
        return Root.model_validate(response)

    def update_symphony(
        self,
        symphony_id: str,
        request: CreateSymphonyRequest,
    ) -> UpdateSymphonyResponse:
        """
        Update an existing symphony.

        Args:
            symphony_id: ID of the symphony to update
            request: Updated symphony metadata including optional new trading logic

        Returns:
            UpdateSymphonyResponse with version IDs
        """
        payload = request.model_dump(exclude_none=True)
        # Wrap the symphony in raw_value structure as expected by API
        if "symphony" in payload:
            symphony_data = payload.pop("symphony")
            if hasattr(symphony_data, "model_dump"):
                symphony_data = symphony_data.model_dump(exclude_none=True)
            payload["symphony"] = {"raw_value": symphony_data}

        response = self.http_client.put(
            f"/api/v0.1/symphonies/{symphony_id}", json=payload
        )
        return UpdateSymphonyResponse.model_validate(response)

    def delete_symphony(self, symphony_id: str) -> None:
        """
        Delete a symphony.

        Args:
            symphony_id: ID of the symphony to delete
        """
        return self.http_client.delete(f"/api/v0.1/symphonies/{symphony_id}")
