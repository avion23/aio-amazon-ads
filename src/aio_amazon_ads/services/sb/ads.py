"""Sponsored Brands ads service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService
from ...validation import (
    validate_ad_id,
    validate_product_ads_for_create,
    validate_product_ads_for_update,
)


class Ads(BaseService):
    """Sponsored Brands ad management."""

    async def list(self, **filters: Any) -> AsyncGenerator[dict, None]:
        """List Sponsored Brands ads with auto-pagination.

        Args:
            **filters: Optional query parameters (campaignIdFilter, adIdFilter, etc.)

        Yields:
            Ad dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sb/ads", params=params)
            data = response.json()
            for ad in data.get("ads", []):
                yield ad
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, ad_id: str) -> dict:
        """Get a specific Sponsored Brands ad.

        Args:
            ad_id: Ad identifier

        Returns:
            Ad dictionary
        """
        validate_ad_id(ad_id)

        response = await self._request("GET", f"/v2/sb/ads/{ad_id}")
        return response.json()

    async def create(self, ads: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Brands ads.

        Args:
            ads: List of ad objects to create

        Returns:
            List of created ad dictionaries
        """
        validate_product_ads_for_create(ads)

        response = await self._request("POST", "/v2/sb/ads", json_data=ads)
        return response.json()

    async def edit(self, ads: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Brands ads.

        Args:
            ads: List of ad objects to update

        Returns:
            List of updated ad dictionaries
        """
        validate_product_ads_for_update(ads)

        response = await self._request("PUT", "/v2/sb/ads", json_data=ads)
        return response.json()
