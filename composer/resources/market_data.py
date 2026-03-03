"""Market data resource for options and other market data."""

from ..models.market_data import (
    ContractType,
    CustomBars,
    MarketOverview,
    MarketSnapshot,
    OptionsChainResponse,
    OptionsContractResponse,
    OptionSortBy,
    OptionsOverview,
    SortOrder,
    TopMoversResponse,
)


class MarketData:
    """Resource for market data endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_options_chain(
        self,
        underlying: str,
        next_cursor: str | None = None,
        strike_price: float | None = None,
        expiry: str | None = None,
        contract_type: ContractType | None = None,
        order: SortOrder = SortOrder.ASC,
        limit: int | None = None,
        sort_by: OptionSortBy = OptionSortBy.SYMBOL,
    ) -> OptionsChainResponse:
        """
        Get options chain for a specific underlying asset.

        Args:
            underlying: The underlying asset symbol (e.g., "AAPL")
            next_cursor: Pagination cursor for fetching the next page
            strike_price: Filter by specific strike price
            expiry: Filter by expiration date (YYYY-MM-DD format)
            contract_type: Filter by option type (CALL or PUT)
            order: Sort order for results
            limit: Maximum number of results to return (max 250)
            sort_by: Field to sort results by

        Returns
        -------
            OptionsChainResponse with list of options contracts
        """
        params: dict = {
            "underlying_asset_symbol": underlying,
            "order": order.value,
            "sort_by": sort_by.value,
        }
        if next_cursor:
            params["next_cursor"] = next_cursor
        if strike_price:
            params["strike_price"] = strike_price
        if expiry:
            params["expiry"] = expiry
        if contract_type:
            params["contract_type"] = contract_type.value
        if limit:
            params["limit"] = limit

        response = self._client.get("/api/v1/market-data/options/chain", params=params)
        return OptionsChainResponse.model_validate(response)

    def get_options_contract(self, symbol: str) -> OptionsContractResponse:
        """
        Get market data for a specific options contract.

        Args:
            symbol: The options contract symbol (e.g., "OPTIONS::AAPL250718C00210000//USD")

        Returns
        -------
            OptionsContractResponse with contract market data
        """
        response = self._client.get(
            "/api/v1/market-data/options/contract", params={"symbol": symbol}
        )

        return OptionsContractResponse.model_validate(response)

    def get_options_overview(self, symbol: str) -> OptionsOverview:
        """
        Get an overview of options data for a given ticker.

        Args:
            symbol: The underlying asset symbol (e.g., "AAPL")

        Returns
        -------
            OptionsOverview with available expiration dates
        """
        response = self._client.get(
            "/api/v1/market-data/options/overview", params={"symbol": symbol}
        )
        return OptionsOverview.model_validate(response)

    def get_snapshot(self, symbol: str) -> MarketSnapshot:
        """
        Get a snapshot of live market data.

        Args:
            symbol: The symbol to get snapshot for (e.g., "AAPL", "BTC-USD")

        Returns
        -------
            MarketSnapshot with bid, ask, last trade, and change data
        """
        response = self._client.get("/api/v1/market-data/snapshot", params={"symbol": symbol})
        return MarketSnapshot.model_validate(response)

    def get_custom_bars(
        self,
        symbol: str,
        range_date_from: str | None = None,
        range_date_to: str | None = None,
        range_preset: str | None = None,
    ) -> CustomBars:
        """
        Get custom bars market data.

        Args:
            symbol: The symbol to get bars for (e.g., "AAPL", "BTC-USD")
            range_date_from: Start date (YYYY-MM-DD format)
            range_date_to: End date (YYYY-MM-DD format)
            range_preset: Preset range (e.g., "1M", "3M", "1Y", "5Y")

        Returns
        -------
            CustomBars with OHLCV data
        """
        params = {"symbol": symbol}
        if range_date_from:
            params["range_date_from"] = range_date_from
        if range_date_to:
            params["range_date_to"] = range_date_to
        if range_preset:
            params["range_preset"] = range_preset

        response = self._client.get("/api/v1/market-data/custom-bars", params=params)
        return CustomBars.model_validate(response)

    def get_market_overview(self, symbol: str) -> MarketOverview:
        """
        Get an overview of reference data for a symbol.

        Args:
            symbol: The symbol to get overview for (e.g., "AAPL", "BTC-USD")

        Returns
        -------
            MarketOverview with company info, market cap, etc.
        """
        response = self._client.get("/api/v1/market-data/overview", params={"symbol": symbol})
        return MarketOverview.model_validate(response)

    def get_top_movers(self) -> TopMoversResponse:
        """
        Get top movers market data.

        Returns
        -------
            TopMoversResponse with list of top gaining/losing symbols
        """
        response = self._client.get("/api/v1/market-data/top-movers")
        return TopMoversResponse.model_validate(response)
