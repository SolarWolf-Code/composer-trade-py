"""Search resource for publicly shared symphonies."""

from typing import Any

from ..models.search import SearchSymphonyResult


class Search:
    """Resource for searching publicly shared symphonies."""

    def __init__(self, http_client):
        self.http_client = http_client

    def search_symphonies(
        self,
        where: list[Any] | None = None,
        order_by: list[list[str]] | None = None,
        offset: int = 0,
    ) -> list[SearchSymphonyResult]:
        """
        Search our database of publicly shared symphonies.

        Args:
            where: Filter conditions for the search. Uses HoneySQL (Clojure) syntax.
                   Format: ["and", [condition1], [condition2], ...]
                   Example: ["and", [">", "oos_num_backtest_days", 180]]
            order_by: Sorting criteria as list of [field, direction] pairs.
                      For example: [["oos_sharpe_ratio", "desc"]]
            offset: Pagination offset for results

        Returns
        -------
            List of matching symphonies with performance statistics
        """
        if where is None:
            where = []
        request: dict[str, Any] = {"offset": offset}
        if where is not None:
            request["where"] = where
        if order_by is not None:
            request["order_by"] = order_by

        response = self.http_client.post(
            "/api/v1/public/search/symphonies",
            json=request,
        )

        return [SearchSymphonyResult.model_validate(r) for r in response]

    def search_symphonies_v2(
        self,
        filter: str | None = None,
        order_by: list[list[str]] | None = None,
        offset: int = 0,
    ) -> list[SearchSymphonyResult]:
        """
        Search publicly shared symphonies using CEL filters (V2).

        Args:
            filter: CEL filter expression for advanced filtering.
                    Example: "oos_sharpe_ratio > 1.5"
            order_by: Sorting criteria as list of [field, direction] pairs.
                      For example: [["oos_sharpe_ratio", "desc"]]
            offset: Pagination offset for results

        Returns
        -------
            List of matching symphonies with performance statistics
        """
        request: dict[str, Any] = {"offset": offset}
        if filter is not None:
            request["filter"] = filter
        if order_by is not None:
            request["order_by"] = order_by

        response = self.http_client.post(
            "/api/v1/public/search/symphonies-v2",
            json=request,
        )
        return [SearchSymphonyResult.model_validate(r) for r in response]
