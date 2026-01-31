"""Test core client functionality."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import sys

sys.path.insert(0, "src")

from amzn_ads import AmazonAdsClient
from amzn_ads.exceptions import AuthenticationError, ThrottlingError


class TestClientInitialization:
    """Test AmazonAdsClient initialization."""

    @pytest.mark.asyncio
    async def test_client_creation(self):
        """Test client can be created with valid credentials."""
        client = AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        )
        assert client.refresh_token == "test_token"
        assert client.profile_id == "123"
        await client.close()

    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Test client works as async context manager."""
        async with AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        ) as client:
            assert client._http is not None


class TestSPServiceAccess:
    """Test accessing SP services via namespacing."""

    @pytest.mark.asyncio
    async def test_access_sp_campaigns(self):
        """Test accessing SP campaigns service."""
        async with AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        ) as client:
            # Check that sp namespace exists
            assert hasattr(client, "sp")
            # Check that campaigns service exists
            assert hasattr(client.sp, "campaigns")
            assert hasattr(client.sp.campaigns, "list")
            assert hasattr(client.sp.campaigns, "create")

    @pytest.mark.asyncio
    async def test_access_sp_keywords(self):
        """Test accessing SP keywords service."""
        async with AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        ) as client:
            assert hasattr(client.sp, "keywords")
            assert hasattr(client.sp.keywords, "list")
            assert hasattr(client.sp.keywords, "create")
