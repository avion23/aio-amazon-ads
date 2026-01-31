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


class AmazonAdsClient(BaseClient):
    """Async client for Amazon Advertising API.

    Provides namespaced access to 70+ endpoints:
    - client.sp.campaigns.list()
    - client.sp.keywords.create()
    - etc.

    Example:
        async with AmazonAdsClient(
            refresh_token="...",
            profile_id="...",
            client_id="...",
            client_secret="...",
        ) as client:
            campaigns = await client.sp.campaigns.list()
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
