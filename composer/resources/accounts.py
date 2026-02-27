"""Accounts resource for account-related endpoints."""

import builtins
from typing import Any

from ..models.accounts import (
    AccountInfo,
    AccountsListResponse,
    AvailableAccountType,
    BuyingPower,
    Holding,
    InvestorDocument,
    SupportedRegionsResponse,
    Trade,
    TradeHistoryItem,
    TradeVolumeResponse,
)


class Accounts:
    """Resource for account-related endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def list(self) -> AccountsListResponse:
        """
        Get a list of all accounts associated with the authenticated user.

        Returns
        -------
            List of accounts with status, asset classes, and key dates
        """
        response = self._client.get("/api/v1/accounts/list")
        return AccountsListResponse.model_validate(response)

    def get_holdings(
        self,
        account_id: str,
        position_type: str | None = None,
    ) -> builtins.list[Holding]:
        """
        Get all current positions held in the specified account.

        Args:
            account_id: The account UUID
            position_type: Optional filter - 'direct', 'symphony', or 'all'

        Returns
        -------
            List of holdings in the account
        """
        params = {}
        if position_type:
            position_type_map = {
                "direct": "DEFAULT_DIRECT",
                "symphony": "SYMPHONY",
                "all": "ALL",
            }
            params["position_type"] = position_type_map.get(
                position_type.lower(), position_type.upper()
            )
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/holdings",
            params=params if params else None,
        )
        return [Holding.model_validate(h) for h in response]

    def get_available_types(
        self,
        country: str | None = None,
        state: str | None = None,
        white_label_footprint: bool | None = None,
    ) -> dict[str, builtins.list[AvailableAccountType]]:
        """
        Get available account types for a user to create.

        Args:
            country: Country code
            state: State code
            white_label_footprint: Whether to use white label footprint

        Returns
        -------
            Map of region to available account types
        """
        params = {}
        if country:
            params["country"] = country
        if state:
            params["state"] = state
        if white_label_footprint is not None:
            params["white_label_footprint"] = white_label_footprint
        response = self._client.get(
            "/api/v1/accounts/available-types/v2",
            params=params if params else None,
        )
        return {
            region: [AvailableAccountType.model_validate(at) for at in types]
            for region, types in response.items()
        }

    def get_supported_regions(self) -> SupportedRegionsResponse:
        """
        Get a list of countries and states that support equity/crypto trading.

        Returns
        -------
            Supported regions for EQUITIES and CRYPTO trading
        """
        response = self._client.get("/api/v1/accounts/supported-regions")
        return SupportedRegionsResponse.model_validate(response)

    def get_activities_trades(
        self,
        account_id: str,
        asset_class: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_request_id: str | None = None,
    ) -> builtins.list[Trade]:
        """
        Get record of historical trades.

        Args:
            account_id: The account UUID
            asset_class: Filter by asset class (CRYPTO, EQUITIES, OPTIONS)
            limit: Maximum number of results
            offset: Pagination offset
            order_request_id: Filter by order request ID

        Returns
        -------
            List of historical trades
        """
        params = {}
        if asset_class:
            params["asset_class"] = asset_class
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if order_request_id:
            params["order_request_id"] = order_request_id
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/activities/trades",
            params=params if params else None,
        )
        return [Trade.model_validate(t) for t in response]

    def get_activities_trades_volume(
        self,
        account_id: str,
        start_time: str,
        asset_class: str | None = None,
        direct_trading_only: bool | None = None,
    ) -> TradeVolumeResponse:
        """
        Get trade volume for the account.

        Args:
            account_id: The account UUID
            start_time: Start time for the volume calculation (ISO format with
                timezone, e.g., "2025-12-10T09:00:00-05:00")
            asset_class: Filter by asset class (CRYPTO, EQUITIES, OPTIONS)
            direct_trading_only: Only include direct trading volume

        Returns
        -------
            Trade volume information
        """
        params: dict[str, Any] = {"start_time": start_time}
        if asset_class:
            params["asset_class"] = asset_class
        if direct_trading_only is not None:
            params["direct_trading_only"] = direct_trading_only
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/activities/trades/volume",
            params=params,
        )
        return TradeVolumeResponse.model_validate(response)

    def get_activities_trade_history(
        self,
        account_id: str,
        asset_class: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_request_id: str | None = None,
    ) -> builtins.list[TradeHistoryItem]:
        """
        Get record of historical trades and option events.

        Args:
            account_id: The account UUID
            asset_class: Filter by asset class (CRYPTO, EQUITIES, OPTIONS)
            limit: Maximum number of results
            offset: Pagination offset
            order_request_id: Filter by order request ID

        Returns
        -------
            List of trade history items including option events
        """
        params = {}
        if asset_class:
            params["asset_class"] = asset_class
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if order_request_id:
            params["order_request_id"] = order_request_id
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/activities/trade-history",
            params=params if params else None,
        )
        return [TradeHistoryItem.model_validate(t) for t in response]

    def get_info(self, account_id: str) -> AccountInfo:
        """
        Get basic account owner information.

        Args:
            account_id: The account UUID

        Returns
        -------
            Account owner information including identity, contact, and profile
        """
        response = self._client.get(f"/api/v1/accounts/{account_id}/info")
        return AccountInfo.model_validate(response)

    def get_buying_power(self, account_id: str) -> builtins.list[BuyingPower]:
        """
        Get account buying power by asset class.

        Args:
            account_id: The account UUID

        Returns
        -------
            List of buying power info for each asset class
        """
        response = self._client.get(f"/api/v1/accounts/{account_id}/info/buying-power")
        return [BuyingPower.model_validate(bp) for bp in response]

    def get_investor_documents(
        self,
        account_id: str,
        category: str,
        year: int,
    ) -> builtins.list[InvestorDocument]:
        """
        Get investor documents for Apex and Alpaca accounts.

        Args:
            account_id: The account UUID
            category: Document category (STATEMENT, TAX_FORM, etc.)
            year: Year of documents to retrieve

        Returns
        -------
            List of investor documents
        """
        params = {"category": category, "year": year}
        response = self._client.get(
            f"/api/v1/accounts/{account_id}/info/investor-documents",
            params=params,
        )
        return [InvestorDocument.model_validate(d) for d in response]

    def download_document(self, document_id: str) -> str:
        """
        Download a single document.

        Args:
            document_id: The document ID to download

        Returns
        -------
            URL to download the document (redirect)
        """
        response = self._client.get(f"/api/v1/accounts/documents/{document_id}/download")
        return response
