"""Accounts response models."""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class AssetClass(str, Enum):
    """Asset class types."""

    CRYPTO = "CRYPTO"
    EQUITIES = "EQUITIES"
    OPTIONS = "OPTIONS"


class DirectTradableAssetClasses(BaseModel):
    """Asset classes available for direct trading."""

    model_config = {"populate_by_name": True}

    buy: List[AssetClass] = Field(
        description="Asset classes available for buying via direct trading"
    )
    sell: List[AssetClass] = Field(
        description="Asset classes available for selling via direct trading"
    )


class Account(BaseModel):
    """
    A brokerage account.

    Contains information about the account status, supported asset classes,
    and key dates for account activity.
    """

    model_config = {"populate_by_name": True}

    account_uuid: str = Field(description="Unique identifier (UUID) for the account")
    account_foreign_id: Optional[str] = Field(
        None, description="Foreign ID from the broker (if applicable)"
    )
    account_type: str = Field(
        description="Type of account (e.g., INDIVIDUAL, IRA, etc.)"
    )
    asset_classes: List[AssetClass] = Field(
        description="Asset classes supported by this account"
    )
    direct_tradable_asset_classes: DirectTradableAssetClasses = Field(
        description="Asset classes available for direct buy/sell trading"
    )
    symphony_tradable_asset_classes: List[AssetClass] = Field(
        description="Asset classes available for Symphony automation"
    )
    account_number: Optional[str] = Field(
        None, description="Account number (if available)"
    )
    status: str = Field(description="Account status (e.g., ACTIVE, PENDING, etc.)")
    broker: str = Field(description="Broker handling this account (e.g., ALPACA, APEX)")
    created_at: str = Field(
        description="When the account was created (ISO 8601 format)"
    )
    first_deposit_at: Optional[str] = Field(
        None, description="When the first deposit was made"
    )
    first_incoming_acats_transfer_at: Optional[str] = Field(
        None, description="When the first incoming ACATS transfer occurred"
    )
    first_deploy_at: Optional[str] = Field(
        None, description="When the first symphony was deployed"
    )
    first_position_created_at: Optional[str] = Field(
        None, description="When the first position was created"
    )
    has_queued_deploy: bool = Field(
        description="Whether there are any queued symphony deployments"
    )
    has_active_position: bool = Field(
        description="Whether the account has any active positions"
    )


class OptionsDetails(BaseModel):
    """Details for options contract holdings."""

    model_config = {"populate_by_name": True}

    underlying_asset_symbol: str = Field(
        description="Underlying asset symbol (e.g., AAPL)"
    )
    strike_price: float = Field(description="Strike price of the option contract")
    expiry: str = Field(description="Expiry date (YYYY-MM-DD format)")
    contract_type: str = Field(description="Type of option: CALL or PUT")


class Holding(BaseModel):
    """
    A position/holding in an account.

    Represents equities, crypto, or options positions.
    """

    model_config = {"populate_by_name": True}

    ticker: str = Field(description="Ticker symbol (e.g., AAPL, CRYPTO::BTC//USD)")
    quantity: float = Field(description="Number of shares/contracts/units held")
    asset_class: AssetClass = Field(
        description="Type of asset: CRYPTO, EQUITIES, or OPTIONS"
    )
    options_details: Optional[OptionsDetails] = Field(
        None, description="Details for options contracts (only for OPTIONS)"
    )


class InvestorDocumentCategory(str, Enum):
    """Categories of investor documents."""

    STATEMENT = "STATEMENT"
    CRYPTO_ACCOUNT_STATEMENT = "CRYPTO_ACCOUNT_STATEMENT"
    CRYPTO_TAX_FORM = "CRYPTO_TAX_FORM"
    TAX_FORM = "TAX_FORM"
    TRADE_CONFIRMATION = "TRADE_CONFIRMATION"


class InvestorDocument(BaseModel):
    """
    An investor document from the broker.

    Includes tax documents, account statements, trade confirmations, etc.
    """

    model_config = {"populate_by_name": True}

    category: InvestorDocumentCategory = Field(description="Category of the document")
    date: str = Field(description="Date of the document")
    id: str = Field(description="Unique identifier for the document")
    type: str = Field(description="Type of document")
    url: str = Field(description="URL to download the document")
    file_name: str = Field(description="File name of the document")
    tax_ids: Optional[List[str]] = Field(
        None, description="Tax IDs associated with the document"
    )


class AccountsListResponse(BaseModel):
    """Response from listing all accounts."""

    model_config = {"populate_by_name": True}

    accounts: List[Account] = Field(
        description="List of all accounts for the authenticated user"
    )
