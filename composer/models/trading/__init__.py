"""Trading models - request and response models for trading endpoints."""

from enum import StrEnum

from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    """Status of an order request."""

    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    OPEN = "OPEN"
    FILLED = "FILLED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"


class OrderSide(StrEnum):
    """Side of an order (buy or sell)."""

    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    """Type of order."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class TimeInForce(StrEnum):
    """Time in force for an order."""

    GTC = "GTC"  # Good Till Canceled
    DAY = "DAY"
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    OPG = "OPG"  # Opening
    CLS = "CLS"  # Closing


class PositionIntent(StrEnum):
    """Position intent for options orders."""

    BUY_TO_OPEN = "BUY_TO_OPEN"
    SELL_TO_OPEN = "SELL_TO_OPEN"
    BUY_TO_CLOSE = "BUY_TO_CLOSE"
    SELL_TO_CLOSE = "SELL_TO_CLOSE"


class AssetClass(StrEnum):
    """Asset class for trading."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"
    OPTIONS = "OPTIONS"


class OrderSource(StrEnum):
    """Source of the order."""

    USER_DIRECT_TRADE = "USER_DIRECT_TRADE"
    COMPOSER_ADMIN = "COMPOSER_ADMIN"


class OptionsDetails(BaseModel):
    """Details for options contracts."""

    underlying_asset_symbol: str = Field(description="Underlying asset symbol")
    strike_price: float = Field(description="Strike price of the option contract")
    expiry: str = Field(description="Expiry date (YYYY-MM-DD)")
    contract_type: str = Field(description="Type of option contract (PUT or CALL)")


class OrderRequest(BaseModel):
    """A trading order request."""

    order_request_id: str = Field(description="Unique identifier for the order request")
    name: str | None = Field(None, description="Name of the order")
    position_id: str | None = Field(None, description="Position ID associated with this order")
    status: OrderStatus | None = Field(None, description="Current status of the order")
    client_order_ids: list[str] | None = Field(
        None, description="IDs of broker orders submitted for this request"
    )
    asset_class: AssetClass | None = Field(None, description="Asset class of the symbol")
    side: OrderSide | None = Field(None, description="Side of the order (BUY or SELL)")
    type: OrderType | None = Field(None, description="Type of order")
    symbol: str | None = Field(None, description="Symbol to trade")
    time_in_force: TimeInForce | None = Field(None, description="Time in force")
    notional: float | None = Field(None, description="Notional amount (if using dollar amount)")
    quantity: float | None = Field(None, description="Quantity of shares/contracts")
    position_intent: PositionIntent | None = Field(
        None, description="Position intent (required for options)"
    )
    limit_price: float | None = Field(None, description="Limit price for limit orders")
    stop_price: float | None = Field(None, description="Stop price for stop orders")
    options_details: OptionsDetails | None = Field(
        None, description="Details for options contracts"
    )
    source: OrderSource | None = Field(None, description="Source of the order")
    created_at: str | None = Field(None, description="When the order was created (ISO 8601)")
    updated_at: str | None = Field(None, description="When the order was last updated (ISO 8601)")
    outcome_reason: str | None = Field(None, description="Reason for the order outcome")


class CreateOrderRequest(BaseModel):
    """Request to create a new order."""

    type: OrderType = Field(description="Type of order")
    symbol: str = Field(description="Symbol to trade")
    time_in_force: TimeInForce = Field(description="Time in force")
    notional: float | None = Field(
        None, description="Notional amount (required if quantity not provided)"
    )
    quantity: float | None = Field(None, description="Quantity (required if notional not provided)")
    position_intent: PositionIntent | None = Field(
        None, description="Position intent (required for options)"
    )
    limit_price: float | None = Field(None, description="Limit price for limit orders")
    stop_price: float | None = Field(None, description="Stop price for stop orders")
    client_order_id: str | None = Field(None, description="Optional client-generated order ID")


class CreateOrderResponse(BaseModel):
    """Response from creating a new order."""

    order_request_id: str = Field(description="Unique identifier for the order request")
    order_time: str = Field(description="When the order was created (ISO 8601)")
    commission: float | None = Field(None, description="Commission for the order")


class ListOrdersResponse(BaseModel):
    """Response containing list of orders."""

    order_requests: list[OrderRequest] = Field(description="List of order requests")


class TradingWindow(BaseModel):
    """Trading window for an asset class."""

    window_opens_at: str = Field(description="When the trading window opens")
    window_closes_at: str = Field(description="When the trading window closes")


class MarketHours(BaseModel):
    """Market hours for an asset class."""

    market_open: str = Field(description="Market open time")
    market_close: str = Field(description="Market close time")


class AssetClassTradingPeriod(BaseModel):
    """Trading period information for an asset class."""

    trading_day: bool = Field(description="Whether it's a trading day")
    trading_window: TradingWindow | None = Field(None, description="Trading window information")
    market_hours: MarketHours | None = Field(None, description="Market hours information")


class TradingPeriodResponse(BaseModel):
    """Response containing trading period information for all asset classes."""

    CRYPTO: AssetClassTradingPeriod = Field(description="Trading period for CRYPTO")
    EQUITIES: AssetClassTradingPeriod = Field(description="Trading period for EQUITIES")
    OPTIONS: AssetClassTradingPeriod = Field(description="Trading period for OPTIONS")


class OrderRequestsResponse(BaseModel):
    """Response containing list of order requests."""

    order_requests: list[OrderRequest] = Field(description="List of order requests")


class ModifyOrderRequest(BaseModel):
    """Request to modify an existing order."""

    client_order_id: str | None = Field(
        None, description="ID for replacement order (serves as idempotency key)"
    )
    limit_price: float | None = Field(None, description="New limit price")
    quantity: float | None = Field(None, description="New quantity")


class ExerciseAsset(BaseModel):
    """Asset delivered or received from exercise."""

    type: str = Field(description="Asset type (EQUITIES or CASH)")
    symbol: str = Field(description="Asset symbol")
    quantity: float = Field(description="Asset quantity")


class ExerciseResponse(BaseModel):
    """Response from exercising an option."""

    symbol: str = Field(description="Option symbol")
    quantity_exercised: float = Field(description="Quantity exercised")
    quantity_remaining: float = Field(description="Quantity remaining")


class ExerciseAffectedSymphony(BaseModel):
    """Symphony affected by exercise."""

    symphony_id: str = Field(description="Symphony ID")


class ExercisePreviewResponse(BaseModel):
    """Response from previewing option exercise."""

    symbol: str = Field(description="Option symbol")
    quantity: float = Field(description="Quantity to exercise")
    payoff_status: str = Field(
        description="Payoff status (IN_THE_MONEY, OUT_OF_THE_MONEY, AT_THE_MONEY)"
    )
    estimated_profit: float = Field(description="Estimated profit")
    fees: float = Field(description="Exercise fees")
    assets_delivered: list[ExerciseAsset] = Field(description="Assets to be delivered")
    assets_received: list[ExerciseAsset] = Field(description="Assets to be received")
    can_be_exercised: bool = Field(description="Whether exercise is possible")
    affected_symphonies: list[ExerciseAffectedSymphony] = Field(
        description="Symphonies affected by exercise"
    )
    reasons_preventing_exercise: list[str] = Field(description="Reasons preventing exercise")


__all__ = [
    "OrderStatus",
    "OrderSide",
    "OrderType",
    "TimeInForce",
    "PositionIntent",
    "AssetClass",
    "OrderSource",
    "OptionsDetails",
    "OrderRequest",
    "CreateOrderRequest",
    "CreateOrderResponse",
    "ListOrdersResponse",
    "TradingWindow",
    "MarketHours",
    "AssetClassTradingPeriod",
    "TradingPeriodResponse",
    "OrderRequestsResponse",
    "ModifyOrderRequest",
    "ExerciseAsset",
    "ExerciseResponse",
    "ExerciseAffectedSymphony",
    "ExercisePreviewResponse",
]
