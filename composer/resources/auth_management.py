"""Auth Management resource for authentication-related endpoints."""

from ..models.accounts import (
    ApiKeysResponse,
)


class AuthManagement:
    """Resource for auth-management endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def list_api_keys(self) -> ApiKeysResponse:
        """
        List API keys for the authenticated user.

        Returns
        -------
            List of API keys
        """
        response = self._client.get("/api/v1/auth-management/api-keys/")
        return ApiKeysResponse.model_validate(response)

    # Note: create_api_key is intentionally not implemented because it destroys
    # the existing API key (users can only have one key at a time)
