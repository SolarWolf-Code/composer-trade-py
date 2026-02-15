from typing import List, Optional, Any, Dict
from ..models.dry_run import (
    DryRunRequest,
    TradePreviewRequest,
    AccountDryRunResult,
    TradePreviewResult,
)


class DryRun:
    """Resource for dry run and trade preview endpoints."""

    def __init__(self, http_client):
        self.http_client = http_client

    def dry_run(
        self,
        account_uuids: Optional[List[str]] = None,
        send_segment_event: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Dry run rebalances for a specific user.

        Previews trades and rebalancing actions before execution across
        all accounts (or specific accounts if provided).

        Args:
            account_uuids: Optional list of account UUIDs to run dry run for.
                          If not provided, runs for all accounts.
            send_segment_event: Whether to send segment events (default False)

        Returns:
            List of dry run results for each account
        """
        request = DryRunRequest(
            account_uuids=account_uuids,
            send_segment_event=send_segment_event,
        )
        response = self.http_client.post(
            "/api/v0.1/dry-run",
            json=request.model_dump(exclude_none=True),
        )
        return response

    def trade_preview(
        self,
        symphony_id: str,
        amount: Optional[float] = None,
        broker_account_uuid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate trade preview for a single symphony.

        Args:
            symphony_id: UUID of the symphony
            amount: Optional specific amount to preview trades for
            broker_account_uuid: Optional specific account to preview for

        Returns:
            Trade preview result with recommended trades
        """
        request = TradePreviewRequest(
            amount=amount,
            broker_account_uuid=broker_account_uuid,
        )
        response = self.http_client.post(
            f"/api/v0.1/dry-run/trade-preview/{symphony_id}",
            json=request.model_dump(exclude_none=True),
        )
        return response
