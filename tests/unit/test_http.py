"""Comprehensive HTTP tests using respx."""

import pytest
import sys

sys.path.insert(0, "src")

import respx
from httpx import Response

from aio_amazon_ads import AmazonAdsClient
from aio_amazon_ads.exceptions import AuthenticationError, ThrottlingError


@pytest.fixture
def client():
    """Create test client."""
    return AmazonAdsClient(
        refresh_token="test_refresh_token",
        profile_id="123456789",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )


@respx.mock
@pytest.mark.asyncio
async def test_list_campaigns_success(client):
    """Test successful campaign listing."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock campaigns endpoint
    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(
            200,
            json=[
                {"campaignId": "1", "name": "Campaign 1", "state": "enabled"},
                {"campaignId": "2", "name": "Campaign 2", "state": "paused"},
            ],
        )
    )

    # Now using AsyncGenerator - collect all items
    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 2
    assert campaigns[0]["campaignId"] == "1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_create_keywords(client):
    """Test keyword creation."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock keywords endpoint
    route = respx.post("https://advertising-api.amazon.com/v2/sp/keywords").mock(
        return_value=Response(
            200,
            json=[
                {"keywordId": "123", "keywordText": "test keyword", "state": "enabled"},
            ],
        )
    )

    result = await client.sp.keywords.create(
        [
            {
                "campaignId": "1",
                "adGroupId": "2",
                "keywordText": "test keyword",
                "matchType": "exact",
            }
        ]
    )

    assert len(result) == 1
    assert result[0]["keywordId"] == "123"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_authentication_error(client):
    """Test 401 authentication error handling."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock campaigns endpoint with 401
    respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(401, json={"error": "Unauthorized"})
    )

    with pytest.raises(AuthenticationError):
        async for _ in client.sp.campaigns.list():
            pass


@respx.mock
@pytest.mark.asyncio
async def test_throttling_error(client):
    """Test 429 throttling error handling."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock campaigns endpoint with 429
    respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(
            429,
            json={"error": "Rate limit exceeded"},
            headers={"Retry-After": "60"},
        )
    )

    with pytest.raises(ThrottlingError) as exc_info:
        async for _ in client.sp.campaigns.list():
            pass

    assert exc_info.value.retry_after == 60


@respx.mock
@pytest.mark.asyncio
async def test_sb_campaigns_list(client):
    """Test Sponsored Brands campaigns listing."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock SB campaigns endpoint - returns wrapped response
    route = respx.get("https://advertising-api.amazon.com/v2/sb/campaigns").mock(
        return_value=Response(
            200,
            json={
                "campaigns": [{"campaignId": "sb1", "name": "SB Campaign 1"}],
            },
        )
    )

    campaigns = []
    async for campaign in client.sb.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 1
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_portfolios_list(client):
    """Test portfolios listing."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock portfolios endpoint - returns wrapped response
    route = respx.get("https://advertising-api.amazon.com/v2/portfolios").mock(
        return_value=Response(
            200,
            json={
                "portfolios": [{"portfolioId": "p1", "name": "Portfolio 1"}],
            },
        )
    )

    portfolios = []
    async for portfolio in client.portfolios.list():
        portfolios.append(portfolio)

    assert len(portfolios) == 1
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_profiles_list(client):
    """Test profiles listing."""
    # Mock token endpoint
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # Mock profiles endpoint
    route = respx.get("https://advertising-api.amazon.com/v2/profiles").mock(
        return_value=Response(
            200,
            json=[
                {"profileId": 123, "countryCode": "US"},
            ],
        )
    )

    profiles = await client.profiles.list()

    assert len(profiles) == 1
    assert profiles[0]["profileId"] == 123
    assert route.called
