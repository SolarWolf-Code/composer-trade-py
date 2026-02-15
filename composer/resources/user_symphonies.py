"""User Symphonies resource - endpoints for user's symphony lists."""

from typing import List
from ..http_client import HTTPClient
from ..models.backtest import (
    UserSymphony,
    DraftSymphony,
    UserSymphoniesResponse,
    DraftSymphoniesResponse,
)


class UserSymphonies:
    """
    User's symphony list endpoints.

    These endpoints provide access to the user's library of symphonies,
    including both published and draft symphonies.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def list_symphonies(self) -> List[UserSymphony]:
        """
        Get all symphonies in the user's library.

        Returns a list of all symphonies created by or copied to the
        authenticated user's account.

        Returns:
            List[UserSymphony]: List of user's symphonies with statistics.

        Example:
            >>> symphonies = client.user_symphonies.list_symphonies()
            >>> for symphony in symphonies:
            ...     print(f"{symphony.name}: Sharpe={symphony.oos_sharpe_ratio}")
        """
        response = self._client.get("/api/v1/user/symphonies")
        result = UserSymphoniesResponse.model_validate(response)
        return result.symphonies

    def list_drafts(self) -> List[DraftSymphony]:
        """
        Get all draft symphonies in the user's library.

        Returns a list of draft (unpublished) symphonies created by the
        authenticated user.

        Returns:
            List[DraftSymphony]: List of user's draft symphonies with statistics.

        Example:
            >>> drafts = client.user_symphonies.list_drafts()
            >>> for draft in drafts:
            ...     print(f"Draft: {draft.name}")
        """
        response = self._client.get("/api/v1/user/symphonies/drafts")
        result = DraftSymphoniesResponse.model_validate(response)
        return result.symphonies
