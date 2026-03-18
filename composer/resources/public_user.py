"""Public User resource - public endpoints for user data."""

from ..http_client import HTTPClient
from ..models.user import ReferralCodeResponse


class PublicUser:
    """
    Public user endpoints (no authentication required).

    These endpoints provide read-only access to public user information.
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    def get_referral_code(self, user_sid: str) -> ReferralCodeResponse:
        """
        Get the referral code for a user.

        Args:
            user_sid: The user's SID (user identifier).

        Returns
        -------
            ReferralCodeResponse: The user's referral code.

        Raises
        ------
            ComposerAPIError: If the user is not found (404).

        Example:
            referral_code = client.public_user.get_referral_code("user-123")
            print(f"Referral code: {referral_code.referral_code}")
        """
        response = self._client.get(f"/api/v1/public/user/{user_sid}/referral-code")
        return ReferralCodeResponse.model_validate(response)
