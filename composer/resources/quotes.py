"""Quotes resource for quote endpoints."""

from typing import List, Dict
from ..models.market_data import QuoteResult


class Quotes:
    """Resource for quote endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_quotes(self, tickers: List[str]) -> Dict[str, QuoteResult]:
        """
        Get realtime crypto and (15-minute delayed) equity quotes.

        If equity markets are closed, returns the last close price.

        Args:
            tickers: List of tickers to get quotes for (e.g., ["AAPL", "CRYPTO::BTC//USD"])

        Returns:
            Dict mapping ticker to QuoteResult
        """
        print({"tickers": tickers})
        response = self._client.post(
            "/api/v1/public/quotes",
            json={"tickers": tickers},
        )
        return {ticker: QuoteResult(**data) for ticker, data in response.items()}
