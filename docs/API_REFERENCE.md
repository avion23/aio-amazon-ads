# API Reference

## AmazonAdsClient

Main entry point for the Amazon Advertising API client.

### Constructor

```python
AmazonAdsClient(
    refresh_token: str,
    profile_id: str,
    client_id: str,
    client_secret: str,
    marketplace: Marketplace = Marketplace.NA,
)
```

**Parameters:**
- `refresh_token` (str): OAuth refresh token from LWA
- `profile_id` (str): Amazon Advertising profile ID
- `client_id` (str): LWA client ID
- `client_secret` (str): LWA client secret
- `marketplace` (Marketplace): Amazon marketplace region. Defaults to `Marketplace.NA`. Available values:
  - `Marketplace.NA` - North America (US, CA, MX, BR)
  - `Marketplace.EU` - Europe (UK, DE, FR, IT, ES, NL, PL, TR, SE, BE, EG)
  - `Marketplace.FE` - Far East (JP, SG, AU, IN)
  - `Marketplace.CN` - China

**Example:**
```python
from aio_amazon_ads import AmazonAdsClient, Marketplace

# EU marketplace for Germany, UK, France, etc.
async with AmazonAdsClient(
    refresh_token="Atzr|...",
    profile_id="123456789",
    client_id="amzn1.application-oa2-client....",
    client_secret="...",
    marketplace=Marketplace.EU,
) as client:
    campaigns = await client.sp.campaigns.list()
```

### Marketplace Auto-Detection

The library provides `COUNTRY_TO_MARKETPLACE` mapping for automatic marketplace selection:

```python
from aio_amazon_ads import COUNTRY_TO_MARKETPLACE, Marketplace

country_code = "DE"  # From profile data
marketplace = COUNTRY_TO_MARKETPLACE[country_code]  # Marketplace.EU
```

### Context Manager

The client must be used as an async context manager:

```python
async with AmazonAdsClient(...) as client:
    campaigns = await client.sp.campaigns.list()
```

### Services

#### Sponsored Products (`client.sp`)

##### Campaigns

```python
# List all campaigns (auto-paginated)
async for campaign in client.sp.campaigns.list():
    print(campaign["name"])

# List with filters
async for campaign in client.sp.campaigns.list(stateFilter="ENABLED"):
    process(campaign)

# Get single campaign
campaign = await client.sp.campaigns.get("123456")

# Create campaigns
new_campaigns = await client.sp.campaigns.create([
    {
        "name": "My Campaign",
        "campaignType": "sponsoredProducts",
        "targetingType": "manual",
        "state": "enabled",
        "dailyBudget": 50.0,
        "startDate": "2026-02-01",
    }
])

# Update campaigns
updated = await client.sp.campaigns.edit([
    {"campaignId": "123", "dailyBudget": 75.0}
])

# Delete campaign
result = await client.sp.campaigns.delete("123456")
```

##### Ad Groups

```python
# List ad groups
async for ad_group in client.sp.ad_groups.list():
    print(ad_group["name"])

# Get single ad group
ad_group = await client.sp.ad_groups.get("789012")

# Create ad groups
new_ad_groups = await client.sp.ad_groups.create([
    {
        "campaignId": "123",
        "name": "My Ad Group",
        "state": "enabled",
        "defaultBid": 1.50,
    }
])

# Update ad groups
updated = await client.sp.ad_groups.edit([
    {"adGroupId": "789", "defaultBid": 2.00}
])

# Delete ad group
result = await client.sp.ad_groups.delete("789012")
```

##### Keywords

```python
# List keywords
async for keyword in client.sp.keywords.list():
    print(keyword["keywordText"])

# Get single keyword
keyword = await client.sp.keywords.get("345678")

# Create keywords
new_keywords = await client.sp.keywords.create([
    {
        "campaignId": "123",
        "adGroupId": "789",
        "keywordText": "running shoes",
        "matchType": "exact",
        "state": "enabled",
        "bid": 1.50,
    }
])

# Update keywords
updated = await client.sp.keywords.edit([
    {"keywordId": "345", "bid": 2.00}
])

# Delete keyword
result = await client.sp.keywords.delete("345678")
```

##### Product Ads

```python
# List product ads
async for ad in client.sp.product_ads.list():
    print(ad["asin"])

# Get single product ad
ad = await client.sp.product_ads.get("901234")

# Create product ads
new_ads = await client.sp.product_ads.create([
    {
        "campaignId": "123",
        "adGroupId": "789",
        "asin": "B123456789",
        "state": "enabled",
    }
])

# Update product ads
updated = await client.sp.product_ads.edit([
    {"adId": "901", "state": "paused"}
])

# Delete product ad
result = await client.sp.product_ads.delete("901234")
```

##### Negative Keywords

```python
# List negative keywords
async for keyword in client.sp.negative_keywords.list():
    print(keyword["keywordText"])

# Create negative keywords
new_keywords = await client.sp.negative_keywords.create([
    {
        "campaignId": "123",
        "adGroupId": "789",
        "keywordText": "free",
        "matchType": "negativeExact",
        "state": "enabled",
    }
])

# Delete negative keyword
result = await client.sp.negative_keywords.delete("567890")
```

##### Targets

```python
# List targets
async for target in client.sp.targets.list():
    print(target["expression"])

# Get single target
target = await client.sp.targets.get("111222")

# Create targets
new_targets = await client.sp.targets.create([
    {
        "campaignId": "123",
        "adGroupId": "789",
        "expression": [{"value": "B123456789", "type": "asinSameAs"}],
        "expressionType": "manual",
        "state": "enabled",
        "bid": 1.50,
    }
])

# Update targets
updated = await client.sp.targets.edit([
    {"targetId": "111", "bid": 2.00}
])

# Delete target
result = await client.sp.targets.delete("111222")
```

##### Reports

```python
# Create report
report_id = await client.sp.reports.create(
    report_date="2026-01-01",
    metrics=["impressions", "clicks", "cost", "sales"]
)

# Check report status
status = await client.sp.reports.get_status(report_id)

# Download report (when ready)
if status["status"] == "SUCCESS":
    data = await client.sp.reports.download(status["url"])
```

#### Sponsored Brands (`client.sb`)

##### Campaigns

```python
# List SB campaigns (auto-paginated)
async for campaign in client.sb.campaigns.list():
    print(campaign["name"])

# Get single campaign
campaign = await client.sb.campaigns.get("123456")

# Create campaigns
new_campaigns = await client.sb.campaigns.create([...])

# Update campaigns
updated = await client.sb.campaigns.edit([...])

# Delete campaign
result = await client.sb.campaigns.delete("123456")
```

##### Ad Groups

```python
# List ad groups
async for ad_group in client.sb.ad_groups.list():
    print(ad_group["name"])

# Get single ad group
ad_group = await client.sb.ad_groups.get("789012")

# Create ad groups
new_ad_groups = await client.sb.ad_groups.create([...])

# Update ad groups
updated = await client.sb.ad_groups.edit([...])
```

##### Keywords

```python
# List keywords
async for keyword in client.sb.keywords.list():
    print(keyword["keywordText"])

# Get single keyword
keyword = await client.sb.keywords.get("345678")

# Create keywords
new_keywords = await client.sb.keywords.create([...])

# Update keywords
updated = await client.sb.keywords.edit([...])
```

##### Ads

```python
# List ads
async for ad in client.sb.ads.list():
    print(ad["name"])

# Get single ad
ad = await client.sb.ads.get("901234")

# Create ads
new_ads = await client.sb.ads.create([...])

# Update ads
updated = await client.sb.ads.edit([...])
```

#### Sponsored Display (`client.sd`)

##### Campaigns

```python
# List SD campaigns
async for campaign in client.sd.campaigns.list():
    print(campaign["name"])

# Get single campaign
campaign = await client.sd.campaigns.get("123456")

# Create campaigns
new_campaigns = await client.sd.campaigns.create([...])

# Update campaigns
updated = await client.sd.campaigns.edit([...])

# Delete campaign
result = await client.sd.campaigns.delete("123456")
```

##### Ad Groups

```python
# List ad groups
async for ad_group in client.sd.ad_groups.list():
    print(ad_group["name"])

# Get single ad group
ad_group = await client.sd.ad_groups.get("789012")

# Create ad groups
new_ad_groups = await client.sd.ad_groups.create([...])
```

#### Portfolios (`client.portfolios`)

```python
# List portfolios
async for portfolio in client.portfolios.list():
    print(portfolio["name"])

# Get single portfolio
portfolio = await client.portfolios.get("portfolio123")

# Create portfolios
new_portfolios = await client.portfolios.create([
    {
        "name": "My Portfolio",
        "state": "enabled",
        "budget": {"amount": 1000.0, "policy": "dateRange"},
    }
])

# Update portfolios
updated = await client.portfolios.edit([
    {"portfolioId": "portfolio123", "budget": {"amount": 1500.0}}
])

# Delete portfolio
result = await client.portfolios.delete("portfolio123")
```

#### Profiles (`client.profiles`)

```python
# List all profiles
profiles = await client.profiles.list()

# Get single profile
profile = await client.profiles.get("123456789")
```

## Error Handling

### Exception Hierarchy

```
AmazonAPIError (base)
├── AuthenticationError (401/403)
├── ThrottlingError (429)
└── ValidationError (400)
```

### Handling Errors

```python
from aio_amazon_ads import (
    AmazonAdsClient,
    AuthenticationError,
    ThrottlingError,
    ValidationError,
)

async def handle_errors():
    try:
        campaigns = await client.sp.campaigns.list()
    except AuthenticationError as e:
        # Token expired or invalid credentials
        print(f"Auth failed: {e}")
        # Token will auto-refresh on next call
    except ThrottlingError as e:
        # Rate limited - wait and retry
        print(f"Rate limited. Retry after {e.retry_after}s")
        await asyncio.sleep(e.retry_after)
    except ValidationError as e:
        # Invalid request parameters
        print(f"Validation error: {e}")
    except AmazonAPIError as e:
        # Other API errors (500, etc.)
        print(f"API error: {e}")
```

## Rate Limiting

The client automatically handles rate limiting:

- **429 errors**: Automatic retry with exponential backoff
- **Retry-After header**: Respects server-specified wait time
- **Max retries**: 3 attempts before raising ThrottlingError

## Pagination

All `list()` methods return `AsyncGenerator` for automatic pagination:

```python
# Process all campaigns (handles pagination automatically)
async for campaign in client.sp.campaigns.list():
    process(campaign)

# With filters
async for campaign in client.sp.campaigns.list(stateFilter="ENABLED"):
    if campaign["dailyBudget"] > 100:
        print(campaign["name"])
```

## Type Safety

All methods are fully typed. Use Pydantic models for IDE autocomplete:

```python
from aio_amazon_ads.models import Campaign, CampaignCreate

# IDE will autocomplete fields
campaign: Campaign = await client.sp.campaigns.get("123")
print(campaign.name)  # Autocomplete works!

# Create with typed model
new_campaign = CampaignCreate(
    name="My Campaign",
    dailyBudget=50.0,
    state="enabled",
)
```
