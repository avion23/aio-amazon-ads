# amzn-ads Package Summary

## Overview
Native async Python client for Amazon Advertising API with clean namespacing and 30+ endpoints implemented.

## Package Structure
```
amzn-ads/
├── src/amzn_ads/
│   ├── __init__.py          # Public API exports
│   ├── base.py              # BaseClient with auth & HTTP
│   ├── client.py            # Main AmazonAdsClient with namespacing
│   ├── exceptions.py        # Custom exceptions
│   └── services/
│       └── sp/              # Sponsored Products
│           ├── campaigns.py     # 5 methods
│           ├── ad_groups.py     # 5 methods
│           ├── keywords.py      # 5 methods
│           ├── product_ads.py   # 5 methods
│           ├── negative_keywords.py  # 3 methods
│           ├── targets.py       # 5 methods
│           └── reports.py       # 3 methods
├── tests/
│   └── unit/
│       └── test_client.py   # 4 passing tests
├── pyproject.toml
├── LICENSE (MIT)
└── README.md
```

## Implemented Endpoints (31 total)

### Sponsored Products V2 (31 methods)
- **Campaigns**: list, get, create, edit, delete
- **Ad Groups**: list, get, create, edit, delete
- **Keywords**: list, get, create, edit, delete
- **Product Ads**: list, get, create, edit, delete
- **Negative Keywords**: list, create, delete
- **Targets**: list, get, create, edit, delete
- **Reports**: create, get_status, download

## Usage Example

```python
from amzn_ads import AmazonAdsClient

async with AmazonAdsClient(
    refresh_token="...",
    profile_id="...",
    client_id="...",
    client_secret="...",
) as client:
    # List campaigns
    campaigns = await client.sp.campaigns.list()
    
    # Create keywords
    keywords = await client.sp.keywords.create([...])
    
    # Get report status
    status = await client.sp.reports.get_status(report_id)
```

## Key Features
- Native async/await with httpx
- OAuth token management with auto-refresh
- Retry logic with exponential backoff
- Namespaced API (client.sp.campaigns.list())
- Type hints throughout
- MIT License

## Tests
All 4 tests passing:
- Client initialization
- Async context manager
- SP service access (campaigns)
- SP service access (keywords)

## Dependencies
- httpx >= 0.27.0
- msgspec >= 0.18.0 (for future models)

## Next Steps (Not Implemented)
- Sponsored Brands (SB) services
- Sponsored Display (SD) services
- Portfolio management
- Profile management
- Additional 40+ endpoints

## Installation
```bash
pip install -e /Users/avion/Documents.nosync/projects/paul/amzn-ads
```

## Git Repository
Initialized at: /Users/avion/Documents.nosync/projects/paul/amzn-ads
First commit: ff3c461
