"""Accounts response models."""

from enum import StrEnum

from pydantic import BaseModel, Field


class AssetClass(StrEnum):
    """Asset class types."""

    CRYPTO = "CRYPTO"
    EQUITIES = "EQUITIES"
    OPTIONS = "OPTIONS"


class DirectTradableAssetClasses(BaseModel):
    """Asset classes available for direct trading."""

    model_config = {"populate_by_name": True}

    buy: list[AssetClass] = Field(
        description="Asset classes available for buying via direct trading"
    )
    sell: list[AssetClass] = Field(
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
    account_foreign_id: str | None = Field(
        None, description="Foreign ID from the broker (if applicable)"
    )
    account_type: str = Field(description="Type of account (e.g., INDIVIDUAL, IRA, etc.)")
    asset_classes: list[AssetClass] = Field(description="Asset classes supported by this account")
    direct_tradable_asset_classes: DirectTradableAssetClasses = Field(
        description="Asset classes available for direct buy/sell trading"
    )
    symphony_tradable_asset_classes: list[AssetClass] = Field(
        description="Asset classes available for Symphony automation"
    )
    account_number: str | None = Field(None, description="Account number (if available)")
    status: str = Field(description="Account status (e.g., ACTIVE, PENDING, etc.)")
    broker: str = Field(description="Broker handling this account (e.g., ALPACA, APEX)")
    created_at: str = Field(description="When the account was created (ISO 8601 format)")
    first_deposit_at: str | None = Field(None, description="When the first deposit was made")
    first_incoming_acats_transfer_at: str | None = Field(
        None, description="When the first incoming ACATS transfer occurred"
    )
    first_deploy_at: str | None = Field(None, description="When the first symphony was deployed")
    first_position_created_at: str | None = Field(
        None, description="When the first position was created"
    )
    is_legacy_crypto_only_account: bool | None = Field(
        None, description="Whether this is a legacy crypto-only account"
    )
    has_queued_deploy: bool = Field(description="Whether there are any queued symphony deployments")
    has_active_position: bool = Field(description="Whether the account has any active positions")


class OptionsDetails(BaseModel):
    """Details for options contract holdings."""

    model_config = {"populate_by_name": True}

    underlying_asset_symbol: str = Field(description="Underlying asset symbol (e.g., AAPL)")
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
    asset_class: AssetClass = Field(description="Type of asset: CRYPTO, EQUITIES, or OPTIONS")
    options_details: OptionsDetails | None = Field(
        None, description="Details for options contracts (only for OPTIONS)"
    )


class InvestorDocumentCategory(StrEnum):
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
    tax_ids: list[str] | None = Field(None, description="Tax IDs associated with the document")


class AccountsListResponse(BaseModel):
    """Response from listing all accounts."""

    model_config = {"populate_by_name": True}

    accounts: list[Account] = Field(description="List of all accounts for the authenticated user")


class AccountType(StrEnum):
    """Account types available for creation."""

    INDIVIDUAL = "INDIVIDUAL"
    ROTH_IRA = "ROTH_IRA"
    TRADITIONAL_IRA = "TRADITIONAL_IRA"
    ROLLOVER_IRA = "ROLLOVER_IRA"


class FootprintPlaybook(BaseModel):
    """Footprint playbook for account creation."""

    model_config = {"populate_by_name": True}

    purpose: str
    playbook_key: str
    index: int


class AvailableAccountType(BaseModel):
    """Available account type for a specific region."""

    model_config = {"populate_by_name": True}

    account_type: AccountType
    asset_classes: list[AssetClass]
    options_trading_levels: list[int] | None = None
    footprint_kyc_completed: bool
    footprint_token: str | None = None
    footprint_playbook_key: str | None = None
    footprint_playbooks: list[FootprintPlaybook] = []


class SupportedRegionStates(BaseModel):
    """States supporting trading for a specific asset class."""

    model_config = {"populate_by_name": True}

    countries: list[str] = []
    states: dict[str, list[str]] = {}


class SupportedRegionsResponse(BaseModel):
    """Response from getting supported regions."""

    model_config = {"populate_by_name": True}

    EQUITIES: SupportedRegionStates
    CRYPTO: SupportedRegionStates


class Trade(BaseModel):
    """A historical trade record."""

    model_config = {"populate_by_name": True}

    order_id: str
    order_request_id: str | None = None
    status: str
    side: str | None = None
    symbol: str | None = None
    asset_class: AssetClass | None = None
    filled_avg_price: float | None = None
    filled_qty: float | None = None
    filled_notional: float | None = None
    created_at: str


class TradeVolumeResponse(BaseModel):
    """Response from getting trade volume."""

    model_config = {"populate_by_name": True}

    volume: float = Field(description="Total trade volume in the account")


class TradeHistoryItem(BaseModel):
    """A trade history item including option events."""

    model_config = {"populate_by_name": True}

    id: str
    status: str
    symbol: str | None = None
    asset_class: AssetClass | None = None
    unit_price: float | None = None
    qty: float | None = None
    net_amount: float | None = None
    created_at: str
    description: str | None = None
    activity_type: str
    side: str | None = None
    order_request_id: str | None = None


class Identity(BaseModel):
    """Account owner identity information."""

    model_config = {"populate_by_name": True}

    given_name: str
    middle_name: str | None = None
    family_name: str


class Address(BaseModel):
    """Postal address."""

    model_config = {"populate_by_name": True}

    street_address: list[str]
    city: str
    state: str | None = None
    postal_code: str
    country: str | None = None


class Contact(BaseModel):
    """Contact information."""

    model_config = {"populate_by_name": True}

    email_address: str
    phone_number: str | None = None
    address: Address


class IncomeRange(BaseModel):
    """Income range in USD."""

    model_config = {"populate_by_name": True}

    min: int
    max: int


class InvestorProfile(BaseModel):
    """Investor profile information."""

    model_config = {"populate_by_name": True}

    investment_objective: str | None = None
    annual_income_usd: IncomeRange
    total_net_worth_usd: IncomeRange


class TrustedContact(BaseModel):
    """Trusted contact information."""

    model_config = {"populate_by_name": True}

    given_name: str
    family_name: str
    email_address: str | None = None
    phone_number: str | None = None
    mailing_address: Address | None = None


class AccountInfo(BaseModel):
    """Basic account owner information."""

    model_config = {"populate_by_name": True}

    account_number: str | None = None
    account_type: str
    broker: str
    status: str | None = None
    broker_status: str | None = None
    identity: Identity
    contact: Contact
    investor_profile: InvestorProfile | None = None
    trusted_contact: TrustedContact | None = None
    pending_trusted_contact: bool | None = None


class BuyingPower(BaseModel):
    """Buying power information for an asset class."""

    model_config = {"populate_by_name": True}

    asset_class: AssetClass
    total_cash: float
    total_unallocated_cash: float
    cash_reserved_for_options_contracts: float
    pending_deploys_cash: float
    pending_withdrawals: float | None = None
    pending_net_deposits: float | None = None
    buying_power: float
    symphony_buying_power: float
    direct_trading_buying_power: float
    direct_trading_daytrading_buying_power: float
    pattern_day_trader_eligible: bool
    pattern_day_trader: bool
    daytrading_blocked: bool
    daytrade_margin_call_protection_on_entry: bool
    daytrade_margin_call_protection_on_exit: bool
    daytrading_buying_power: float | None = None
    current_equity_for_dtbp: float | None = None
    sod_equity_for_dtbp: float | None = None
    buying_power_constrained_when_daytrading: bool
