# aio-amazon-ads Architecture Documentation

## Overview

Native async Python client for Amazon Advertising API with 70+ endpoints, uniform interfaces, and professional retry logic.

## Architecture Principles

1. **Uniform Interface**: All `list()` methods return `AsyncGenerator` for consistent pagination
2. **Pure Functions**: Validation extracted to separate module with no side effects
3. **Professional Retry**: Tenacity library for battle-tested exponential backoff
4. **Testability**: Dependency injection pattern for easy mocking
5. **Type Safety**: Pydantic models for request/response validation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AmazonAdsClient                          │
│  (Main entry point with async context manager)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐ ┌─────▼──────┐
│      SP      │ │    SB    │ │     SD      │ │ Portfolios │
│  (31 endpoints)│ (16 endpoints)│ (8 endpoints)│  (5 endpoints)│
└───────┬──────┘ └────┬─────┘ └──────┬──────┘ └─────┬──────┘
        │             │              │              │
   ┌────▼────┐   ┌───▼────┐    ┌────▼────┐    ┌────▼────┐
   │Campaigns│   │Campaigns│    │Campaigns│    │Portfolios│
   │AdGroups │   │AdGroups │    │AdGroups │    └─────────┘
   │Keywords │   │Keywords │    └─────────┘
   │ProductAds│  │Ads     │
   │Targets  │   └────────┘
   └─────────┘
```

## Service Interface Pattern

All services follow the same interface:

```python
class Campaigns(BaseService):
    async def list(self, **filters) -> AsyncGenerator[Dict, None]:
        """Auto-paginated listing with client-side filtering."""
        
    async def get(self, id: str) -> Dict:
        """Get single entity."""
        
    async def create(self, items: List[Dict]) -> List[Dict]:
        """Batch create."""
        
    async def edit(self, items: List[Dict]) -> List[Dict]:
        """Batch update."""
        
    async def delete(self, id: str) -> Dict:
        """Delete single entity."""
```

## Retry Strategy

```
Request
    │
    ▼
┌─────────────┐
│  Tenacity   │◄── stop_after_attempt(3)
│   Retry     │◄── wait_exponential(multiplier=1, min=2, max=60)
│   Wrapper   │◄── retry_if_exception_type((ThrottlingError, NetworkError))
└──────┬──────┘
       │
       ▼
┌──────────────┐     429     ┌─────────────┐
│  HTTP Call   │────────────►│  Sleep      │
│              │             │  Retry-After│
└──────┬───────┘             └──────┬──────┘
       │                            │
       │ 200/201                    │
       ▼                            ▼
┌──────────────┐             ┌──────────────┐
│  Parse JSON  │             │  Exponential │
│  Yield items │             │  Backoff     │
└──────────────┘             └──────────────┘
```

## Pagination Flow

```python
# Client usage
async for campaign in client.sp.campaigns.list(stateFilter="ENABLED"):
    if campaign["dailyBudget"] > 100:  # Client-side filtering
        print(campaign["name"])

# Internal flow
params = {"stateFilter": "ENABLED"}
while True:
    response = await http.get("/v2/sp/campaigns", params=params)
    data = response.json()
    
    for item in data["campaigns"]:
        yield item  # Stream to client
    
    if not data.get("nextToken"):
        break
    params["nextToken"] = data["nextToken"]
```

## Authentication Flow

```
┌──────────────┐
│  Client Call │
└──────┬───────┘
       │
       ▼
┌──────────────┐     Token expired?     ┌──────────────┐
│ Check Token  │───────────────────────►│ Refresh Token│
│   Valid?     │                        │   (locked)   │
└──────┬───────┘                        └──────┬───────┘
       │ No                                    │
       │ Yes                                   ▼
       │                              ┌──────────────┐
       │                              │ POST /auth   │
       │                              │ /o2/token    │
       │                              └──────┬───────┘
       │                                     │
       │                              ┌──────▼───────┐
       │                              │ Store token  │
       │                              │ with expiry  │
       │                              └──────┬───────┘
       │                                     │
       └─────────────────────────────────────┘
                       │
                       ▼
              ┌──────────────┐
              │  Make API    │
              │    Call      │
              └──────────────┘
```

## Testing Strategy

```
┌─────────────────────────────────────────┐
│           Test Pyramid                  │
├─────────────────────────────────────────┤
│                                         │
│     ┌─────────┐  Integration tests      │
│     │  HTTP   │  (respx mocking)        │
│     │  Layer  │  - Auth flow            │
│     └────┬────┘  - Retry logic          │
│          │       - Error handling       │
│     ┌────▼────┐                         │
│     │ Service │  Unit tests             │
│     │  Layer  │  - Validation logic     │
│     └────┬────┘  - Response parsing     │
│          │                             │
│     ┌────▼────┐                         │
│     │  Pure   │  Validation tests       │
│     │Functions│  - Edge cases           │
│     └─────────┘  - Error conditions     │
│                                         │
└─────────────────────────────────────────┘
```

## Comparison with Open-Source Library

| Feature | python-amazon-ad-api | aio-amazon-ads (Ours) |
|---------|---------------------|----------------------|
| **Async** | ❌ Sync only | ✅ Native async |
| **Pagination** | ❌ Manual | ✅ Auto (AsyncGenerator) |
| **Retry** | ❌ Basic | ✅ Tenacity (exponential) |
| **Type Safety** | ⚠️ Dicts | ✅ Pydantic models |
| **Interface** | ❌ Inconsistent | ✅ Uniform (list/get/create/edit/delete) |
| **Testability** | ⚠️ Hard to mock | ✅ Dependency injection |
| **Documentation** | ⚠️ Minimal | ✅ Comprehensive |
| **Rate Limiting** | ⚠️ Basic | ✅ Respect Retry-After |

## Best Practices Implemented

1. **Pure Functions**: All validation in `validation.py` with no side effects
2. **Guard Clauses**: Early returns for error conditions
3. **Composition**: Services compose BaseService, not inherit
4. **Explicit over Implicit**: Clear method names, explicit parameters
5. **Fail Fast**: Validation before API calls
6. **Resource Management**: Proper async context managers

## Future Improvements

1. **Caching**: LRU cache for profiles/portfolios
2. **Batching**: Automatic request batching for bulk operations
3. **Metrics**: Prometheus metrics for API calls
4. **Circuit Breaker**: Fail fast when API is down
5. **Webhooks**: Support for Amazon's webhook notifications

## Conclusion

This architecture provides:
- ✅ **Better than open-source**: Native async, uniform interface, professional retry
- ✅ **Production-ready**: Comprehensive testing, type safety, proper error handling
- ✅ **Maintainable**: Clear separation of concerns, pure functions, good documentation
- ✅ **Extensible**: Easy to add new endpoints or services
