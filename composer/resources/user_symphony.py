"""User Symphony resource - authenticated endpoints for symphony management."""

from typing import List, Optional
from ..http_client import HTTPClient
from ..models.backtest import (
    Indicator,
    SymphonyDetail,
    SymphonyVersionInfo,
)
from ..models.common import Root


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
            >>> indicators = client.user_symphony.get_indicators()
            >>> for indicator in indicators:
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
            >>> symphony = client.user_symphony.get_symphony("sym-abc123")
            >>> print(f"Name: {symphony.name}")
            >>> print(f"Sharpe: {symphony.stats_oos_sharpe_ratio}")
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
            >>> versions = client.user_symphony.get_versions("sym-abc123")
            >>> for version in versions:
            ...     print(f"Version {version.version_id}: {version.created_at}")
        """
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}/versions")
        return [SymphonyVersionInfo.model_validate(item) for item in response]

    def get_version_score(
        self, symphony_id: str, version_id: str, score_version: str = "v1"
    ) -> Root:
        """
        Get an existing symphony version's EDN (score) - authenticated.

        Args:
            symphony_id: Unique identifier for the symphony.
            version_id: Unique identifier for the symphony version.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            Root: The symphony score/parsed EDN structure.

        Example:
            >>> score = client.user_symphony.get_version_score(
            ...     "sym-abc123",
            ...     "ver-xyz789"
            ... )
            >>> print(score.name)
            >>> print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(
            f"/api/v1/symphonies/{symphony_id}/versions/{version_id}/score", params=params
        )
        return Root.model_validate(response)

    def get_score(self, symphony_id: str, score_version: str = "v1") -> Root:
        """
        Get an existing symphony's EDN (score) - authenticated.

        Args:
            symphony_id: Unique identifier for the symphony.
            score_version: Score version to retrieve ("v1" or "v2"). Defaults to "v1".

        Returns:
            Root: The symphony score/parsed EDN structure.

        Example:
            >>> score = client.user_symphony.get_score("sym-abc123")
            >>> print(score.name)
            >>> print(score.rebalance)
        """
        params = {"score_version": score_version}
        response = self._client.get(f"/api/v1/symphonies/{symphony_id}/score", params=params)
        return Root.model_validate(response)
