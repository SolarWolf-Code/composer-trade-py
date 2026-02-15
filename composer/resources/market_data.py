"""Market data resource for options and other market data."""

from typing import Optional, List
from ..models.market_data import (
    OptionsChainResponse,
    OptionsContractResponse,
    OptionsOverview,
    ContractType,
    OptionSortBy,
    SortOrder,
)


class MarketData:
    """Resource for market data endpoints."""

    def __init__(self, http_client):
        self.http_client = http_client

    def get_options_chain(
        self,
        underlying: str,
        next_cursor: Optional[str] = None,
        strike_price: Optional[float] = None,
        expiry: Optional[str] = None,
        contract_type: Optional[ContractType] = None,
        order: SortOrder = SortOrder.ASC,
        limit: Optional[int] = None,
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

        Returns:
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

        response = self.http_client.get(
            "/api/v1/market-data/options/chain", params=params
        )
        return OptionsChainResponse.model_validate(response)

    def get_options_contract(self, symbol: str) -> OptionsContractResponse:
        """
        Get market data for a specific options contract.

        Args:
            symbol: The options contract symbol (e.g., "OPTIONS::AAPL250718C00210000//USD")

        Returns:
            OptionsContractResponse with contract market data
        """
        response = self.http_client.get(
            "/api/v1/market-data/options/contract", params={"symbol": symbol}
        )
        
        return OptionsContractResponse.model_validate(response)

    def get_options_overview(self, symbol: str) -> OptionsOverview:
        """
        Get an overview of options data for a given ticker.

        Args:
            symbol: The underlying asset symbol (e.g., "AAPL")

        Returns:
            OptionsOverview with available expiration dates
        """
        response = self.http_client.get(
            "/api/v1/market-data/options/overview", params={"symbol": symbol}
        )
        return OptionsOverview.model_validate(response)
