"""Trading resource for trading-related endpoints."""

from ..models.trading import (
    CreateOrderRequest,
    CreateOrderResponse,
    ExercisePreviewResponse,
    ExerciseResponse,
    ModifyOrderRequest,
    OrderRequest,
    OrderRequestsResponse,
    OrderType,
    PositionIntent,
    TimeInForce,
    TradingPeriodResponse,
)


class Trading:
    """Resource for trading-related endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_trading_period(self) -> TradingPeriodResponse:
        """
        Get the trading period for the authenticated user.

        Returns
        -------
            Trading period information for CRYPTO, EQUITIES, and OPTIONS
        """
        response = self._client.get("/api/v1/trading-period")
        return TradingPeriodResponse.model_validate(response)

    def get_order_requests(
        self,
        account_id: str,
        limit: int | None = None,
        status: str | None = None,
    ) -> OrderRequestsResponse:
        """
        Get order requests for an account.

        Args:
            account_id: Unique identifier (UUID) of the account
            limit: Maximum number of results
            status: Filter by status (e.g., 'QUEUED,OPEN,IN_PROGRESS')

        Returns
        -------
            List of order requests
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if status:
            params["status"] = status
        response = self._client.get(
            f"/api/v1/trading/accounts/{account_id}/order-requests",
            params=params if params else None,
        )
        return OrderRequestsResponse.model_validate(response)

    def get_order_request(
        self,
        account_id: str,
        order_request_id: str,
    ) -> OrderRequest:
        """
        Get a single order request.

        Args:
            account_id: Unique identifier (UUID) of the account
            order_request_id: Unique identifier for the order request

        Returns
        -------
            Details of the specified order request
        """
        response = self._client.get(
            f"/api/v1/trading/accounts/{account_id}/order-requests/{order_request_id}"
        )
        return OrderRequest.model_validate(response)

    def create_order_request(
        self,
        account_id: str,
        type: OrderType | str,
        symbol: str,
        time_in_force: TimeInForce | str,
        notional: float | None = None,
        quantity: float | None = None,
        position_intent: PositionIntent | str | None = None,
        limit_price: float | None = None,
        stop_price: float | None = None,
        client_order_id: str | None = None,
    ) -> CreateOrderResponse:
        """
        Create a new order request.

        Args:
            account_id: Unique identifier (UUID) of the account
            type: Order type (MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP)
            symbol: Symbol to trade
            time_in_force: Time in force (GTC, DAY, IOC, FOK, OPG, CLS)
            notional: Notional amount (required if quantity not provided)
            quantity: Quantity (required if notional not provided)
            position_intent: Position intent for options (BUY_TO_OPEN, etc.)
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders
            client_order_id: Optional client-generated order ID

        Returns
        -------
            Created order details
        """
        request = CreateOrderRequest(
            type=type if isinstance(type, OrderType) else OrderType(type),
            symbol=symbol,
            time_in_force=time_in_force
            if isinstance(time_in_force, TimeInForce)
            else TimeInForce(time_in_force),
            notional=notional,
            quantity=quantity,
            position_intent=position_intent
            if position_intent is None or isinstance(position_intent, PositionIntent)
            else PositionIntent(position_intent),
            limit_price=limit_price,
            stop_price=stop_price,
            client_order_id=client_order_id,
        )
        response = self._client.post(
            f"/api/v1/trading/accounts/{account_id}/order-requests",
            json=request.model_dump(exclude_none=True),
        )
        return CreateOrderResponse.model_validate(response)

    def delete_order_request(
        self,
        account_id: str,
        order_request_id: str,
    ) -> None:
        """
        Cancel an order request that has not executed yet.

        Args:
            account_id: Unique identifier (UUID) of the account
            order_request_id: Unique identifier for the order request
        """
        self._client.delete(
            f"/api/v1/trading/accounts/{account_id}/order-requests/{order_request_id}"
        )

    def modify_order_request(
        self,
        account_id: str,
        order_request_id: str,
        client_order_id: str | None = None,
        limit_price: float | None = None,
        quantity: float | None = None,
    ) -> None:
        """
        Modify an existing order request that has not executed yet.

        Args:
            account_id: Unique identifier (UUID) of the account
            order_request_id: Unique identifier for the order request
            client_order_id: ID for replacement order (idempotency key)
            limit_price: New limit price
            quantity: New quantity
        """
        request = ModifyOrderRequest(
            client_order_id=client_order_id,
            limit_price=limit_price,
            quantity=quantity,
        )
        self._client.patch(
            f"/api/v1/trading/accounts/{account_id}/order-requests/{order_request_id}",
            json=request.model_dump(exclude_none=True),
        )

    def exercise_option(
        self,
        account_id: str,
        symbol: str,
    ) -> ExerciseResponse:
        """
        Exercise an option contract position.

        Args:
            account_id: Unique identifier (UUID) of the account
            symbol: Option symbol (e.g., OPTIONS::AAPL1234567890PC20240119//USD)

        Returns
        -------
            Exercise result
        """
        response = self._client.post(
            f"/api/v1/trading/accounts/{account_id}/options/exercise",
            json={"symbol": symbol},
        )
        return ExerciseResponse.model_validate(response)

    def preview_exercise_option(
        self,
        account_id: str,
        symbol: str,
    ) -> ExercisePreviewResponse:
        """
        Preview exercise of an option contract position.

        Args:
            account_id: Unique identifier (UUID) of the account
            symbol: Option symbol (e.g., OPTIONS::AAPL1234567890PC20240119//USD)

        Returns
        -------
            Exercise preview
        """
        response = self._client.post(
            f"/api/v1/trading/accounts/{account_id}/options/exercise/preview",
            json={"symbol": symbol},
        )
        return ExercisePreviewResponse.model_validate(response)

    def preview_order_request(
        self,
        account_id: str,
        type: str,
        symbol: str,
        time_in_force: str,
        notional: float | None = None,
        quantity: float | None = None,
        position_intent: str | None = None,
        limit_price: float | None = None,
        stop_price: float | None = None,
    ) -> ExercisePreviewResponse:
        """
        Preview an order request before placing it.

        Args:
            account_id: Unique identifier (UUID) of the account
            type: Order type (MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP)
            symbol: Symbol to trade
            time_in_force: Time in force (GTC, DAY, IOC, FOK, OPG, CLS)
            notional: Notional amount (required if quantity not provided)
            quantity: Quantity (required if notional not provided)
            position_intent: Position intent for options (BUY_TO_OPEN, etc.)
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders

        Returns
        -------
            Order preview
        """
        request = CreateOrderRequest(
            type=type if isinstance(type, OrderType) else OrderType(type),
            symbol=symbol,
            time_in_force=time_in_force
            if isinstance(time_in_force, TimeInForce)
            else TimeInForce(time_in_force),
            notional=notional,
            quantity=quantity,
            position_intent=position_intent
            if position_intent is None or isinstance(position_intent, PositionIntent)
            else PositionIntent(position_intent),
            limit_price=limit_price,
            stop_price=stop_price,
            client_order_id=None,
        )
        response = self._client.post(
            f"/api/v1/trading/accounts/{account_id}/order-requests/preview",
            json=request.model_dump(exclude_none=True),
        )
        return ExercisePreviewResponse.model_validate(response)
