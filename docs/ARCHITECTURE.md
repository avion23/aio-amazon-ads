# aio-amazon-ads Architecture

## Overview

This document describes the architecture of `aio-amazon-ads`, a native async Python client for the Amazon Advertising API.

## Design Principles

1. **Uniform Interface**: All services expose the same CRUD pattern
2. **Type Safety**: Pydantic models for validation and IDE support
3. **Pure Functions**: Validation logic isolated with no side effects
4. **Professional Retry**: Tenacity library for exponential backoff
5. **Testability**: Dependency injection and Protocol-based interfaces

## System Architecture

```
AmazonAdsClient (Entry Point)
    │
    ├─── Sponsored Products (sp)
    │       ├── Campaigns (31 endpoints)
    │       ├── AdGroups
    │       ├── Keywords
    │       ├── ProductAds
    │       ├── NegativeKeywords
    │       ├── Targets
    │       └── Reports
    │
    ├─── Sponsored Brands (sb)
    │       ├── Campaigns (16 endpoints)
    │       ├── AdGroups
    │       ├── Keywords
    │       └── Ads
    │
    ├─── Sponsored Display (sd)
    │       ├── Campaigns (8 endpoints)
    │       └── AdGroups
    │
    ├─── Portfolios (5 endpoints)
    │
    └─── Profiles (2 endpoints)
```

## Service Pattern

All services follow a uniform CRUD interface:

```python
class CampaignsService:
    async def list(self, **filters) -> AsyncGenerator[Dict, None]
    async def get(self, campaign_id: str) -> Dict
    async def create(self, campaigns: List[Dict]) -> List[Dict]
    async def edit(self, campaigns: List[Dict]) -> List[Dict]
    async def delete(self, campaign_id: str) -> Dict
```

## Pagination Strategy

All `list()` methods return `AsyncGenerator` for automatic pagination:

```python
# Client code
async for campaign in client.sp.campaigns.list(stateFilter="ENABLED"):
    process(campaign)

# Internal implementation
params = filters.copy()
while True:
    response = await self._request("GET", endpoint, params=params)
    data = response.json()
    
    for item in data.get("items", []):
        yield item
    
    if not data.get("nextToken"):
        break
    params["nextToken"] = data["nextToken"]
```

## Retry Strategy

Uses tenacity for professional retry logic:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception_type((ThrottlingError, NetworkError))
)
async def request(self, method: str, path: str, ...) -> httpx.Response:
    ...
```

## Authentication Flow

```
1. Client makes API call
2. Check if access token is valid (not expired)
3. If expired, acquire lock and refresh token
4. Use refreshed token for API call
5. Handle 401/403 errors with automatic retry
```

## Validation Architecture

Validation is separated into pure functions:

```python
# validation.py - Pure functions, no side effects
def validate_campaign_state(state: Optional[str]) -> None:
    if state and state not in VALID_STATES:
        raise ValueError(f"Invalid state: {state}")

def validate_campaign_id(campaign_id: Optional[str]) -> str:
    if not campaign_id:
        raise ValueError("campaign_id is required")
    return campaign_id
```

## Testing Strategy

```
Test Pyramid:
    
    Integration Tests (respx)
    ├── HTTP layer mocking
    ├── Auth flow testing
    └── Retry logic verification
    
    Unit Tests
    ├── Service logic
    ├── Validation functions
    └── Error handling
    
    Pure Function Tests
    ├── Edge cases
    └── Input validation
```

## Comparison with Open Source

| Feature | python-amazon-ad-api | aio-amazon-ads |
|---------|---------------------|----------------|
| Async Support | ❌ Sync only | ✅ Native async |
| Pagination | ❌ Manual | ✅ Auto (AsyncGenerator) |
| Retry Logic | ⚠️ Basic | ✅ Tenacity (exponential) |
| Type Safety | ⚠️ Dicts | ✅ Pydantic models |
| Interface | ❌ Inconsistent | ✅ Uniform CRUD |
| Testability | ⚠️ Hard to mock | ✅ Protocol-based DI |

## File Structure

```
aio-amazon-ads/
├── src/aio_amazon_ads/
│   ├── __init__.py          # Public exports
│   ├── client.py            # Main client class
│   ├── base.py              # Base client with HTTP/retry
│   ├── exceptions.py        # Custom exceptions
│   ├── validation.py        # Pure validation functions
│   ├── models/              # Pydantic models
│   │   └── sp.py
│   └── services/            # API services
│       ├── sp/
│       ├── sb/
│       ├── sd/
│       ├── portfolios/
│       └── profiles/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── ARCHITECTURE.md
│   └── API_REFERENCE.md
└── examples/
```

## Future Improvements

1. **Caching**: LRU cache for immutable data (profiles)
2. **Batching**: Automatic request batching for bulk operations
3. **Metrics**: Prometheus metrics for API call monitoring
4. **Circuit Breaker**: Fail-fast when API is unavailable
5. **Regional Endpoints**: Support for EU/FE endpoints
