"""Base HTTP client and authentication for Amazon Advertising API."""

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional

import httpx

from .exceptions import (
    AmazonAPIError,
    AuthenticationError,
    ThrottlingError,
    ValidationError,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://advertising-api.amazon.com"
TOKEN_URL = "https://api.amazon.com/auth/o2/token"


class BaseClient:
    """Base HTTP client with auth and retry logic."""

    def __init__(
        self,
        refresh_token: str,
        profile_id: str,
        client_id: str,
        client_secret: str,
    ):
        self.refresh_token = refresh_token
        self.profile_id = profile_id
        self.client_id = client_id
        self.client_secret = client_secret

        self._http: Optional[httpx.AsyncClient] = None
        self._http_lock = asyncio.Lock()
        self._token_lock = asyncio.Lock()
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0

    async def _get_http(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http is None:
            async with self._http_lock:
                if self._http is None:
                    self._http = httpx.AsyncClient(
                        base_url=BASE_URL,
                        timeout=httpx.Timeout(30.0, connect=5.0),
                        limits=httpx.Limits(
                            max_keepalive_connections=20,
                            max_connections=100,
                        ),
                    )
        return self._http

    async def close(self) -> None:
        """Close HTTP client."""
        async with self._http_lock:
            if self._http is not None:
                await self._http.aclose()
                self._http = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self._get_http()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _get_access_token(self) -> str:
        """Get valid access token, refresh if expired."""
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        # Use lock to prevent concurrent token refresh
        async with self._token_lock:
            # Double-check after acquiring lock
            if self._access_token and time.time() < self._token_expires_at - 60:
                return self._access_token
            return await self._refresh_token()

    async def _refresh_token(self) -> str:
        """Refresh OAuth token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )

            if response.status_code != 200:
                raise AuthenticationError(f"Token refresh failed: {response.text}")

            data = response.json()
            access_token = data["access_token"]
            self._access_token = access_token
            expires_in = data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in

            return access_token

    def _map_error(self, status_code: int, response_text: str) -> AmazonAPIError:
        """Map HTTP status to exception."""
        if status_code == 401:
            return AuthenticationError(f"Authentication failed: {response_text}")
        elif status_code == 429:
            return ThrottlingError(
                f"Rate limit exceeded: {response_text}",
                retry_after=60,
            )
        elif status_code == 400:
            return ValidationError(f"Validation error: {response_text}")
        else:
            return AmazonAPIError(f"API error {status_code}: {response_text}")

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json_data: Optional[Any] = None,
        retry_count: int = 3,
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        http = await self._get_http()
        access_token = await self._get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Amazon-Advertising-API-Scope": self.profile_id,
            "Content-Type": "application/json",
        }

        last_error: Optional[Exception] = None

        for attempt in range(retry_count):
            try:
                response = await http.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                )

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 2**attempt))
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    await asyncio.sleep(2**attempt)
                    continue

                if response.status_code >= 400:
                    raise self._map_error(response.status_code, response.text)

                return response

            except (httpx.NetworkError, httpx.TimeoutException) as e:
                last_error = e
                if attempt < retry_count - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise AmazonAPIError(f"Network error after {retry_count} retries: {e}")

        if last_error:
            raise AmazonAPIError(f"Request failed after {retry_count} retries: {last_error}")

        raise AmazonAPIError("Request failed")


class BaseService:
    """Base service for API endpoints."""

    def __init__(self, request: Callable):
        self._request = request
