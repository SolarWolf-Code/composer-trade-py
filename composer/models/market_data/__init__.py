"""Market data models."""

from enum import StrEnum

import pandas as pd
from pydantic import BaseModel


class ContractType(StrEnum):
    """Option contract type."""

    PUT = "PUT"
    CALL = "CALL"


class PayoffStatus(StrEnum):
    """Option payoff status."""

    IN_THE_MONEY = "IN_THE_MONEY"
    OUT_OF_THE_MONEY = "OUT_OF_THE_MONEY"
    AT_THE_MONEY = "AT_THE_MONEY"


class OptionSortBy(StrEnum):
    """Fields to sort options by."""

    SYMBOL = "symbol"
    EXPIRY = "expiry"
    STRIKE_PRICE = "strike_price"


class SortOrder(StrEnum):
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
    rho: float | None = None


class QuotePrice(BaseModel):
    """Quote price information."""

    model_config = {"populate_by_name": True}

    price: float | None = None
    size: float | None = None


class OptionDayData(BaseModel):
    """Daily options data."""

    model_config = {"populate_by_name": True}

    close: float | None = None
    high: float | None = None
    low: float | None = None
    open: float | None = None
    volume: float | None = None


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
    change_to_break_even: float | None = None
    payoff_status: PayoffStatus | None = None
    ask: QuotePrice
    bid: QuotePrice
    last_trade: QuotePrice
    todays_change: float | None = None
    todays_change_percent: float | None = None
    open_interest: float
    implied_volatility: float | None = None
    delta_dollars: float | None = None
    notional_value: float
    greeks: OptionGreeks
    day: OptionDayData


class OptionsChainResponse(BaseModel):
    """Response from getting options chain."""

    model_config = {"populate_by_name": True}

    results: list[OptionContract]
    next_cursor: str | None = None


class OptionsContractResponse(BaseModel):
    """Response from getting options contract market data."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: str
    underlying_asset_symbol: str
    contract_details: OptionContractDetails
    underlying_asset_price: float
    change_to_break_even: float | None = None
    payoff_status: PayoffStatus | None = None
    ask: QuotePrice
    bid: QuotePrice
    last_trade: QuotePrice
    todays_change: float | None = None
    todays_change_percent: float | None = None
    open_interest: float
    implied_volatility: float | None = None
    delta_dollars: float | None = None
    notional_value: float
    greeks: OptionGreeks
    day: OptionDayData


class OptionsOverview(BaseModel):
    """Overview of options data for a symbol."""

    model_config = {"populate_by_name": True}

    symbol: str
    calendar: list[str] = []


# New models for additional market data endpoints


class MarketSnapshotPrice(BaseModel):
    """Price information for market snapshot."""

    model_config = {"populate_by_name": True}

    price: float | None = None
    size: float | None = None


class MarketSnapshot(BaseModel):
    """Snapshot of live market data for a symbol."""

    model_config = {"populate_by_name": True}

    symbol: str | None = None
    ask: MarketSnapshotPrice | None = None
    bid: MarketSnapshotPrice | None = None
    last_trade: MarketSnapshotPrice | None = None
    last_trade_size: float | None = None
    last_trade_time: str | None = None
    todays_change: float | None = None
    todays_change_percent: float | None = None
    market_status: str | None = None
    asset_type: str | None = None


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

    symbol: str | None = None
    data: list[BarData] = []


class AssetType(StrEnum):
    """Asset type for market overview."""

    CRYPTO = "CRYPTO"
    STOCK = "STOCK"
    ETF = "ETF"


class HQAddress(BaseModel):
    """Headquarters address."""

    model_config = {"populate_by_name": True}

    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    postal_code: str | None = None
    state: str | None = None


class MarketOverview(BaseModel):
    """Market overview response."""

    model_config = {"populate_by_name": True}

    symbol: str | None = None
    name: str | None = None
    asset_type: AssetType | None = None
    description: str | None = None
    hq: HQAddress | None = None
    sector: str | None = None
    industry: str | None = None
    website: str | None = None
    market_cap: float | None = None
    shares_outstanding: float | None = None


class TopMover(BaseModel):
    """Individual top mover."""

    model_config = {"populate_by_name": True}

    symbol: str
    name: str | None = None
    last_price: float
    todays_change: float
    todays_change_percent: float
    volume: float


class TopMoversResponse(BaseModel):
    """Response with top movers."""

    model_config = {"populate_by_name": True}

    top_movers: list[TopMover] = []


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
        """Get quote result for a symbol."""
        return QuoteResult(**self.__dict__.get(key, {}))

    def keys(self):
        """Return available symbols."""
        return self.__dict__.keys()

    def values(self):
        """Return quote values."""
        return self.__dict__.values()

    def items(self):
        """Return quote items."""
        return self.__dict__.items()
