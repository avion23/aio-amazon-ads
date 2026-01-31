"""Comprehensive SP endpoint tests using respx."""

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
    """Mock authentication token endpoint."""
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
async def test_campaigns_get(client):
    """Test getting a specific campaign."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns/123").mock(
        return_value=Response(
            200,
            json={
                "campaignId": "123",
                "name": "Test Campaign",
                "state": "ENABLED",
                "dailyBudget": 10.0,
            },
        )
    )

    result = await client.sp.campaigns.get("123")

    assert result["campaignId"] == "123"
    assert result["name"] == "Test Campaign"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_campaigns_create(client):
    """Test creating campaigns."""
    mock_token()

    route = respx.post("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(
            200,
            json=[
                {
                    "campaignId": "123",
                    "name": "New Campaign",
                    "state": "ENABLED",
                    "dailyBudget": 10.0,
                }
            ],
        )
    )

    result = await client.sp.campaigns.create(
        [
            {
                "name": "New Campaign",
                "campaignType": "sponsoredProducts",
                "targetingType": "manual",
                "state": "ENABLED",
                "dailyBudget": 10.0,
                "startDate": "20260101",
            }
        ]
    )

    assert len(result) == 1
    assert result[0]["campaignId"] == "123"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_campaigns_edit(client):
    """Test editing campaigns."""
    mock_token()

    route = respx.put("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(
            200,
            json=[
                {
                    "campaignId": "123",
                    "name": "Updated Campaign",
                    "state": "PAUSED",
                    "dailyBudget": 15.0,
                }
            ],
        )
    )

    result = await client.sp.campaigns.edit(
        [{"campaignId": "123", "state": "PAUSED", "dailyBudget": 15.0}]
    )

    assert len(result) == 1
    assert result[0]["campaignId"] == "123"
    assert result[0]["state"] == "PAUSED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_campaigns_delete(client):
    """Test deleting a campaign."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sp/campaigns/123").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Campaign deleted"})
    )

    result = await client.sp.campaigns.delete("123")

    assert result["code"] == "SUCCESS"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_ad_groups_get(client):
    """Test getting a specific ad group."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/sp/adGroups/456").mock(
        return_value=Response(
            200,
            json={
                "adGroupId": "456",
                "campaignId": "123",
                "name": "Test Ad Group",
                "state": "ENABLED",
                "defaultBid": 0.5,
            },
        )
    )

    result = await client.sp.ad_groups.get("456")

    assert result["adGroupId"] == "456"
    assert result["name"] == "Test Ad Group"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_ad_groups_create(client):
    """Test creating ad groups."""
    mock_token()

    route = respx.post("https://advertising-api.amazon.com/sp/adGroups").mock(
        return_value=Response(
            200,
            json=[
                {
                    "adGroupId": "456",
                    "campaignId": "123",
                    "name": "New Ad Group",
                    "state": "ENABLED",
                    "defaultBid": 0.5,
                }
            ],
        )
    )

    result = await client.sp.ad_groups.create(
        [{"campaignId": "123", "name": "New Ad Group", "defaultBid": 0.5}]
    )

    assert len(result) == 1
    assert result[0]["adGroupId"] == "456"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_ad_groups_edit(client):
    """Test editing ad groups."""
    mock_token()

    route = respx.put("https://advertising-api.amazon.com/sp/adGroups").mock(
        return_value=Response(
            200,
            json=[
                {
                    "adGroupId": "456",
                    "name": "Updated Ad Group",
                    "state": "PAUSED",
                    "defaultBid": 0.75,
                }
            ],
        )
    )

    result = await client.sp.ad_groups.edit(
        [{"adGroupId": "456", "state": "PAUSED", "defaultBid": 0.75}]
    )

    assert len(result) == 1
    assert result[0]["adGroupId"] == "456"
    assert result[0]["state"] == "PAUSED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_ad_groups_delete(client):
    """Test deleting an ad group."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/sp/adGroups/456").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Ad group deleted"})
    )

    result = await client.sp.ad_groups.delete("456")

    assert result["code"] == "SUCCESS"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_keywords_get(client):
    """Test getting a specific keyword."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sp/keywords/789").mock(
        return_value=Response(
            200,
            json={
                "keywordId": "789",
                "campaignId": "123",
                "adGroupId": "456",
                "keywordText": "test keyword",
                "matchType": "exact",
                "state": "ENABLED",
                "bid": 0.5,
            },
        )
    )

    result = await client.sp.keywords.get("789")

    assert result["keywordId"] == "789"
    assert result["keywordText"] == "test keyword"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_keywords_edit(client):
    """Test editing keywords."""
    mock_token()

    route = respx.put("https://advertising-api.amazon.com/v2/sp/keywords").mock(
        return_value=Response(
            200,
            json=[
                {
                    "keywordId": "789",
                    "state": "PAUSED",
                    "bid": 0.75,
                }
            ],
        )
    )

    result = await client.sp.keywords.edit([{"keywordId": "789", "state": "PAUSED", "bid": 0.75}])

    assert len(result) == 1
    assert result[0]["keywordId"] == "789"
    assert result[0]["state"] == "PAUSED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_keywords_delete(client):
    """Test deleting a keyword."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sp/keywords/789").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Keyword deleted"})
    )

    result = await client.sp.keywords.delete("789")

    assert result["code"] == "SUCCESS"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_product_ads_get(client):
    """Test getting a specific product ad."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sp/productAds/101").mock(
        return_value=Response(
            200,
            json={
                "adId": "101",
                "campaignId": "123",
                "adGroupId": "456",
                "sku": "TEST-SKU",
                "state": "ENABLED",
            },
        )
    )

    result = await client.sp.product_ads.get("101")

    assert result["adId"] == "101"
    assert result["sku"] == "TEST-SKU"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_product_ads_edit(client):
    """Test editing product ads."""
    mock_token()

    route = respx.put("https://advertising-api.amazon.com/v2/sp/productAds").mock(
        return_value=Response(
            200,
            json=[
                {
                    "adId": "101",
                    "state": "PAUSED",
                }
            ],
        )
    )

    result = await client.sp.product_ads.edit([{"adId": "101", "state": "PAUSED"}])

    assert len(result) == 1
    assert result[0]["adId"] == "101"
    assert result[0]["state"] == "PAUSED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_product_ads_delete(client):
    """Test deleting a product ad."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sp/productAds/101").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Product ad deleted"})
    )

    result = await client.sp.product_ads.delete("101")

    assert result["code"] == "SUCCESS"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_negative_keywords_delete(client):
    """Test deleting a negative keyword."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sp/negativeKeywords/202").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Negative keyword deleted"})
    )

    result = await client.sp.negative_keywords.delete("202")

    assert result["code"] == "SUCCESS"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_targets_get(client):
    """Test getting a specific target."""
    mock_token()

    route = respx.get("https://advertising-api.amazon.com/v2/sp/targets/303").mock(
        return_value=Response(
            200,
            json={
                "targetId": "303",
                "campaignId": "123",
                "adGroupId": "456",
                "expression": [{"type": "asin", "value": "B08X6YZ"}],
                "state": "ENABLED",
                "bid": 0.5,
            },
        )
    )

    result = await client.sp.targets.get("303")

    assert result["targetId"] == "303"
    assert result["state"] == "ENABLED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_targets_edit(client):
    """Test editing targets."""
    mock_token()

    route = respx.put("https://advertising-api.amazon.com/v2/sp/targets").mock(
        return_value=Response(
            200,
            json=[
                {
                    "targetId": "303",
                    "state": "PAUSED",
                    "bid": 0.75,
                }
            ],
        )
    )

    result = await client.sp.targets.edit([{"targetId": "303", "state": "PAUSED", "bid": 0.75}])

    assert len(result) == 1
    assert result[0]["targetId"] == "303"
    assert result[0]["state"] == "PAUSED"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_targets_delete(client):
    """Test deleting a target."""
    mock_token()

    route = respx.delete("https://advertising-api.amazon.com/v2/sp/targets/303").mock(
        return_value=Response(200, json={"code": "SUCCESS", "details": "Target deleted"})
    )

    result = await client.sp.targets.delete("303")

    assert result["code"] == "SUCCESS"
    assert route.called
