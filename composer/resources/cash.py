"""Cash resource for cash-related endpoints."""

from ..models.cash import (
    ACHLimits,
    ACHRelationshipsResponse,
    ACHTransfer,
    RecurringDepositProjection,
    RecurringDepositsMeta,
    RecurringDepositsResponse,
    TaxWithholding,
    TransferConstraints,
)


class Cash:
    """Resource for cash-related endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_transfer_constraints(self) -> dict[str, TransferConstraints]:
        """
        Get all transfer constraints for a user's active accounts.

        Returns
        -------
            Map of account UUID to transfer constraints
        """
        response = self._client.get("/api/v1/cash/transfer-constraints")
        return {
            account_id: TransferConstraints.model_validate(constraints)
            for account_id, constraints in response.items()
        }

    def get_ach_relationships(
        self,
        include_plaid_account_details: bool,
    ) -> ACHRelationshipsResponse:
        """
        Get all ACH relationships for a user.

        Args:
            include_plaid_account_details: Whether to include Plaid account details

        Returns
        -------
            ACH relationships including bank accounts
        """
        params = {"include_plaid_account_details": include_plaid_account_details}
        response = self._client.get(
            "/api/v1/cash/ach-relationships",
            params=params,
        )
        return ACHRelationshipsResponse.model_validate(response)

    def get_ach_limits(self, account_id: str) -> ACHLimits:
        """
        Get limits to ACH transfers.

        Args:
            account_id: The account UUID

        Returns
        -------
            ACH transfer limits
        """
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/ach-limits",
        )
        return ACHLimits.model_validate(response)

    def get_tax_withholding_federal(self, account_id: str) -> TaxWithholding:
        """
        Get federal tax withholding requirements for Traditional IRA distributions.

        Args:
            account_id: The account UUID

        Returns
        -------
            Tax withholding information
        """
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/tax-withholding/federal",
        )
        return TaxWithholding.model_validate(response)

    def get_ach_transfers(
        self,
        account_id: str,
        year: int | None = None,
    ) -> list[ACHTransfer]:
        """
        Get an account's ACH transfers.

        Args:
            account_id: The account UUID
            year: Optional year to filter transfers

        Returns
        -------
            List of ACH transfers
        """
        params = {}
        if year is not None:
            params["year"] = year
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/ach-transfers",
            params=params if params else None,
        )
        return [ACHTransfer.model_validate(t) for t in response]

    def get_recurring_deposits(
        self,
        account_id: str,
        status: str | None = None,
        n: int = 10,
    ) -> RecurringDepositsResponse:
        """
        Get all recurring deposits for a broker account.

        Args:
            account_id: The account UUID
            status: Optional status filter (ACTIVE, CANCELED, etc.)
            n: Number of results to return

        Returns
        -------
            List of recurring deposits
        """
        params = {"n": n}
        if status:
            params["status"] = status
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/recurring-deposits",
            params=params,
        )
        return RecurringDepositsResponse.model_validate(response)

    def get_recurring_deposits_meta(self, account_id: str) -> RecurringDepositsMeta:
        """
        Get maximum recurring deposit amount for all frequencies.

        Args:
            account_id: The account UUID

        Returns
        -------
            Max deposit amounts by frequency
        """
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/recurring-deposits-meta",
        )
        return RecurringDepositsMeta.model_validate(response)

    def get_recurring_deposits_projection(
        self,
        account_id: str,
        amount: float,
        frequency: str,
    ) -> RecurringDepositProjection:
        """
        Project when a retirement account would reach its annual contribution limit.

        Args:
            account_id: The account UUID
            amount: Deposit amount
            frequency: Deposit frequency (WEEKLY, SEMIMONTHLY, MONTHLY, QUARTERLY)

        Returns
        -------
            Projection of when limit will be hit
        """
        params = {"amount": amount, "frequency": frequency}
        response = self._client.get(
            f"/api/v1/cash/accounts/{account_id}/recurring-deposits-projection",
            params=params,
        )
        return RecurringDepositProjection.model_validate(response)

    def get_all_recurring_deposits(
        self,
        n: int = 10,
        status: str | None = None,
    ) -> RecurringDepositsResponse:
        """
        Get all recurring deposits for a user.

        Args:
            n: Number of results to return
            status: Optional status filter (ACTIVE, CANCELED, etc.)

        Returns
        -------
            List of all recurring deposits across accounts
        """
        params = {"n": n}
        if status:
            params["status"] = status
        response = self._client.get(
            "/api/v1/cash/recurring-deposits",
            params=params,
        )
        return RecurringDepositsResponse.model_validate(response)
