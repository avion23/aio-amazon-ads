"""Comprehensive pagination tests using respx."""

import sys

import pytest
from httpx import Response

sys.path.insert(0, "src")

import respx

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


@respx.mock
@pytest.mark.asyncio
async def test_multi_page_pagination_campaigns(client):
    """Test multi-page pagination with nextToken."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    call_count = 0

    async def pagination_handler(request):
        nonlocal call_count
        call_count += 1
        params = dict(request.url.params)

        if call_count == 1:
            # First page - no nextToken
            assert "nextToken" not in params
            return Response(
                200,
                json={
                    "campaigns": [
                        {"campaignId": "1", "name": "Campaign 1", "state": "enabled"},
                        {"campaignId": "2", "name": "Campaign 2", "state": "enabled"},
                        {"campaignId": "3", "name": "Campaign 3", "state": "enabled"},
                    ],
                    "nextToken": "abc123xyz",
                },
            )
        else:
            # Second page - should have nextToken
            assert params.get("nextToken") == "abc123xyz"
            return Response(
                200,
                json={
                    "campaigns": [
                        {"campaignId": "4", "name": "Campaign 4", "state": "paused"},
                        {"campaignId": "5", "name": "Campaign 5", "state": "paused"},
                    ],
                },
            )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(  # noqa: F841
        side_effect=pagination_handler
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 5
    assert campaigns[0]["campaignId"] == "1"
    assert campaigns[1]["campaignId"] == "2"
    assert campaigns[2]["campaignId"] == "3"
    assert campaigns[3]["campaignId"] == "4"
    assert campaigns[4]["campaignId"] == "5"
    assert call_count == 2


@respx.mock
@pytest.mark.asyncio
async def test_multi_page_pagination_sb_campaigns(client):
    """Test multi-page pagination for Sponsored Brands campaigns."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    page1_response = {
        "campaigns": [
            {"campaignId": "sb1", "name": "SB Campaign 1", "state": "ENABLED"},
            {"campaignId": "sb2", "name": "SB Campaign 2", "state": "ENABLED"},
        ],
        "nextToken": "token_page_2",
    }

    page2_response = {
        "campaigns": [
            {"campaignId": "sb3", "name": "SB Campaign 3", "state": "PAUSED"},
        ],
    }

    route = respx.get("https://advertising-api.amazon.com/v2/sb/campaigns").mock(
        return_value=Response(200, json=page1_response),
    )

    campaigns = []
    async for campaign in client.sb.campaigns.list():
        if len(campaigns) == 0:
            route.side_effect = lambda request: Response(200, json=page2_response)
        campaigns.append(campaign)

    assert len(campaigns) == 3
    assert campaigns[0]["campaignId"] == "sb1"
    assert campaigns[1]["campaignId"] == "sb2"
    assert campaigns[2]["campaignId"] == "sb3"


@respx.mock
@pytest.mark.asyncio
async def test_multi_page_pagination_sd_ad_groups(client):
    """Test multi-page pagination for Sponsored Display ad groups."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    call_count = 0

    async def paginated_handler(request):
        nonlocal call_count
        call_count += 1
        params = dict(request.url.params)

        if call_count == 1:
            return Response(
                200,
                json={
                    "adGroups": [
                        {"adGroupId": "1", "name": "Ad Group 1"},
                        {"adGroupId": "2", "name": "Ad Group 2"},
                        {"adGroupId": "3", "name": "Ad Group 3"},
                    ],
                    "nextToken": "page2_token",
                },
            )
        else:
            assert params.get("nextToken") == "page2_token"
            return Response(
                200,
                json={
                    "adGroups": [
                        {"adGroupId": "4", "name": "Ad Group 4"},
                    ],
                },
            )

    route = respx.get("https://advertising-api.amazon.com/v2/sd/adGroups").mock(
        side_effect=paginated_handler
    )

    ad_groups = []
    async for ad_group in client.sd.ad_groups.list():
        ad_groups.append(ad_group)

    assert len(ad_groups) == 4
    assert ad_groups[0]["adGroupId"] == "1"
    assert ad_groups[1]["adGroupId"] == "2"
    assert ad_groups[2]["adGroupId"] == "3"
    assert ad_groups[3]["adGroupId"] == "4"
    assert call_count == 2


@respx.mock
@pytest.mark.asyncio
async def test_pagination_with_filters(client):
    """Test pagination works correctly with query filters."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    page1_response = {
        "campaigns": [
            {"campaignId": "1", "name": "Enabled 1", "state": "ENABLED"},
            {"campaignId": "2", "name": "Enabled 2", "state": "ENABLED"},
        ],
        "nextToken": "next_page",
    }

    page2_response = {
        "campaigns": [
            {"campaignId": "3", "name": "Enabled 3", "state": "ENABLED"},
        ],
    }

    request_params = []

    async def filtered_handler(request):
        params = dict(request.url.params)
        request_params.append(params)
        if len(request_params) == 1:
            # SB campaigns uses **filters so parameter names are passed as-is
            assert params.get("state_filter") == "ENABLED"
            return Response(200, json=page1_response)
        else:
            assert params.get("nextToken") == "next_page"
            assert params.get("state_filter") == "ENABLED"
            return Response(200, json=page2_response)

    route = respx.get("https://advertising-api.amazon.com/v2/sb/campaigns").mock(
        side_effect=filtered_handler
    )

    campaigns = []
    # Use state_filter (with underscore) since SB uses **filters
    async for campaign in client.sb.campaigns.list(state_filter="ENABLED"):
        campaigns.append(campaign)

    assert len(campaigns) == 3
    assert campaigns[0]["state"] == "ENABLED"
    assert campaigns[1]["state"] == "ENABLED"
    assert campaigns[2]["state"] == "ENABLED"
    assert len(request_params) == 2
    assert request_params[0]["state_filter"] == "ENABLED"
    assert request_params[1]["state_filter"] == "ENABLED"


@respx.mock
@pytest.mark.asyncio
async def test_single_page_no_pagination(client):
    """Test that single page responses work correctly without nextToken."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(
            200,
            json={
                "campaigns": [
                    {"campaignId": "1", "name": "Campaign 1", "state": "enabled"},
                ],
            },
        )
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 1
    assert campaigns[0]["campaignId"] == "1"
    assert route.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_empty_response_pagination(client):
    """Test pagination with empty campaign list."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        return_value=Response(200, json={"campaigns": []})
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 0
    assert route.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_three_page_pagination(client):
    """Test pagination across three pages."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    call_count = 0

    async def multi_page_handler(request):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return Response(
                200,
                json={
                    "campaigns": [
                        {"campaignId": f"{i}", "name": f"Campaign {i}"} for i in range(1, 4)
                    ],
                    "nextToken": "page2_token",
                },
            )
        elif call_count == 2:
            assert request.url.params.get("nextToken") == "page2_token"
            return Response(
                200,
                json={
                    "campaigns": [
                        {"campaignId": f"{i}", "name": f"Campaign {i}"} for i in range(4, 7)
                    ],
                    "nextToken": "page3_token",
                },
            )
        else:
            assert request.url.params.get("nextToken") == "page3_token"
            return Response(
                200,
                json={
                    "campaigns": [
                        {"campaignId": "7", "name": "Campaign 7"},
                        {"campaignId": "8", "name": "Campaign 8"},
                    ],
                },
            )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        side_effect=multi_page_handler
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    assert len(campaigns) == 8
    assert call_count == 3
    for i in range(1, 9):
        assert campaigns[i - 1]["campaignId"] == str(i)


@respx.mock
@pytest.mark.asyncio
async def test_async_generator_yields_all_items(client):
    """Test that AsyncGenerator properly yields all items across pages."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    page1_response = {
        "campaigns": [
            {"campaignId": str(i), "name": f"Campaign {i}", "state": "enabled"} for i in range(1, 6)
        ],
        "nextToken": "continue_token",
    }

    page2_response = {
        "campaigns": [
            {"campaignId": str(i), "name": f"Campaign {i}", "state": "enabled"}
            for i in range(6, 11)
        ],
    }

    request_count = 0

    async def track_requests(request):
        nonlocal request_count
        request_count += 1
        if request_count == 1:
            return Response(200, json=page1_response)
        return Response(200, json=page2_response)

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        side_effect=track_requests
    )

    collected_items = []
    async for campaign in client.sp.campaigns.list():
        collected_items.append(campaign)

    assert len(collected_items) == 10
    assert request_count == 2

    for i, campaign in enumerate(collected_items, start=1):
        assert campaign["campaignId"] == str(i)
        assert campaign["name"] == f"Campaign {i}"
        assert campaign["state"] == "enabled"


@respx.mock
@pytest.mark.asyncio
async def test_pagination_with_campaign_id_filter(client):
    """Test pagination with campaignIdFilter parameter."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    captured_params = []

    async def capture_params(request):
        params = dict(request.url.params)
        captured_params.append(params)
        return Response(
            200,
            json={
                "campaigns": [
                    {"campaignId": "12345", "name": "Specific Campaign", "state": "enabled"},
                ],
            },
        )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        side_effect=capture_params
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list(campaign_id_filter="12345"):
        campaigns.append(campaign)

    assert len(campaigns) == 1
    assert campaigns[0]["campaignId"] == "12345"
    assert len(captured_params) == 1
    assert captured_params[0].get("campaignIdFilter") == "12345"


@respx.mock
@pytest.mark.asyncio
async def test_mixed_response_format_pagination(client):
    """Test pagination handles both list and dict response formats."""
    respx.post("https://api.amazon.com/auth/o2/token").mock(
        return_value=Response(
            200,
            json={
                "access_token": "mock_token",
                "expires_in": 3600,
            },
        )
    )

    # First page returns a list (no pagination support)
    # Second page returns dict with nextToken
    call_count = 0

    async def mixed_handler(request):
        nonlocal call_count
        call_count += 1
        params = dict(request.url.params)

        if call_count == 1:
            # First call - return list format (no nextToken, single page)
            return Response(
                200,
                json=[
                    {"campaignId": "1", "name": "Campaign 1", "state": "enabled"},
                    {"campaignId": "2", "name": "Campaign 2", "state": "enabled"},
                ],
            )
        else:
            # Should not be called for list format
            return Response(
                200,
                json={"campaigns": []},
            )

    route = respx.get("https://advertising-api.amazon.com/v2/sp/campaigns").mock(
        side_effect=mixed_handler
    )

    campaigns = []
    async for campaign in client.sp.campaigns.list():
        campaigns.append(campaign)

    # List format returns only first page (2 items), no pagination
    assert len(campaigns) == 2
    assert campaigns[0]["campaignId"] == "1"
    assert campaigns[1]["campaignId"] == "2"
    assert call_count == 1
