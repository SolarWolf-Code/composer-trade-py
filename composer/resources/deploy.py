"""Deploy resource for deployment-related endpoints."""

from typing import Optional
from ..models.deploy import (
    MarketHoursResponse,
    DeploySymphoniesResponse,
    DeploysResponse,
    Deploy as DeployModel,
    DeployActionResponse,
)


class DeployResource:
    """Resource for deploy-related endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_market_hours(self) -> MarketHoursResponse:
        """
        Get market hours schedule for the upcoming week.

        Returns:
            Market hours schedule including open/close times for each day
        """
        response = self._client.get("/api/v1/deploy/market-hours")
        return MarketHoursResponse.model_validate(response)

    def get_deploy_symphonies(
        self,
        account_id: str,
        asset_class: Optional[str] = None,
    ) -> DeploySymphoniesResponse:
        """
        Get metadata for symphonies which have new invests pending.

        Args:
            account_id: Unique identifier (UUID) of the account
            asset_class: Deprecated.

        Returns:
            List of symphonies with pending invests
        """
        params = {}
        if asset_class:
            params["asset_class"] = asset_class
        response = self._client.get(
            f"/api/v1/deploy/accounts/{account_id}/deploy-symphonies",
            params=params if params else None,
        )
        return DeploySymphoniesResponse.model_validate(response)

    def get_deploys(
        self,
        account_id: str,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> DeploysResponse:
        """
        Get all deploy details for an account.

        Args:
            account_id: Unique identifier (UUID) of the account
            status: Filter by status (QUEUED, CANCELED, SUCCEEDED, FAILED, REJECTED, EXPIRED)
            limit: Maximum number of results

        Returns:
            List of deploys for the account
        """
        params = {}
        if status:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        response = self._client.get(
            f"/api/v1/deploy/accounts/{account_id}/deploys",
            params=params if params else None,
        )
        return DeploysResponse.model_validate(response)

    def get_deploy(
        self,
        account_id: str,
        deploy_id: str,
    ) -> DeployModel:
        """
        Get a specific deploy's details.

        Args:
            account_id: Unique identifier (UUID) of the account
            deploy_id: Unique identifier for the deployment operation

        Returns:
            Details of the specified deploy
        """
        response = self._client.get(f"/api/v1/deploy/accounts/{account_id}/deploys/{deploy_id}")
        return DeployModel.model_validate(response)

    def delete_deploy(
        self,
        account_id: str,
        deploy_id: str,
    ) -> None:
        """
        Cancel a pending deploy.

        Args:
            account_id: Unique identifier (UUID) of the account
            deploy_id: Unique identifier for the deployment operation
        """
        self._client.delete(f"/api/v1/deploy/accounts/{account_id}/deploys/{deploy_id}")

    def go_to_cash(
        self,
        account_id: str,
        symphony_id: str,
    ) -> DeployActionResponse:
        """
        Sell all assets in a symphony, leaving proceeds in cash.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony

        Returns:
            Information about the deploy
        """
        response = self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/go-to-cash"
        )
        return DeployActionResponse.model_validate(response)

    def invest(
        self,
        account_id: str,
        symphony_id: str,
        amount: float,
    ) -> DeployActionResponse:
        """
        Invest cash into a Symphony.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony
            amount: Amount of cash to invest (in USD)

        Returns:
            Information about the deploy
        """
        response = self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/invest",
            json={"amount": amount},
        )
        return DeployActionResponse.model_validate(response)

    def liquidate(
        self,
        account_id: str,
        symphony_id: str,
    ) -> DeployActionResponse:
        """
        Liquidate a symphony entirely.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony

        Returns:
            Information about the deploy
        """
        response = self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/liquidate"
        )
        return DeployActionResponse.model_validate(response)

    def rebalance(
        self,
        account_id: str,
        symphony_id: str,
        rebalance_request_uuid: str,
    ) -> DeployActionResponse:
        """
        Rebalance a symphony NOW.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony
            rebalance_request_uuid: UUID for the rebalance request

        Returns:
            Information about the deploy
        """
        response = self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/rebalance",
            json={"rebalance_request_uuid": rebalance_request_uuid},
        )
        return DeployActionResponse.model_validate(response)

    def skip_automated_rebalance(
        self,
        account_id: str,
        symphony_id: str,
        skip: bool,
    ) -> None:
        """
        Skip automated rebalancing.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony
            skip: Whether to skip the next automated rebalance
        """
        self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/skip-automated-rebalance",
            json={"skip": skip},
        )

    def withdraw(
        self,
        account_id: str,
        symphony_id: str,
        amount: float,
    ) -> DeployActionResponse:
        """
        Withdraw cash from a Symphony.

        Args:
            account_id: Unique identifier (UUID) of the account
            symphony_id: Unique identifier for the Symphony
            amount: Amount of cash to withdraw (in USD)

        Returns:
            Information about the deploy
        """
        response = self._client.post(
            f"/api/v1/deploy/accounts/{account_id}/symphonies/{symphony_id}/withdraw",
            json={"amount": amount},
        )
        return DeployActionResponse.model_validate(response)
