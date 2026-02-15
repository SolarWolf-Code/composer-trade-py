import requests
from typing import Any, Dict, Optional
from urllib.parse import urljoin


class ComposerError(Exception):
    """Base exception for Composer SDK"""

    pass


class ComposerAPIError(ComposerError):
    """Exception raised for API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[requests.Response] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class HTTPClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = "https://api.composer.trade/",
    ):
        self.base_url = base_url
        self.session = requests.Session()

        # Build headers - auth headers only if credentials provided
        headers = {
            "User-Agent": "composer-trade-py",
            "Content-Type": "application/json",
        }

        if api_key:
            headers["x-api-key-id"] = api_key
        if api_secret:
            headers["authorization"] = f"Bearer {api_secret}"

        self.session.headers.update(headers)

    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            # Check for empty response content
            if not response.content:
                return None

            # Check content type for non-JSON responses
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()

            # Return text for CSV, plain text, etc.
            return response.text
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error {e.response.status_code}: {e.response.text}"
            raise ComposerAPIError(
                error_msg, status_code=e.response.status_code, response=e.response
            )
        except requests.exceptions.RequestException as e:
            raise ComposerError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> Any:
        return self.request("DELETE", endpoint)
