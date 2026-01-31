"""Comprehensive tests for SB and SD endpoints using respx."""

import sys

import pytest

sys.path.insert(0, "src")

import respx
from httpx import Response

from aio_amazon_ads import AmazonAdsClient


@pytest.fixture
def client():
    """Create test client."""
    return AmazonAdsClient(
        refresh_token="test_refresh_token",
        profile_id="123456789",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )


def mock_token():
    """Mock token endpoint."""
    return respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )


@respx.mock
@pytest.mark.asyncio
async def test_sb_campaigns_get(client):
    """Test Sponsored Brands campaign get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/campaigns/sb123").mock(
        return_value=Response(
            200,
            json={
                "campaignId": "sb123",
                "name": "SB Campaign 1",
                "state": "enabled",
                "budget": 100.0,
            },
        )
    )

    result = await client.sb.campaigns.get("sb123")

    assert result["campaignId"] == "sb123"
    assert result["name"] == "SB Campaign 1"
    assert result["state"] == "enabled"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_campaigns_delete(client):
    """Test Sponsored Brands campaign delete."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sb/campaigns/sb123").mock(
        return_value=Response(
            200,
            json={
                "campaignId": "sb123",
                "status": "deleted",
            },
        )
    )

    result = await client.sb.campaigns.delete("sb123")

    assert result["campaignId"] == "sb123"
    assert result["status"] == "deleted"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_ad_groups_get(client):
    """Test Sponsored Brands ad group get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/adGroups/sbag123").mock(
        return_value=Response(
            200,
            json={
                "adGroupId": "sbag123",
                "name": "SB Ad Group 1",
                "state": "enabled",
                "campaignId": "sb123",
            },
        )
    )

    result = await client.sb.ad_groups.get("sbag123")

    assert result["adGroupId"] == "sbag123"
    assert result["name"] == "SB Ad Group 1"
    assert result["state"] == "enabled"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_keywords_get(client):
    """Test Sponsored Brands keyword get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/keywords/sbkw123").mock(
        return_value=Response(
            200,
            json={
                "keywordId": "sbkw123",
                "keywordText": "running shoes",
                "matchType": "broad",
                "state": "enabled",
                "campaignId": "sb123",
            },
        )
    )

    result = await client.sb.keywords.get("sbkw123")

    assert result["keywordId"] == "sbkw123"
    assert result["keywordText"] == "running shoes"
    assert result["matchType"] == "broad"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_ads_get(client):
    """Test Sponsored Brands ad get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/ads/sbad123").mock(
        return_value=Response(
            200,
            json={
                "adId": "sbad123",
                "adGroupId": "sbag123",
                "campaignId": "sb123",
                "state": "enabled",
            },
        )
    )

    result = await client.sb.ads.get("sbad123")

    assert result["adId"] == "sbad123"
    assert result["adGroupId"] == "sbag123"
    assert result["state"] == "enabled"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_campaigns_list(client):
    """Test Sponsored Brands campaigns list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/campaigns").mock(
        return_value=Response(
            200,
            json={
                "campaigns": [
                    {"campaignId": "sb1", "name": "SB Campaign 1", "state": "enabled"},
                    {"campaignId": "sb2", "name": "SB Campaign 2", "state": "paused"},
                ],
            },
        )
    )

    campaigns = []
    async for campaign in client.sb.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 2
    assert campaigns[0]["campaignId"] == "sb1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_ad_groups_list(client):
    """Test Sponsored Brands ad groups list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/adGroups").mock(
        return_value=Response(
            200,
            json={
                "adGroups": [
                    {"adGroupId": "sbag1", "name": "SB Ad Group 1", "state": "enabled"},
                    {"adGroupId": "sbag2", "name": "SB Ad Group 2", "state": "paused"},
                ],
            },
        )
    )

    ad_groups = []
    async for ad_group in client.sb.ad_groups.list():
        ad_groups.append(ad_group)

    assert len(ad_groups) == 2
    assert ad_groups[0]["adGroupId"] == "sbag1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_keywords_list(client):
    """Test Sponsored Brands keywords list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/keywords").mock(
        return_value=Response(
            200,
            json={
                "keywords": [
                    {
                        "keywordId": "sbkw1",
                        "keywordText": "running shoes",
                        "matchType": "broad",
                    },
                    {
                        "keywordId": "sbkw2",
                        "keywordText": "walking shoes",
                        "matchType": "exact",
                    },
                ],
            },
        )
    )

    keywords = []
    async for keyword in client.sb.keywords.list():
        keywords.append(keyword)

    assert len(keywords) == 2
    assert keywords[0]["keywordId"] == "sbkw1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sb_ads_list(client):
    """Test Sponsored Brands ads list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sb/ads").mock(
        return_value=Response(
            200,
            json={
                "ads": [
                    {"adId": "sbad1", "adGroupId": "sbag1", "state": "enabled"},
                    {"adId": "sbad2", "adGroupId": "sbag2", "state": "paused"},
                ],
            },
        )
    )

    ads = []
    async for ad in client.sb.ads.list():
        ads.append(ad)

    assert len(ads) == 2
    assert ads[0]["adId"] == "sbad1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sd_campaigns_get(client):
    """Test Sponsored Display campaign get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sd/campaigns/sd123").mock(
        return_value=Response(
            200,
            json={
                "campaignId": "sd123",
                "name": "SD Campaign 1",
                "state": "enabled",
                "budget": 100.0,
            },
        )
    )

    result = await client.sd.campaigns.get("sd123")

    assert result["campaignId"] == "sd123"
    assert result["name"] == "SD Campaign 1"
    assert result["state"] == "enabled"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sd_campaigns_delete(client):
    """Test Sponsored Display campaign delete."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sd/campaigns/sd123").mock(
        return_value=Response(
            200,
            json={
                "campaignId": "sd123",
                "status": "deleted",
            },
        )
    )

    result = await client.sd.campaigns.delete("sd123")

    assert result["campaignId"] == "sd123"
    assert result["status"] == "deleted"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sd_ad_groups_get(client):
    """Test Sponsored Display ad group get by ID."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sd/adGroups/sdag123").mock(
        return_value=Response(
            200,
            json={
                "adGroupId": "sdag123",
                "name": "SD Ad Group 1",
                "state": "enabled",
                "campaignId": "sd123",
            },
        )
    )

    result = await client.sd.ad_groups.get("sdag123")

    assert result["adGroupId"] == "sdag123"
    assert result["name"] == "SD Ad Group 1"
    assert result["state"] == "enabled"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sd_campaigns_list(client):
    """Test Sponsored Display campaigns list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sd/campaigns").mock(
        return_value=Response(
            200,
            json={
                "campaigns": [
                    {"campaignId": "sd1", "name": "SD Campaign 1", "state": "enabled"},
                    {"campaignId": "sd2", "name": "SD Campaign 2", "state": "paused"},
                ],
            },
        )
    )

    campaigns = []
    async for campaign in client.sd.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 2
    assert campaigns[0]["campaignId"] == "sd1"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_sd_ad_groups_list(client):
    """Test Sponsored Display ad groups list."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sd/adGroups").mock(
        return_value=Response(
            200,
            json={
                "adGroups": [
                    {"adGroupId": "sdag1", "name": "SD Ad Group 1", "state": "enabled"},
                    {"adGroupId": "sdag2", "name": "SD Ad Group 2", "state": "paused"},
                ],
            },
        )
    )

    ad_groups = []
    async for ad_group in client.sd.ad_groups.list():
        ad_groups.append(ad_group)

    assert len(ad_groups) == 2
    assert ad_groups[0]["adGroupId"] == "sdag1"
    assert route.called
