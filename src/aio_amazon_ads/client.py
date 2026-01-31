"""Main Amazon Ads client with namespaced services."""

from typing import Optional

from .base import BaseClient
from .services.sp import (
    Campaigns as SPCampaigns,
    AdGroups as SPAdGroups,
    Keywords as SPKeywords,
    ProductAds as SPProductAds,
    NegativeKeywords as SPNegativeKeywords,
    Targets as SPTargets,
    Reports as SPReports,
)
from .services.sb import (
    Campaigns as SBCampaigns,
    AdGroups as SBAdGroups,
    Keywords as SBKeywords,
    Ads as SBAds,
)
from .services.sd import (
    Campaigns as SDCampaigns,
    AdGroups as SDAdGroups,
)
from .services.portfolios import Portfolios
from .services.profiles import Profiles


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
    """

    def __init__(
        self,
        refresh_token: str,
        profile_id: str,
        client_id: str,
        client_secret: str,
    ):
        """Initialize Amazon Ads client."""
        super().__init__(
            refresh_token=refresh_token,
            profile_id=profile_id,
            client_id=client_id,
            client_secret=client_secret,
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

    def __init__(self, request):
        self.campaigns = SPCampaigns(request)
        self.ad_groups = SPAdGroups(request)
        self.keywords = SPKeywords(request)
        self.product_ads = SPProductAds(request)
        self.negative_keywords = SPNegativeKeywords(request)
        self.targets = SPTargets(request)
        self.reports = SPReports(request)


class _SBServices:
    """Container for Sponsored Brands services."""

    def __init__(self, request):
        self.campaigns = SBCampaigns(request)
        self.ad_groups = SBAdGroups(request)
        self.keywords = SBKeywords(request)
        self.ads = SBAds(request)


class _SDServices:
    """Container for Sponsored Display services."""

    def __init__(self, request):
        self.campaigns = SDCampaigns(request)
        self.ad_groups = SDAdGroups(request)
