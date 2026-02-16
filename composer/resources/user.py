"""User resource for user-related endpoints."""

from ..models.user import (
    JWTResponse,
    UserProfile,
    AgreementStatusResponse,
)


class User:
    """Resource for user-related endpoints."""

    def __init__(self, http_client):
        self._client = http_client

    def get_jwt(self) -> JWTResponse:
        """
        Get a user JWT.

        Returns:
            JWT token response
        """
        response = self._client.get("/api/v1/user/jwt")
        return JWTResponse.model_validate(response)

    def get_profile(self) -> UserProfile:
        """
        Get a user profile.

        Returns:
            User profile information
        """
        response = self._client.get("/api/v1/user/profile")
        return UserProfile.model_validate(response)

    def get_agreement_status(self, agreement_id: str) -> AgreementStatusResponse:
        """
        Check if a user has accepted a specific agreement.

        Args:
            agreement_id: The agreement ID to check

        Returns:
            Whether the user has agreed to the agreement
        """
        response = self._client.get(f"/api/v1/user/agreement-status/{agreement_id}")
        return AgreementStatusResponse.model_validate(response)
