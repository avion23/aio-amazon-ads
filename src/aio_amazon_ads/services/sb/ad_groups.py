"""Sponsored Brands ad groups service."""

import builtins
from collections.abc import AsyncGenerator

from ...base import BaseService


class AdGroups(BaseService):
    """Sponsored Brands ad groups API service."""

    async def list(self, **filters) -> AsyncGenerator[dict, None]:
        """List Sponsored Brands ad groups with auto-pagination.

        Args:
            **filters: Optional query parameters (campaignIdFilter, adGroupIdFilter, etc.)

        Yields:
            Ad group dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sb/adGroups", params=params)
            data = response.json()
            for ad_group in data.get("adGroups", []):
                yield ad_group
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, ad_group_id: str) -> dict:
        """Get a specific Sponsored Brands ad group.

        Args:
            ad_group_id: Ad group identifier

        Returns:
            Ad group dictionary
        """
        from ...validation import validate_ad_group_id

        validate_ad_group_id(ad_group_id)

        response = await self._request("GET", f"/v2/sb/adGroups/{ad_group_id}")
        return response.json()

    async def create(self, ad_groups: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Brands ad groups.

        Args:
            ad_groups: List of ad group objects to create

        Returns:
            List of created ad group dictionaries
        """
        from ...validation import validate_ad_groups_for_create

        validate_ad_groups_for_create(ad_groups)

        response = await self._request("POST", "/v2/sb/adGroups", json_data=ad_groups)
        return response.json()

    async def edit(self, ad_groups: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Brands ad groups.

        Args:
            ad_groups: List of ad group objects to update

        Returns:
            List of updated ad group dictionaries
        """
        from ...validation import validate_ad_groups_for_update

        validate_ad_groups_for_update(ad_groups)

        response = await self._request("PUT", "/v2/sb/adGroups", json_data=ad_groups)
        return response.json()
