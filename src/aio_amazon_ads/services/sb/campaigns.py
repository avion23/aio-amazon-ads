"""Sponsored Brands campaigns service."""

from typing import Any, AsyncGenerator, Dict, List, Optional

from ...base import BaseService


class Campaigns(BaseService):
    """Sponsored Brands campaign management."""

    async def list(self, **filters) -> AsyncGenerator[Dict, None]:
        """List Sponsored Brands campaigns with auto-pagination.

        Args:
            **filters: Optional query parameters (stateFilter, campaignIdFilter, etc.)

        Yields:
            Campaign dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sb/campaigns", params=params)
            data = response.json()

            if isinstance(data, list):
                for campaign in data:
                    yield campaign
                break

            for campaign in data.get("campaigns", []):
                yield campaign
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, campaign_id: str) -> Dict:
        """Get a specific Sponsored Brands campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Campaign dictionary
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        response = await self._request("GET", f"/v2/sb/campaigns/{campaign_id}")
        return response.json()

    async def create(self, campaigns: List[Dict]) -> List[Dict]:
        """Create Sponsored Brands campaigns.

        Args:
            campaigns: List of campaign objects to create

        Returns:
            List of created campaign dictionaries
        """
        if not campaigns:
            raise ValueError("campaigns list cannot be empty")

        response = await self._request("POST", "/v2/sb/campaigns", json_data=campaigns)
        return response.json()

    async def edit(self, campaigns: List[Dict]) -> List[Dict]:
        """Edit Sponsored Brands campaigns.

        Args:
            campaigns: List of campaign objects to update

        Returns:
            List of updated campaign dictionaries
        """
        if not campaigns:
            raise ValueError("campaigns list cannot be empty")

        for campaign in campaigns:
            if "campaignId" not in campaign:
                raise ValueError("Each campaign must have campaignId")

        response = await self._request("PUT", "/v2/sb/campaigns", json_data=campaigns)
        return response.json()

    async def delete(self, campaign_id: str) -> Dict:
        """Delete a Sponsored Brands campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Deletion response dictionary
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        response = await self._request("DELETE", f"/v2/sb/campaigns/{campaign_id}")
        return response.json()
