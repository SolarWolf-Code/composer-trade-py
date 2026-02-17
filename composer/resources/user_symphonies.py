"""User Symphonies resource - endpoints for user's symphony lists."""

from typing import List, Optional, Any, Dict
from ..http_client import HTTPClient
from ..models.backtest import (
    UserSymphony,
    DraftSymphony,
    UserSymphoniesResponse,
    DraftSymphoniesResponse,
    BulkModifySymphoniesRequest,
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
             symphonies = client.user_symphonies.list_symphonies()
             for symphony in symphonies:
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
             drafts = client.user_symphonies.list_drafts()
             for draft in drafts:
            ...     print(f"Draft: {draft.name}")
        """
        response = self._client.get("/api/v1/user/symphonies/drafts")
        result = DraftSymphoniesResponse.model_validate(response)
        return result.symphonies

    def bulk_modify_symphonies(
        self, old_ticker: str, new_ticker: str, user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Bulk modify all symphonies in the user's library by finding and replacing a ticker.

        Args:
            old_ticker: The ticker symbol to find (e.g., "SPY").
            new_ticker: The ticker symbol to replace with (e.g., "TQQQ").
            user_id: Optional user ID. If not provided, uses the authenticated user.

        Returns:
            List[Dict[str, Any]]: Response from the bulk modify operation.

        Example:
             result = client.user_symphonies.bulk_modify_symphonies(
            ...     "SPY",
            ...     "TQQQ"
            ... )
             print(result)
        """
        request_body = {
            "op": "FIND_AND_REPLACE",
            "old_ticker": old_ticker,
            "new_ticker": new_ticker,
        }
        if user_id:
            request_body["user_id"] = user_id
        response = self._client.post(
            "/api/v1/user/symphonies/modify",
            json=request_body,
        )
        return response

    def pubsub_modify_symphonies(
        self,
        subscription: str,
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Programmatically modify all of a user's symphonies via pub/sub.

        Args:
            subscription: The pub/sub subscription name.
            message: The message containing modification instructions.

        Returns:
            Dict[str, Any]: Response from the API.

        Example:
             result = client.user_symphonies.pubsub_modify_symphonies(
            ...     subscription="my-subscription",
            ...     message={"publish_time": "2024-01-01", "data": {...}}
            ... )
             print(result)
        """
        request_body = {
            "subscription": subscription,
            "message": message,
        }
        response = self._client.post(
            "/api/v1/pubsub/symphonies/modify",
            json=request_body,
        )
        return response
