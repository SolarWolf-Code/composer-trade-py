"""Quotes resource for quote endpoints."""

from ..models.market_data import QuoteResult, _QuoteDict


class Quotes:
    """Resource for quote endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_quotes(self, tickers: list[str]) -> _QuoteDict:
        """
        Get realtime crypto and (15-minute delayed) equity quotes.

        If equity markets are closed, returns the last close price.

        Args:
            tickers: List of tickers to get quotes for (e.g., ["AAPL", "CRYPTO::BTC//USD"])

        Returns
        -------
            Dict mapping ticker to QuoteResult
        """
        response = self._client.post(
            "/api/v1/public/quotes",
            json={"tickers": tickers},
        )
        return _QuoteDict({ticker: QuoteResult(**data) for ticker, data in response.items()})
