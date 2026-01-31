"""Sponsored Brands ad groups service."""

from typing import Any, AsyncGenerator, Dict, List

from ...base import BaseService


class AdGroups(BaseService):
    """Sponsored Brands ad groups API service."""

    async def list(self, **filters) -> AsyncGenerator[Dict, None]:
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

    async def get(self, ad_group_id: str) -> Dict:
        """Get a specific Sponsored Brands ad group.

        Args:
            ad_group_id: Ad group identifier

        Returns:
            Ad group dictionary
        """
        if not ad_group_id:
            raise ValueError("ad_group_id is required")

        response = await self._request("GET", f"/v2/sb/adGroups/{ad_group_id}")
        return response.json()

    async def create(self, ad_groups: List[Dict]) -> List[Dict]:
        """Create Sponsored Brands ad groups.

        Args:
            ad_groups: List of ad group objects to create

        Returns:
            List of created ad group dictionaries
        """
        if not ad_groups:
            raise ValueError("ad_groups list cannot be empty")

        response = await self._request("POST", "/v2/sb/adGroups", json_data=ad_groups)
        return response.json()

    async def edit(self, ad_groups: List[Dict]) -> List[Dict]:
        """Edit Sponsored Brands ad groups.

        Args:
            ad_groups: List of ad group objects to update

        Returns:
            List of updated ad group dictionaries
        """
        if not ad_groups:
            raise ValueError("ad_groups list cannot be empty")

        for ad_group in ad_groups:
            if "adGroupId" not in ad_group:
                raise ValueError("Each ad group must have adGroupId")

        response = await self._request("PUT", "/v2/sb/adGroups", json_data=ad_groups)
        return response.json()
