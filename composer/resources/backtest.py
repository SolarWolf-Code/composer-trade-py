from typing import Dict, Any, Union
from ..models.backtest import BacktestRequest, BacktestResult


class Backtest:
    def __init__(self, http_client):
        self.http_client = http_client

    def run(self, request: Union[BacktestRequest, Dict[str, Any]]) -> BacktestResult:
        """
        Run a generic backtest simulation.

        Args:
            request: BacktestRequest model or dictionary matching the schema.

        Returns:
            BacktestResult: Parsed backtest result with all statistics

        Example:
            # Backtest with full symphony definition
            result = client.backtest.run(
                BacktestRequest(
                    symphony=SymphonyDefinition(
                        raw_value=Root(name="My Strategy", ...)
                    )
                )
            )

            # Backtest with encoded EDN
            result = client.backtest.run(
                BacktestRequest(
                    symphony=SymphonyDefinition(
                        encoded_value="...transit...",
                        encoding_type="transit_json"
                    )
                )
            )
        """
        payload = request
        if isinstance(request, BacktestRequest):
            payload = request.model_dump(by_alias=True, exclude_none=True, mode="json")

        raw_response = self.http_client.post("/api/v0.1/backtest", json=payload)
        return BacktestResult.model_validate(raw_response)
