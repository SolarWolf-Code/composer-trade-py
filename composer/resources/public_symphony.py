"""Public Symphony resource - public endpoints for accessing symphony data."""

from typing import List, Optional
from ..http_client import HTTPClient
from ..models.backtest import (
    Indicator,
    SymphonyMeta,
    SymphonyMetaResponse,
    SymphonyDetail,
    SymphonyVersionInfo,
    TickersResponse,
)
from ..models.common import Root


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
            >>> indicators = client.public_symphony.get_indicators()
            >>> for indicator in indicators:
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
            >>> meta = client.public_symphony.get_symphony_meta(["sym-abc123"])
            >>> for symphony in meta:
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
            >>> symphony = client.public_symphony.get_symphony("sym-abc123")
            >>> print(f"Name: {symphony.name}")
            >>> print(f"Sharpe: {symphony.stats_oos_sharpe_ratio}")
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
            >>> versions = client.public_symphony.get_versions("sym-abc123")
            >>> for version in versions:
            ...     print(f"Version {version.version_id}: {version.created_at}")
        """
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/versions")
        return [SymphonyVersionInfo.model_validate(item) for item in response]

    def get_version_score(
        self, symphony_id: str, version_id: str, score_version: str = "v1"
    ) -> Root:
        """
        Get an existing symphony version's EDN (score).

        Args:
            symphony_id: Unique identifier for the symphony.
            version_id: Unique identifier for the symphony version.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            Root: The symphony score/parsed EDN structure.

        Example:
            >>> score = client.public_symphony.get_version_score(
            ...     "sym-abc123",
            ...     "ver-xyz789"
            ... )
            >>> print(score.name)
            >>> print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(
            f"/api/v1/public/symphonies/{symphony_id}/versions/{version_id}/score", params=params
        )
        return Root.model_validate(response)

    def get_score(self, symphony_id: str, score_version: str = "v1") -> Root:
        """
        Get an existing symphony's EDN (score).

        Args:
            symphony_id: Unique identifier for the symphony.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            Root: The symphony score/parsed EDN structure.

        Example:
            >>> score = client.public_symphony.get_score("sym-abc123")
            >>> print(score.name)
            >>> print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/score", params=params)
        return Root.model_validate(response)

    def get_tickers(self, symphony_id: str) -> List[str]:
        """
        Get all tickers used in a symphony.

        Args:
            symphony_id: Unique identifier for the symphony.

        Returns:
            List[str]: List of ticker symbols used in the symphony.

        Example:
            >>> tickers = client.public_symphony.get_tickers("sym-abc123")
            >>> print(f"Symphony uses: {', '.join(tickers)}")
        """
        response = self._client.get(f"/api/v1/public/symphonies/{symphony_id}/tickers")
        result = TickersResponse.model_validate(response)
        return result.tickers
