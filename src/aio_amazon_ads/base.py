"""Base HTTP client and authentication for Amazon Advertising API.

Supports multiple marketplaces:
- NA (North America): https://advertising-api.amazon.com
- EU (Europe): https://advertising-api-eu.amazon.com
- FE (Far East): https://advertising-api-fe.amazon.com
"""

import asyncio
import logging
import time
from collections.abc import Callable
from enum import Enum
from typing import Any

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from .exceptions import (
    AmazonAPIError,
    AuthenticationError,
    ThrottlingError,
    ValidationError,
)

logger = logging.getLogger(__name__)

TOKEN_URL = "https://api.amazon.com/auth/o2/token"


class Marketplace(Enum):
    """Amazon Advertising API marketplaces."""

    NA = "https://advertising-api.amazon.com"
    """North America (US, CA, MX, BR)"""

    EU = "https://advertising-api-eu.amazon.com"
    """Europe (UK, DE, FR, IT, ES, NL, AE, SE, PL, TR, EG, SA)"""

    FE = "https://advertising-api-fe.amazon.com"
    """Far East (JP, AU, SG, IN)"""


# Country code to marketplace mapping
COUNTRY_TO_MARKETPLACE: dict[str, Marketplace] = {
    # North America
    "US": Marketplace.NA,
    "CA": Marketplace.NA,
    "MX": Marketplace.NA,
    "BR": Marketplace.NA,
    # Europe
    "UK": Marketplace.EU,
    "GB": Marketplace.EU,
    "DE": Marketplace.EU,
    "FR": Marketplace.EU,
    "IT": Marketplace.EU,
    "ES": Marketplace.EU,
    "NL": Marketplace.EU,
    "AE": Marketplace.EU,
    "SE": Marketplace.EU,
    "PL": Marketplace.EU,
    "TR": Marketplace.EU,
    "EG": Marketplace.EU,
    "SA": Marketplace.EU,
    # Far East
    "JP": Marketplace.FE,
    "AU": Marketplace.FE,
    "SG": Marketplace.FE,
    "IN": Marketplace.FE,
}


class BaseClient:
    """Base HTTP client with auth and retry logic."""

    def __init__(
        self,
        refresh_token: str,
        profile_id: str,
        client_id: str,
        client_secret: str,
        marketplace: Marketplace = Marketplace.NA,
    ):
        """Initialize Amazon Ads client.

        Args:
            refresh_token: OAuth refresh token
            profile_id: Amazon Advertising profile ID
            client_id: LWA client ID
            client_secret: LWA client secret
            marketplace: API marketplace (NA, EU, FE). Defaults to NA.
        """
        self.refresh_token = refresh_token
        self.profile_id = profile_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.marketplace = marketplace
        self.base_url = marketplace.value

        self._http: httpx.AsyncClient | None = None
        self._http_lock = asyncio.Lock()
        self._token_lock = asyncio.Lock()
        self._access_token: str | None = None
        self._token_expires_at: float = 0

    async def _get_http(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http is None:
            async with self._http_lock:
                if self._http is None:
                    self._http = httpx.AsyncClient(
                        base_url=self.base_url,
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
        if self._access_token and time.time() < self._token_expires_at - 300:
            return self._access_token

        # Use lock to prevent concurrent token refresh
        async with self._token_lock:
            # Double-check after acquiring lock
            if self._access_token and time.time() < self._token_expires_at - 300:
                return self._access_token
            # Invalidate token before refresh to prevent deadlock
            self._access_token = None
            return await self._refresh_token()

    async def _refresh_token(self) -> str:
        """Refresh OAuth token."""
        logger.debug("Token refresh started")

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
                logger.error(f"Token refresh failed: {response.status_code} - {response.text}")
                raise AuthenticationError(f"Token refresh failed: {response.text}")

            data = response.json()
            access_token = data["access_token"]
            self._access_token = access_token
            expires_in = data.get("expires_in", 3600)
            # Subtract 5 minutes for clock skew safety
            self._token_expires_at = time.time() + expires_in - 300

            logger.debug("Token refresh succeeded")
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=60),
        retry=retry_if_exception_type(
            (ThrottlingError, httpx.NetworkError, httpx.TimeoutException)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_data: Any | None = None,
    ) -> httpx.Response:
        """Make HTTP request with automatic retry via tenacity."""
        logger.debug(f"Request: {method} {path} params={params}")

        http = await self._get_http()
        access_token = await self._get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Amazon-Advertising-API-Scope": self.profile_id,
            "Content-Type": "application/json",
        }

        response = await http.request(
            method=method,
            url=path,
            params=params,
            json=json_data,
            headers=headers,
        )

        # Log request ID for debugging
        request_id = response.headers.get("X-Amzn-Request-Id")
        logger.debug(f"Response: {response.status_code} (X-Amzn-Request-Id: {request_id})")

        # Handle 401 - invalidate token and let tenacity retry
        if response.status_code == 401:
            logger.error(
                f"Authentication failed (X-Amzn-Request-Id: {request_id}): {response.text}"
            )
            self._access_token = None
            raise AuthenticationError(f"Authentication failed: {response.text}")

        # Handle 429 - raise ThrottlingError for tenacity to catch
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            logger.warning(
                f"Rate limited (X-Amzn-Request-Id: {request_id}), retry after {retry_after}s"
            )
            raise ThrottlingError("Rate limited", retry_after=retry_after)

        # Handle other errors
        if response.status_code >= 400:
            logger.error(
                f"API error {response.status_code} (X-Amzn-Request-Id: {request_id}): {response.text}"
            )
            raise self._map_error(response.status_code, response.text)

        return response


class BaseService:
    """Base service for API endpoints."""

    def __init__(self, request: Callable):
        self._request = request
