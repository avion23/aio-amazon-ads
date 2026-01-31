# aio-amazon-ads

**Unofficial** native async Python client for Amazon Advertising API.

⚠️ **Disclaimer:** This is an unofficial client. It is not affiliated with, endorsed by, or sponsored by Amazon.

## Features

- **Native async/await**: Built on `httpx` for high-performance concurrent requests
- **Type-safe**: Full type hints with Pydantic models for request/response validation
- **Resilient**: Built-in retry logic with exponential backoff and token refresh
- **Namespaced API**: Clean interface with `client.sp.campaigns.list()`
- **Auto-pagination**: Automatically handles paginated responses

## Installation

```bash
pip install aio-amazon-ads
```

## Quick Start

```python
import asyncio
from aio_amazon_ads import AmazonAdsClient

async def main():
    async with AmazonAdsClient(
        refresh_token="your_refresh_token",
        profile_id="your_profile_id",
        client_id="your_client_id",
        client_secret="your_client_secret",
    ) as client:
        # List campaigns (auto-paginated)
        campaigns = []
        async for campaign in client.sp.campaigns.list():
            campaigns.append(campaign)
        
        print(f"Found {len(campaigns)} campaigns")
        
        # Create keywords
        new_keywords = await client.sp.keywords.create([
            {
                "campaignId": 123,
                "adGroupId": 456,
                "keywordText": "running shoes",
                "matchType": "exact",
                "state": "enabled",
                "bid": 1.50,
            }
        ])

asyncio.run(main())
```

## API Coverage

### Sponsored Products V2 (31 endpoints)
- **Campaigns**: list, get, create, edit, delete
- **Ad Groups**: list, get, create, edit, delete
- **Keywords**: list, get, create, edit, delete
- **Product Ads**: list, get, create, edit, delete
- **Negative Keywords**: list, create, delete
- **Targets**: list, get, create, edit, delete
- **Reports**: create, get_status, download

## Authentication

You need Amazon Advertising API credentials:
- `refresh_token`: From LWA (Login with Amazon) OAuth flow
- `profile_id`: Your Amazon Advertising profile ID (not Seller/Vendor ID)
- `client_id` & `client_secret`: From your Amazon Developer account

## Error Handling

```python
from aio_amazon_ads import (
    AmazonAdsClient,
    AuthenticationError,
    ThrottlingError,
    AmazonAPIError,
)

async def safe_api_call():
    try:
        campaigns = await client.sp.campaigns.list()
    except AuthenticationError:
        # Token expired - will auto-refresh on next call
        pass
    except ThrottlingError as e:
        # Rate limited, retry after e.retry_after seconds
        await asyncio.sleep(e.retry_after)
    except AmazonAPIError as e:
        # Other API errors
        print(f"API error: {e}")
```

## Rate Limiting

Amazon Advertising API has strict rate limits:
- **Sponsored Products**: ~10 requests/second per profile
- **Sponsored Brands**: ~2 requests/second per profile
- **Sponsored Display**: ~5 requests/second per profile

This client automatically:
- Retries on 429 (Too Many Requests) with exponential backoff
- Respects `Retry-After` headers
- Prevents concurrent token refresh

## License

MIT License - see [LICENSE](LICENSE) file.

## Disclaimer

This is an **unofficial** client library. Use at your own risk. Amazon may change their API at any time.
