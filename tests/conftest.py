"""Test configuration and fixtures for aio-amazon-ads."""

import pytest
from unittest.mock import AsyncMock, MagicMock

import sys

sys.path.insert(0, "src")

from aio_amazon_ads import AmazonAdsClient
from aio_amazon_ads.exceptions import (
    AmazonAPIError,
    AuthenticationError,
    ThrottlingError,
    ValidationError,
)


@pytest.fixture
def mock_credentials():
    """Return mock credentials for testing."""
    return {
        "refresh_token": "test_refresh_token",
        "profile_id": "123456789",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
    }


@pytest.fixture
async def mock_client(mock_credentials):
    """Create a mock AmazonAdsClient for testing."""
    client = AmazonAdsClient(**mock_credentials)
    # Mock the HTTP client
    client._client = AsyncMock()
    # Mock token manager
    client._access_token = "mock_access_token"
    client._token_expires_at = float("inf")

    yield client

    # Cleanup
    await client.close()


@pytest.fixture
def mock_response():
    """Factory for creating mock HTTP responses."""

    def _make_response(status_code=200, json_data=None, headers=None):
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = json_data or {}
        response.headers = headers or {}
        response.text = str(json_data) if json_data else ""
        return response

    return _make_response
