"""Trading models - request and response models for trading endpoints."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Status of an order request."""

    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    OPEN = "OPEN"
    FILLED = "FILLED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"


class OrderSide(str, Enum):
    """Side of an order (buy or sell)."""

    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Type of order."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class TimeInForce(str, Enum):
    """Time in force for an order."""

    GTC = "GTC"  # Good Till Canceled
    DAY = "DAY"
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    OPG = "OPG"  # Opening
    CLS = "CLS"  # Closing


class PositionIntent(str, Enum):
    """Position intent for options orders."""

    BUY_TO_OPEN = "BUY_TO_OPEN"
    SELL_TO_OPEN = "SELL_TO_OPEN"
    BUY_TO_CLOSE = "BUY_TO_CLOSE"
    SELL_TO_CLOSE = "SELL_TO_CLOSE"


class AssetClass(str, Enum):
    """Asset class for trading."""

    EQUITIES = "EQUITIES"
    CRYPTO = "CRYPTO"
    OPTIONS = "OPTIONS"


class OrderSource(str, Enum):
    """Source of the order."""

    USER_DIRECT_TRADE = "USER_DIRECT_TRADE"


class OptionsDetails(BaseModel):
    """Details for options contracts."""

    underlying_asset_symbol: str = Field(description="Underlying asset symbol")
    strike_price: float = Field(description="Strike price of the option contract")
    expiry: str = Field(description="Expiry date (YYYY-MM-DD)")
    contract_type: str = Field(description="Type of option contract (PUT or CALL)")


class OrderRequest(BaseModel):
    """A trading order request."""

    order_request_id: str = Field(description="Unique identifier for the order request")
    name: Optional[str] = Field(None, description="Name of the order")
    position_id: Optional[str] = Field(
        None, description="Position ID associated with this order"
    )
    status: Optional[OrderStatus] = Field(
        None, description="Current status of the order"
    )
    client_order_ids: Optional[List[str]] = Field(
        None, description="IDs of broker orders submitted for this request"
    )
    asset_class: Optional[AssetClass] = Field(
        None, description="Asset class of the symbol"
    )
    side: Optional[OrderSide] = Field(
        None, description="Side of the order (BUY or SELL)"
    )
    type: Optional[OrderType] = Field(None, description="Type of order")
    symbol: Optional[str] = Field(None, description="Symbol to trade")
    time_in_force: Optional[TimeInForce] = Field(None, description="Time in force")
    notional: Optional[float] = Field(
        None, description="Notional amount (if using dollar amount)"
    )
    quantity: Optional[float] = Field(None, description="Quantity of shares/contracts")
    position_intent: Optional[PositionIntent] = Field(
        None, description="Position intent (required for options)"
    )
    limit_price: Optional[float] = Field(
        None, description="Limit price for limit orders"
    )
    stop_price: Optional[float] = Field(None, description="Stop price for stop orders")
    options_details: Optional[OptionsDetails] = Field(
        None, description="Details for options contracts"
    )
    source: Optional[OrderSource] = Field(None, description="Source of the order")
    created_at: Optional[str] = Field(
        None, description="When the order was created (ISO 8601)"
    )
    updated_at: Optional[str] = Field(
        None, description="When the order was last updated (ISO 8601)"
    )
    outcome_reason: Optional[str] = Field(
        None, description="Reason for the order outcome"
    )


class CreateOrderRequest(BaseModel):
    """Request to create a new order."""

    type: OrderType = Field(description="Type of order")
    symbol: str = Field(description="Symbol to trade")
    time_in_force: TimeInForce = Field(description="Time in force")
    notional: Optional[float] = Field(
        None, description="Notional amount (required if quantity not provided)"
    )
    quantity: Optional[float] = Field(
        None, description="Quantity (required if notional not provided)"
    )
    position_intent: Optional[PositionIntent] = Field(
        None, description="Position intent (required for options)"
    )
    limit_price: Optional[float] = Field(
        None, description="Limit price for limit orders"
    )
    stop_price: Optional[float] = Field(None, description="Stop price for stop orders")
    client_order_id: Optional[str] = Field(
        None, description="Optional client-generated order ID"
    )


class CreateOrderResponse(BaseModel):
    """Response from creating a new order."""

    order_request_id: str = Field(description="Unique identifier for the order request")
    order_time: str = Field(description="When the order was created (ISO 8601)")
    commission: Optional[float] = Field(None, description="Commission for the order")


class ListOrdersResponse(BaseModel):
    """Response containing list of orders."""

    order_requests: List[OrderRequest] = Field(description="List of order requests")


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
]
