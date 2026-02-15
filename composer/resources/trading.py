from typing import List
from ..models.trading import (
    CreateOrderRequest,
    CreateOrderResponse,
    OrderRequest,
    ListOrdersResponse,
)


class Trading:
    def __init__(self, http_client):
        self.http_client = http_client

    def list_orders(self, account_id: str) -> List[OrderRequest]:
        """
        List all orders for an account.

        Args:
            account_id: UUID of the account

        Returns:
            List of OrderRequest objects
        """
        response = self.http_client.get(
            f"/api/v0.1/trading/accounts/{account_id}/order-requests"
        )
        validated = ListOrdersResponse.model_validate(response)
        return validated.order_requests

    def create_order(
        self, account_id: str, request: CreateOrderRequest
    ) -> CreateOrderResponse:
        """
        Create a new order.

        Args:
            account_id: UUID of the account
            request: Order creation request

        Returns:
            CreateOrderResponse with order_request_id and order_time

        Example:
            from composer.models.trading import (
                CreateOrderRequest, OrderType, TimeInForce
            )

            order = client.trading.create_order(
                account_id="account-uuid",
                request=CreateOrderRequest(
                    type=OrderType.MARKET,
                    symbol="AAPL",
                    time_in_force=TimeInForce.DAY,
                    notional=1000.0
                )
            )
            print(f"Created order: {order.order_request_id} at {order.order_time}")
        """
        response = self.http_client.post(
            f"/api/v0.1/trading/accounts/{account_id}/order-requests",
            json=request.model_dump(exclude_none=True),
        )
        return CreateOrderResponse.model_validate(response)
