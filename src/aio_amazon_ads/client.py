"""Main Amazon Ads client with namespaced services."""

from collections.abc import Callable
from typing import Any

from .base import BaseClient, Marketplace
from .services.portfolios import Portfolios
from .services.profiles import Profiles
from .services.sb import AdGroups as SBAdGroups
from .services.sb import Ads as SBAds
from .services.sb import Campaigns as SBCampaigns
from .services.sb import Keywords as SBKeywords
from .services.sd import AdGroups as SDAdGroups
from .services.sd import Campaigns as SDCampaigns
from .services.sp import AdGroups as SPAdGroups
from .services.sp import Campaigns as SPCampaigns
from .services.sp import Keywords as SPKeywords
from .services.sp import NegativeKeywords as SPNegativeKeywords
from .services.sp import ProductAds as SPProductAds
from .services.sp import Reports as SPReports
from .services.sp import Targets as SPTargets


class AmazonAdsClient(BaseClient):
    """Async client for Amazon Advertising API.

    Provides namespaced access to 70+ endpoints:
    - client.sp.campaigns.list()
    - client.sb.campaigns.list()
    - client.sd.campaigns.list()
    - client.portfolios.list()
    - client.profiles.list()

    Example:
        async with AmazonAdsClient(
            refresh_token="...",
            profile_id="...",
            client_id="...",
            client_secret="...",
        ) as client:
            # SP campaigns with auto-pagination
            async for campaign in client.sp.campaigns.list():
                print(campaign["name"])

    For EU marketplace (Germany, UK, France, etc.):
        async with AmazonAdsClient(
            refresh_token="...",
            profile_id="...",
            client_id="...",
            client_secret="...",
            marketplace=Marketplace.EU,
        ) as client:
            campaigns = await client.sp.campaigns.list()
    """

    def __init__(
        self,
        refresh_token: str,
        profile_id: str,
        client_id: str,
        client_secret: str,
        marketplace: Marketplace = Marketplace.NA,
    ):
        """Initialize Amazon Ads client."""
        super().__init__(
            refresh_token=refresh_token,
            profile_id=profile_id,
            client_id=client_id,
            client_secret=client_secret,
            marketplace=marketplace,
        )

        # Sponsored Products services
        self.sp = _SPServices(self.request)

        # Sponsored Brands services
        self.sb = _SBServices(self.request)

        # Sponsored Display services
        self.sd = _SDServices(self.request)

        # Portfolios service
        self.portfolios = Portfolios(self.request)

        # Profiles service
        self.profiles = Profiles(self.request)


class _SPServices:
    """Container for Sponsored Products services."""

    def __init__(self, request: Callable[..., Any]):
        self.campaigns: SPCampaigns = SPCampaigns(request)
        self.ad_groups: SPAdGroups = SPAdGroups(request)
        self.keywords: SPKeywords = SPKeywords(request)
        self.product_ads: SPProductAds = SPProductAds(request)
        self.negative_keywords: SPNegativeKeywords = SPNegativeKeywords(request)
        self.targets: SPTargets = SPTargets(request)
        self.reports: SPReports = SPReports(request)


class _SBServices:
    """Container for Sponsored Brands services."""

    def __init__(self, request: Callable[..., Any]):
        self.campaigns: SBCampaigns = SBCampaigns(request)
        self.ad_groups: SBAdGroups = SBAdGroups(request)
        self.keywords: SBKeywords = SBKeywords(request)
        self.ads: SBAds = SBAds(request)


class _SDServices:
    """Container for Sponsored Display services."""

    def __init__(self, request: Callable[..., Any]):
        self.campaigns: SDCampaigns = SDCampaigns(request)
        self.ad_groups: SDAdGroups = SDAdGroups(request)
