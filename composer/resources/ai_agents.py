"""AI Agents resource for AI agent endpoints."""


from ..models.ai_agents import (
    AIAgent,
    AIAgentsResponse,
    AIExecutionsResponse,
)


class AIAgents:
    """Resource for AI agent endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def list(
        self,
        broker_account_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AIAgentsResponse:
        """
        List AI agents for a broker account.

        Args:
            broker_account_id: The broker account ID
            limit: Maximum number of results
            offset: Pagination offset

        Returns
        -------
            List of AI agents
        """
        params = {"broker_account_id": broker_account_id}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        response = self._client.get("/api/v1/ai-agents", params=params)
        return AIAgentsResponse.model_validate(response)

    def get(self, agent_id: str) -> AIAgent:
        """
        Get an AI agent by ID.

        Args:
            agent_id: The AI agent ID

        Returns
        -------
            AI agent details
        """
        response = self._client.get(f"/api/v1/ai-agents/{agent_id}")
        return AIAgent.model_validate(response)

    def get_executions(
        self,
        agent_id: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AIExecutionsResponse:
        """
        List executions for an AI agent.

        Args:
            agent_id: The AI agent ID
            limit: Maximum number of results
            offset: Pagination offset

        Returns
        -------
            List of agent executions
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        response = self._client.get(
            f"/api/v1/ai-agents/{agent_id}/executions",
            params=params if params else None,
        )
        return AIExecutionsResponse.model_validate(response)
