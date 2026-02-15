"""Market data models."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ContractType(str, Enum):
    """Option contract type."""

    PUT = "PUT"
    CALL = "CALL"


class PayoffStatus(str, Enum):
    """Option payoff status."""

    IN_THE_MONEY = "IN_THE_MONEY"
    OUT_OF_THE_MONEY = "OUT_OF_THE_MONEY"
    AT_THE_MONEY = "AT_THE_MONEY"


class OptionSortBy(str, Enum):
    """Fields to sort options by."""

    SYMBOL = "symbol"
    EXPIRY = "expiry"
    STRIKE_PRICE = "strike_price"


class SortOrder(str, Enum):
    """Sort order."""

    ASC = "ASC"
    DESC = "DESC"


class OptionGreeks(BaseModel):
    """Option greeks."""

    model_config = {"populate_by_name": True}

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: Optional[float] = None


class QuotePrice(BaseModel):
    """Quote price information."""

    model_config = {"populate_by_name": True}

    price: Optional[float] = None
    size: Optional[float] = None


class OptionDayData(BaseModel):
    """Daily options data."""

    model_config = {"populate_by_name": True}

    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    volume: Optional[float] = None


class OptionContractDetails(BaseModel):
    """Details of an option contract."""

    model_config = {"populate_by_name": True}

    contract_type: ContractType
    shares_per_contract: float
    expiry: str
    strike_price: float


class OptionContract(BaseModel):
    """An options contract with market data."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: str
    underlying_asset_symbol: str
    contract_details: OptionContractDetails
    underlying_asset_price: float
    change_to_break_even: Optional[float] = None
    payoff_status: Optional[PayoffStatus] = None
    ask: QuotePrice
    bid: QuotePrice
    last_trade: QuotePrice
    todays_change: Optional[float] = None
    todays_change_percent: Optional[float] = None
    open_interest: float
    implied_volatility: Optional[float] = None
    delta_dollars: Optional[float] = None
    notional_value: float
    greeks: OptionGreeks
    day: OptionDayData


class OptionsChainResponse(BaseModel):
    """Response from getting options chain."""

    model_config = {"populate_by_name": True}

    results: List[OptionContract]
    next_cursor: Optional[str] = None


class OptionsContractResponse(BaseModel):
    """Response from getting options contract market data."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: str
    underlying_asset_symbol: str
    contract_details: OptionContractDetails
    underlying_asset_price: float
    change_to_break_even: Optional[float] = None
    payoff_status: Optional[PayoffStatus] = None
    ask: QuotePrice
    bid: QuotePrice
    last_trade: QuotePrice
    todays_change: Optional[float] = None
    todays_change_percent: Optional[float] = None
    open_interest: float
    implied_volatility: Optional[float] = None
    delta_dollars: Optional[float] = None
    notional_value: float
    greeks: OptionGreeks
    day: OptionDayData


class OptionsOverview(BaseModel):
    """Overview of options data for a symbol."""

    model_config = {"populate_by_name": True}

    symbol: str
    calendar: List[str] = []
