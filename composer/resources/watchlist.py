"""Watchlist resource - endpoints for managing user's watchlist."""

from typing import List
from ..http_client import HTTPClient
from ..models.backtest import (
    WatchlistSymphony,
    WatchlistResponse,
)


class Watchlist:
    """
    Watchlist endpoints.

    These endpoints provide access to the user's watchlist of symphonies
    they are tracking but haven't necessarily invested in.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def get_watchlist(self) -> List[WatchlistSymphony]:
        """
        Get all symphonies on the user's watchlist.

        Returns a list of symphonies the user has added to their watchlist
        for tracking purposes.

        Returns:
            List[WatchlistSymphony]: List of watchlist symphonies with statistics.

        Example:
            >>> watchlist = client.watchlist.get_watchlist()
            >>> for item in watchlist:
            ...     print(f"Watching: {item.name}")
            ...     print(f"  Sharpe: {item.oos_sharpe_ratio}")
        """
        response = self._client.get("/api/v1/watchlist")
        result = WatchlistResponse.model_validate(response)
        return result.watchlist
