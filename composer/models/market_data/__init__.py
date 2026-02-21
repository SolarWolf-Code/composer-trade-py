"""Market data models."""

from typing import List, Optional, Dict

import pandas as pd
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


# New models for additional market data endpoints


class MarketSnapshotPrice(BaseModel):
    """Price information for market snapshot."""

    model_config = {"populate_by_name": True}

    price: Optional[float] = None
    size: Optional[float] = None


class MarketSnapshot(BaseModel):
    """Snapshot of live market data for a symbol."""

    model_config = {"populate_by_name": True}

    symbol: Optional[str] = None
    ask: Optional[MarketSnapshotPrice] = None
    bid: Optional[MarketSnapshotPrice] = None
    last_trade: Optional[MarketSnapshotPrice] = None
    last_trade_size: Optional[float] = None
    last_trade_time: Optional[str] = None
    todays_change: Optional[float] = None
    todays_change_percent: Optional[float] = None
    market_status: Optional[str] = None
    asset_type: Optional[str] = None


class BarData(BaseModel):
    """Individual bar data point."""

    model_config = {"populate_by_name": True}

    volume: float
    open: float
    close: float
    high: float
    low: float
    volume_weighted_average_price: float
    timestamp: int


class CustomBars(BaseModel):
    """Custom bars market data response."""

    model_config = {"populate_by_name": True}

    symbol: Optional[str] = None
    data: List[BarData] = []


class AssetType(str, Enum):
    """Asset type for market overview."""

    CRYPTO = "CRYPTO"
    STOCK = "STOCK"
    ETF = "ETF"


class HQAddress(BaseModel):
    """Headquarters address."""

    model_config = {"populate_by_name": True}

    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None


class MarketOverview(BaseModel):
    """Market overview response."""

    model_config = {"populate_by_name": True}

    symbol: Optional[str] = None
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    description: Optional[str] = None
    hq: Optional[HQAddress] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    market_cap: Optional[float] = None
    shares_outstanding: Optional[float] = None


class TopMover(BaseModel):
    """Individual top mover."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: Optional[str] = None
    last_price: float
    todays_change: float
    todays_change_percent: float
    volume: float


class TopMoversResponse(BaseModel):
    """Response with top movers."""

    model_config = {"populate_by_name": True}

    top_movers: List[TopMover] = []


class QuoteResult(BaseModel):
    """Quote result for a single symbol."""

    model_config = {"populate_by_name": True}

    name: str
    price: float
    previous_price: float


class _QuoteDict(dict):
    """Dict subclass with .df property for quote data."""

    @property
    def df(self) -> pd.DataFrame:
        """Convert quotes to DataFrame."""
        if not self:
            return pd.DataFrame()

        data = []
        for ticker, quote in self.items():
            data.append(
                {
                    "ticker": ticker,
                    "name": quote.name,
                    "price": quote.price,
                    "previous_price": quote.previous_price,
                }
            )

        df = pd.DataFrame(data).set_index("ticker")
        return df


class QuotesResponse(BaseModel):
    """Response from getting quotes."""

    model_config = {"populate_by_name": True}

    def __getitem__(self, key: str) -> QuoteResult:
        return QuoteResult(**self.__dict__.get(key, {}))

    def __iter__(self):
        return iter(self.__dict__.keys())

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()
