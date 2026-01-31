# amzn-ads

Native async Python client for Amazon Advertising API.

## Features

- **Native async/await**: Built on `httpx` for high-performance concurrent requests
- **Complete coverage**: 70+ endpoints across Sponsored Products, Brands, and Display
- **Type-safe**: Full type hints with `msgspec` for fast serialization
- **Resilient**: Built-in retry logic with exponential backoff
- **Simple**: Flat API design, minimal abstractions

## Installation

```bash
pip install amzn-ads
```

## Quick Start

```python
import asyncio
from amzn_ads import AmazonAdsClient

async def main():
    async with AmazonAdsClient(
        refresh_token="your_refresh_token",
        profile_id="your_profile_id",
        client_id="your_client_id",
        client_secret="your_client_secret",
    ) as client:
        # List campaigns
        campaigns = await client.list_campaigns_v2()
        
        # Create a campaign
        new_campaign = await client.create_campaign_v2({
            "name": "My Campaign",
            "campaignType": "sponsoredProducts",
            "targetingType": "manual",
            "state": "enabled",
            "dailyBudget": 50.0,
            "startDate": "2026-02-01",
        })
        
        print(f"Created campaign: {new_campaign['campaignId']}")

asyncio.run(main())
```

## API Coverage

### Sponsored Products (40 endpoints)
- Campaigns: list, get, create, edit, delete
- Ad Groups: list, get, create, edit, delete
- Keywords: list, get, create, edit, delete
- Product Ads: list, get, create, edit, delete
- Negative Keywords: list, create, delete
- Product Targets: list, get, create, edit, delete
- Negative Targets: list, create, delete
- Reports: create, get status, download
- Snapshots: create, get status, download

### Sponsored Brands (15 endpoints)
- Campaigns: list, get, create, edit, delete
- Ad Groups: list, get, create, edit
- Keywords: list, get, create, edit
- Ads: list, get, create, edit

### Sponsored Display (10 endpoints)
- Campaigns: list, get, create, edit, delete
- Ad Groups: list, get, create
- Product Ads: list, create

### Portfolios (5 endpoints)
- list, get, create, edit, delete

## Error Handling

```python
from amzn_ads import (
    AmazonAdsClient,
    AuthenticationError,
    ThrottlingError,
    AmazonAPIError,
)

async def safe_api_call():
    try:
        campaigns = await client.list_campaigns_v2()
    except AuthenticationError:
        # Refresh token expired
        pass
    except ThrottlingError as e:
        # Rate limited, retry after e.retry_after seconds
        pass
    except AmazonAPIError as e:
        # Other API errors
        pass
```

## License

MIT License - see [LICENSE](LICENSE) file.
