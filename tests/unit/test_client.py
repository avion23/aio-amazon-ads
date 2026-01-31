"""Test core client functionality."""

import pytest
import sys

sys.path.insert(0, "src")

from aio_amazon_ads import AmazonAdsClient
from aio_amazon_ads.exceptions import AuthenticationError, ThrottlingError


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


class TestTokenRefreshLock:
    """Test token refresh race condition prevention."""

    @pytest.mark.asyncio
    async def test_token_refresh_uses_lock(self):
        """Test that token refresh uses lock to prevent race conditions."""
        client = AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        )

        # Check that token lock exists
        assert hasattr(client, "_token_lock")
        await client.close()


class TestAsyncGeneratorInterface:
    """Test that list() methods return AsyncGenerator."""

    @pytest.mark.asyncio
    async def test_sp_campaigns_list_is_async_generator(self):
        """Test SP campaigns list returns AsyncGenerator."""
        from typing import AsyncGenerator
        import inspect

        async with AmazonAdsClient(
            refresh_token="test_token",
            profile_id="123",
            client_id="test_id",
            client_secret="test_secret",
        ) as client:
            # Check that list is an async generator function
            assert inspect.isasyncgenfunction(client.sp.campaigns.list)
