# aio-amazon-ads

**Unofficial** native async Python client for Amazon Advertising API.

[![CI](https://github.com/avion23/aio-amazon-ads/actions/workflows/ci.yml/badge.svg)](https://github.com/avion23/aio-amazon-ads/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

⚠️ **Disclaimer:** This is an unofficial client. It is not affiliated with, endorsed by, or sponsored by Amazon.

## Features

- **Native async/await**: Built on `httpx` for high-performance concurrent requests
- **Auto-pagination**: Automatically fetches all pages for list endpoints
- **Professional retry**: Uses tenacity with exponential backoff and jitter
- **Namespaced API**: Clean interface with `client.sp.campaigns.list()`
- **Observability**: Comprehensive logging with X-Amzn-Request-Id tracking
- **Multi-marketplace**: Support for NA, EU, and FE endpoints
- **Type hints**: Full type annotations throughout

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
    marketplace=Marketplace.NA,  # or Marketplace.EU, Marketplace.FE
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

### Sponsored Brands V2 (16 endpoints)
- **Campaigns**: list, get, create, edit, delete
- **Ad Groups**: list, get, create, edit
- **Keywords**: list, get, create, edit
- **Ads**: list, get, create, edit

### Sponsored Display V2 (8 endpoints)
- **Campaigns**: list, get, create, edit, delete
- **Ad Groups**: list, get, create

### Portfolios (5 endpoints)
- list, get, create, edit, delete

### Profiles (2 endpoints)
- list, get

## Authentication

You need Amazon Advertising API credentials:
- `refresh_token`: From LWA (Login with Amazon) OAuth flow
- `profile_id`: Your Amazon Advertising profile ID (not Seller/Vendor ID)
- `client_id` & `client_secret`: From your Amazon Developer account

## Marketplace Support

The client supports three regional marketplaces:

- **NA** (North America): US, CA, MX, BR
- **EU** (Europe): UK, DE, FR, IT, ES, NL, AE, SE, PL, TR, EG, SA  
- **FE** (Far East): JP, AU, SG, IN

### Usage

```python
from aio_amazon_ads import AmazonAdsClient, Marketplace

# For EU marketplace
async with AmazonAdsClient(
    ...,
    marketplace=Marketplace.EU,
) as client:
    campaigns = await client.sp.campaigns.list()

# Or auto-detect from country code
from aio_amazon_ads import COUNTRY_TO_MARKETPLACE
marketplace = COUNTRY_TO_MARKETPLACE["DE"]  # Germany
```

**Important:** You must use the correct marketplace endpoint for your profile. Using the wrong endpoint will result in authentication errors.

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

## Retry Logic

The client uses `tenacity` for professional retry handling:

- **Automatic retry**: Network errors, timeouts, rate limiting (429)
- **Exponential backoff with jitter**: Prevents thundering herd
- **Max attempts**: 3 retries with configurable wait times
- **401 handling**: Automatic token refresh and retry

## Observability

The client provides comprehensive logging:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async with AmazonAdsClient(...) as client:
    # Logs will include:
    # - Request method, path, and parameters
    # - X-Amzn-Request-Id for debugging with Amazon support
    # - Response status and errors
    # - Token refresh events
    # - Retry attempts with tenacity
    campaigns = await client.sp.campaigns.list()
```

## Rate Limiting

Amazon Advertising API has strict rate limits:
- **Sponsored Products**: ~10 requests/second per profile
- **Sponsored Brands**: ~2 requests/second per profile
- **Sponsored Display**: ~5 requests/second per profile

The client automatically:
- Retries on 429 (Too Many Requests) with exponential backoff
- Respects `Retry-After` headers
- Prevents concurrent token refresh
- Logs rate limiting events

## Development Status

**Current Version:** 0.1.0 (Alpha)

**Known Limitations:**
- Pydantic models exist but are not yet enforced in service responses
- Input validation is basic (type checking only)
- No built-in caching for immutable data

**Roadmap:**
- [ ] Full Pydantic model integration for type safety
- [ ] Input validation with detailed error messages
- [ ] Caching for profiles and portfolios
- [ ] Metrics and monitoring hooks
- [ ] Additional endpoint coverage

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and architecture diagrams
- [Examples](examples/) - Usage examples

## CI/CD

This project uses GitHub Actions for continuous integration:

- **CI Pipeline**: Runs on every push and PR
  - Linting with `ruff`
  - Type checking with `mypy`
  - Tests on Python 3.10, 3.11, 3.12, 3.13, 3.14
  - Coverage reporting with Codecov

- **Release Pipeline**: Triggered on version tags
  - Automated PyPI publishing

View the [CI status](https://github.com/avion23/aio-amazon-ads/actions/workflows/ci.yml).

## License

MIT License - see [LICENSE](LICENSE) file.

## Disclaimer

This is an **unofficial** client library. Use at your own risk. Amazon may change their API at any time.
