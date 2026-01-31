"""Sponsored Products ad groups service."""

from typing import Any, Dict, List, Optional

from ...base import BaseService


class AdGroups(BaseService):
    """Sponsored Products ad groups API service."""

    async def list(
        self,
        campaign_id_filter: Optional[str] = None,
        ad_group_id_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List ad groups with optional filters.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID

        Returns:
            List of ad group objects
        """
        if not campaign_id_filter and not ad_group_id_filter:
            response = await self._request("GET", "/sp/adGroups")
            return response.json()

        params: Dict[str, str] = {}
        if campaign_id_filter:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter:
            params["adGroupIdFilter"] = ad_group_id_filter

        response = await self._request("GET", "/sp/adGroups", params=params)
        return response.json()

    async def get(self, ad_group_id: str) -> Dict[str, Any]:
        """Get a single ad group by ID.

        Args:
            ad_group_id: Ad group identifier

        Returns:
            Ad group object
        """
        if not ad_group_id:
            raise ValueError("ad_group_id is required")

        response = await self._request("GET", f"/sp/adGroups/{ad_group_id}")
        return response.json()

    async def create(self, ad_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create new ad groups.

        Args:
            ad_groups: List of ad group objects to create

        Returns:
            List of created ad group objects
        """
        if not ad_groups:
            raise ValueError("ad_groups list cannot be empty")

        response = await self._request("POST", "/sp/adGroups", json_data=ad_groups)
        return response.json()

    async def edit(self, ad_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Update existing ad groups.

        Args:
            ad_groups: List of ad group objects to update

        Returns:
            List of updated ad group objects
        """
        if not ad_groups:
            raise ValueError("ad_groups list cannot be empty")

        response = await self._request("PUT", "/sp/adGroups", json_data=ad_groups)
        return response.json()

    async def delete(self, ad_group_id: str) -> Dict[str, Any]:
        """Delete an ad group.

        Args:
            ad_group_id: Ad group identifier

        Returns:
            Deletion response
        """
        if not ad_group_id:
            raise ValueError("ad_group_id is required")

        response = await self._request("DELETE", f"/sp/adGroups/{ad_group_id}")
        return response.json()
