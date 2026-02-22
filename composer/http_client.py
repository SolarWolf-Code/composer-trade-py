import logging
import time
import httpx
from typing import Any, Dict, Optional
from urllib.parse import urljoin

logger = logging.getLogger("composer")


class ComposerError(Exception):
    """Base exception for Composer SDK"""

    pass


class ComposerAPIError(ComposerError):
    """Exception raised for API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[httpx.Response] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.request_id = _get_request_id(response)


def _get_request_id(response: Optional[httpx.Response]) -> Optional[str]:
    """Extract request ID from response headers."""
    if response is None:
        return None
    for header in ("x-request-id", "x-cloud-trace-context", "x-correlation-id"):
        if header in response.headers:
            return response.headers[header]
    return None


def _convert_params(params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Convert params to ensure booleans are properly serialized as lowercase strings."""
    if params is None:
        return None
    result = {}
    for key, value in params.items():
        if isinstance(value, bool):
            result[key] = str(value).lower()
        elif isinstance(value, (list, tuple)):
            result[key] = value
        elif value is not None:
            result[key] = value
    return result if result else None


class HTTPClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = "https://api.composer.trade/",
        timeout: float = 30.0,
    ):
        self.base_url = base_url
        self._client = httpx.Client(
            timeout=timeout,
            headers=self._build_headers(api_key, api_secret),
        )

    def _build_headers(self, api_key: Optional[str], api_secret: Optional[str]) -> Dict[str, str]:
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
        url = urljoin(self.base_url, endpoint)
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
            )
        except httpx.RequestError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"Error: {method} {url} - {type(e).__name__} ({elapsed:.3f}s)")
            raise ComposerError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("GET", endpoint, params=_convert_params(params))

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> Any:
        return self.request("DELETE", endpoint)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "HTTPClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
