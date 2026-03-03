"""Watchlist resource - endpoints for managing user's watchlist."""

from ..http_client import HTTPClient
from ..models.backtest import (
    WatchlistResponse,
    WatchlistSymphony,
    WatchlistSymphonyItem,
)


class Watchlist:
    """
    Watchlist endpoints.

    These endpoints provide access to the user's watchlist of symphonies
    they are tracking but haven't necessarily invested in.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def get_watchlist(self) -> list[WatchlistSymphony]:
        """
        Get all symphonies on the user's watchlist.

        Returns a list of symphonies the user has added to their watchlist
        for tracking purposes.

        Returns
        -------
            List[WatchlistSymphony]: List of watchlist symphonies with statistics.

        Example:
             watchlist = client.watchlist.get_watchlist()
             for item in watchlist:
            ...     print(f"Watching: {item.name}")
            ...     print(f"  Sharpe: {item.oos_sharpe_ratio}")
        """
        response = self._client.get("/api/v1/watchlist")
        result = WatchlistResponse.model_validate(response)
        return result.watchlist or [] or []

    def add_to_watchlist(self, symphony_id: str) -> WatchlistSymphonyItem:
        """
        Add a symphony to the user's watchlist.

        Args:
            symphony_id: The unique identifier of the symphony to add.

        Returns
        -------
            WatchlistSymphonyItem: The added symphony with its details.

        Example:
             result = client.watchlist.add_to_watchlist("fk6VGRDAAgiH120TfUPS")
             print(f"Added: {result.name}")
        """
        response = self._client.post(f"/api/v1/watchlist/{symphony_id}")
        return WatchlistSymphonyItem.model_validate(response)

    def remove_from_watchlist(self, symphony_id: str) -> None:
        """
        Remove a symphony from the user's watchlist.

        Args:
            symphony_id: The unique identifier of the symphony to remove.

        Example:
             client.watchlist.remove_from_watchlist("fk6VGRDAAgiH120TfUPS")
        """
        self._client.delete(f"/api/v1/watchlist/{symphony_id}")
