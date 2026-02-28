"""HTTP Client for Composer API.

This module provides the HTTP client for making requests to the Composer API.
"""

import logging
import time
from typing import Any
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger("composer")


class RetryConfig(BaseModel):
    """Configuration for retry behavior."""

    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    rate_limit_wait: float = Field(
        default=10.0, description="Initial seconds to wait on 429 responses"
    )
    server_error_wait: float = Field(
        default=3.0, description="Initial seconds to wait on 500, 502, 503, 504 responses"
    )
    exponential_base: float = Field(
        default=2.0, description="Base for exponential backoff multiplier"
    )
    retry_statuses: set[int] = Field(
        default={429, 500, 502, 503, 504}, description="HTTP status codes that trigger a retry"
    )


class ComposerError(Exception):
    """Base exception for Composer SDK."""

    pass


class ComposerAPIError(ComposerError):
    """Exception raised for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: httpx.Response | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.request_id = _get_request_id(response)


def _get_request_id(response: httpx.Response | None) -> str | None:
    """Extract request ID from response headers."""
    if response is None:
        return None
    for header in ("x-request-id", "x-cloud-trace-context", "x-correlation-id"):
        if header in response.headers:
            return response.headers[header]
    return None


def _convert_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Convert params to ensure booleans are properly serialized as lowercase strings."""
    if params is None:
        return None
    result = {}
    for key, value in params.items():
        if isinstance(value, bool):
            result[key] = str(value).lower()
        elif isinstance(value, (list, tuple)) or value is not None:
            result[key] = value
    return result if result else None


class HTTPClient:
    """HTTP client for making requests to the Composer API.

    This client handles authentication, request serialization, and response
    parsing for all API endpoints.

    Args:
        api_key: The API Key ID for authentication.
        api_secret: The API Secret Key for authentication.
        base_url: Base URL for the API (default: https://api.composer.trade/).
        timeout: Request timeout in seconds (default: 30.0).
    """

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        base_url: str = "https://api.composer.trade/",
        timeout: float = 30.0,
        retry_config: RetryConfig | None = None,
    ):
        self.base_url = base_url
        self.retry_config = retry_config
        self._client = httpx.Client(
            timeout=timeout,
            headers=self._build_headers(api_key, api_secret),
        )

    def _build_headers(self, api_key: str | None, api_secret: str | None) -> dict[str, str]:
        headers = {
            "User-Agent": "composer-trade-py",
            "x-origin": "public-api",
            "Content-Type": "application/json",
        }
        if api_key:
            headers["x-api-key-id"] = api_key
        if api_secret:
            headers["authorization"] = f"Bearer {api_secret}"
        return headers

    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an HTTP request to the API with optional retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            endpoint: API endpoint path.
            **kwargs: Additional arguments to pass to httpx.

        Returns
        -------
            Parsed response data (JSON dict, text, or None).
        """
        url = urljoin(self.base_url, endpoint)

        if self.retry_config is None:
            return self._execute_request(method, url, **kwargs)

        max_retries = self.retry_config.max_retries
        exponential_base = self.retry_config.exponential_base
        last_exception: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                return self._execute_request(method, url, **kwargs)
            except ComposerAPIError as e:
                if e.status_code not in self.retry_config.retry_statuses or attempt >= max_retries:
                    raise

                last_exception = e
                base_wait = (
                    self.retry_config.rate_limit_wait
                    if e.status_code == 429
                    else self.retry_config.server_error_wait
                )
                wait_time = base_wait * (exponential_base**attempt)
                logger.debug(
                    f"Retry {attempt + 1}/{max_retries}: {method} {url} - {e.status_code}, "
                    f"waiting {wait_time:.1f}s..."
                )
                time.sleep(wait_time)

        if last_exception:
            raise last_exception

    def _execute_request(self, method: str, url: str, **kwargs) -> Any:
        """Execute a single HTTP request.

        Args:
            method: HTTP method.
            url: Full URL.
            **kwargs: Additional arguments to pass to httpx.

        Returns
        -------
            Parsed response data (JSON dict, text, or None).
        """
        start_time = time.perf_counter()
        try:
            logger.debug(f"Request: {method} {url}")
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()

            elapsed = time.perf_counter() - start_time
            logger.debug(f"Response: {method} {url} - {response.status_code} ({elapsed:.3f}s)")

            if not response.content:
                return None

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()

            return response.text
        except httpx.HTTPStatusError as e:
            elapsed = time.perf_counter() - start_time
            request_id = _get_request_id(e.response)
            request_id_str = f" [request_id: {request_id}]" if request_id else ""
            logger.error(
                f"Error: {method} {url} - {e.response.status_code} ({elapsed:.3f}s){request_id_str}"
            )
            error_msg = f"HTTP Error {e.response.status_code}: {e.response.text}{request_id_str}"
            raise ComposerAPIError(
                error_msg, status_code=e.response.status_code, response=e.response
            ) from e
        except httpx.RequestError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"Error: {method} {url} - {type(e).__name__} ({elapsed:.3f}s)")
            raise ComposerError(f"Request failed: {str(e)}") from e

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Make a GET request.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns
        -------
            Parsed response data.
        """
        return self.request("GET", endpoint, params=_convert_params(params))

    def post(self, endpoint: str, json: dict[str, Any] | None = None) -> Any:
        """Make a POST request.

        Args:
            endpoint: API endpoint path.
            json: JSON request body.

        Returns
        -------
            Parsed response data.
        """
        return self.request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict[str, Any] | None = None) -> Any:
        """Make a PUT request.

        Args:
            endpoint: API endpoint path.
            json: JSON request body.

        Returns
        -------
            Parsed response data.
        """
        return self.request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: dict[str, Any] | None = None) -> Any:
        """Make a PATCH request.

        Args:
            endpoint: API endpoint path.
            json: JSON request body.

        Returns
        -------
            Parsed response data.
        """
        return self.request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> Any:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint path.

        Returns
        -------
            Parsed response data.
        """
        return self.request("DELETE", endpoint)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "HTTPClient":
        """Enter the context manager.

        Returns
        -------
            Self.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and close the HTTP client."""
        self.close()
