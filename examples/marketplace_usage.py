import asyncio
from aio_amazon_ads import AmazonAdsClient, Marketplace, COUNTRY_TO_MARKETPLACE


async def eu_example():
    # Method 1: Explicit marketplace enum
    async with AmazonAdsClient(
        refresh_token="...",
        profile_id="123",
        client_id="...",
        client_secret="...",
        marketplace=Marketplace.EU,  # For DE, UK, FR, IT, ES, etc.
    ) as client:
        campaigns = await client.sp.campaigns.list()
        print(f"EU campaigns: {len(campaigns)}")


async def auto_detect_example():
    # Method 2: Auto-detect from country code
    country_code = "DE"  # Could come from user input
    marketplace = COUNTRY_TO_MARKETPLACE.get(country_code, Marketplace.NA)

    async with AmazonAdsClient(
        refresh_token="...",
        profile_id="123",
        client_id="...",
        client_secret="...",
        marketplace=marketplace,
    ) as client:
        campaigns = await client.sp.campaigns.list()


async def all_marketplaces_example():
    # Method 3: Query all marketplaces
    credentials = {
        "refresh_token": "...",
        "client_id": "...",
        "client_secret": "...",
    }

    for marketplace in [Marketplace.NA, Marketplace.EU, Marketplace.FE]:
        try:
            async with AmazonAdsClient(
                profile_id="123", marketplace=marketplace, **credentials
            ) as client:
                profiles = await client.profiles.list()
                print(f"{marketplace.name}: {len(profiles)} profiles")
        except Exception as e:
            print(f"{marketplace.name}: No access ({e})")


if __name__ == "__main__":
    asyncio.run(eu_example())
