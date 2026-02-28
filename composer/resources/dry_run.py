"""Dry run resource for dry-run endpoints."""


from ..models.dry_run import (
    AccountDryRunResult,
    DryRunRequest,
    TradePreviewRequest,
    TradePreviewResult,
)


class DryRun:
    """Resource for dry-run endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def create_dry_run(
        self,
        send_segment_event: bool = False,
        account_uuids: list[str] | None = None,
    ) -> list[AccountDryRunResult]:
        """
        Dry run rebalances for a specific user.

        Args:
            send_segment_event: Whether to send segment events
            account_uuids: Optional list of specific account UUIDs

        Returns
        -------
            List of dry run results for each account
        """
        request = DryRunRequest(
            account_uuids=account_uuids,
            send_segment_event=send_segment_event,
        )
        response = self._client.post(
            "/api/v1/dry-run",
            json=request.model_dump(exclude_none=True),
        )
        return [AccountDryRunResult.model_validate(r) for r in response]

    def create_trade_preview(
        self,
        symphony_id: str,
        amount: float | None = None,
        broker_account_uuid: str | None = None,
    ) -> TradePreviewResult:
        """
        Generate trade preview for a single symphony.

        Args:
            symphony_id: Unique identifier for the Symphony
            amount: Optional amount to preview
            broker_account_uuid: Optional specific account UUID

        Returns
        -------
            Trade preview result
        """
        request = TradePreviewRequest(
            amount=amount,
            broker_account_uuid=broker_account_uuid,
        )
        response = self._client.post(
            f"/api/v1/dry-run/trade-preview/{symphony_id}",
            json=request.model_dump(exclude_none=True),
        )
        return TradePreviewResult.model_validate(response)
