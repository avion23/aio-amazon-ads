"""Sponsored Products product ads service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService


class ProductAds(BaseService):
    """Sponsored Products product ad management."""

    async def list(
        self,
        campaign_id_filter: str | None = None,
        ad_group_id_filter: str | None = None,
        ad_id_filter: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """List Sponsored Products product ads.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID
            ad_id_filter: Filter by specific ad ID

        Yields:
            Product ad dictionaries
        """
        params: dict[str, Any] = {}
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter is not None:
            params["adGroupIdFilter"] = ad_group_id_filter
        if ad_id_filter is not None:
            params["adIdFilter"] = ad_id_filter

        response = await self._request("GET", "/v2/sp/productAds", params=params)
        for item in response.json():
            yield item

    async def get(self, ad_id: str) -> dict:
        """Get a specific Sponsored Products product ad.

        Args:
            ad_id: Product ad identifier

        Returns:
            Product ad dictionary
        """
        from ...validation import validate_ad_id

        validate_ad_id(ad_id)

        response = await self._request("GET", f"/v2/sp/productAds/{ad_id}")
        return response.json()

    async def create(self, ads: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Products product ads.

        Args:
            ads: List of product ad objects to create

        Returns:
            List of created product ad dictionaries
        """
        from ...validation import validate_product_ads_for_create

        validate_product_ads_for_create(ads)

        response = await self._request("POST", "/v2/sp/productAds", json_data=ads)
        return response.json()

    async def edit(self, ads: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Products product ads.

        Args:
            ads: List of product ad objects to update

        Returns:
            List of updated product ad dictionaries
        """
        from ...validation import validate_product_ads_for_update

        validate_product_ads_for_update(ads)

        response = await self._request("PUT", "/v2/sp/productAds", json_data=ads)
        return response.json()

    async def delete(self, ad_id: str) -> dict:
        """Delete a Sponsored Products product ad.

        Args:
            ad_id: Product ad identifier

        Returns:
            Deletion response dictionary
        """
        from ...validation import validate_ad_id

        validate_ad_id(ad_id)

        response = await self._request("DELETE", f"/v2/sp/productAds/{ad_id}")
        return response.json()
