"""Sponsored Display ad groups service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService
from ...validation import (
    validate_ad_group_id,
    validate_ad_groups_for_create,
)


class AdGroups(BaseService):
    """Sponsored Display ad group management."""

    async def list(self, **filters: Any) -> AsyncGenerator[dict, None]:
        """List Sponsored Display ad groups with auto-pagination.

        Args:
            **filters: Optional query parameters (campaignIdFilter, adGroupIdFilter, etc.)

        Yields:
            Ad group dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sd/adGroups", params=params)
            data = response.json()
            for ad_group in data.get("adGroups", []):
                yield ad_group
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, ad_group_id: str) -> dict:
        """Get a specific Sponsored Display ad group.

        Args:
            ad_group_id: Ad group identifier

        Returns:
            Ad group dictionary
        """
        validate_ad_group_id(ad_group_id)

        response = await self._request("GET", f"/v2/sd/adGroups/{ad_group_id}")
        return response.json()

    async def create(self, ad_groups: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Display ad groups.

        Args:
            ad_groups: List of ad group objects to create

        Returns:
            List of created ad group dictionaries
        """
        validate_ad_groups_for_create(ad_groups)

        response = await self._request("POST", "/v2/sd/adGroups", json_data=ad_groups)
        return response.json()
