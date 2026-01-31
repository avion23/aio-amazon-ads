"""Sponsored Products campaigns service."""

from typing import Any, AsyncGenerator, Dict, List, Optional

from ...base import BaseService


class Campaigns(BaseService):
    """Sponsored Products campaign management."""

    async def list(
        self,
        state_filter: Optional[str] = None,
        campaign_id_filter: Optional[str] = None,
    ) -> AsyncGenerator[Dict, None]:
        """List Sponsored Products campaigns with auto-pagination.

        Args:
            state_filter: Filter by campaign state (ENABLED, PAUSED, ARCHIVED)
            campaign_id_filter: Filter by specific campaign ID

        Yields:
            Campaign dictionaries
        """
        from ...validation import validate_campaign_state

        validate_campaign_state(state_filter)

        params: Dict[str, Any] = {}
        if state_filter is not None:
            params["stateFilter"] = state_filter
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter

        response = await self._request("GET", "/v2/sp/campaigns", params=params)
        campaigns = response.json()

        for campaign in campaigns:
            yield campaign

    async def get(self, campaign_id: str) -> Dict:
        """Get a specific Sponsored Products campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Campaign dictionary
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        response = await self._request("GET", f"/v2/sp/campaigns/{campaign_id}")
        return response.json()

    async def create(self, campaigns: List[Dict]) -> List[Dict]:
        """Create Sponsored Products campaigns.

        Args:
            campaigns: List of campaign objects to create

        Returns:
            List of created campaign dictionaries
        """
        if not campaigns:
            raise ValueError("campaigns list cannot be empty")

        response = await self._request("POST", "/v2/sp/campaigns", json_data=campaigns)
        return response.json()

    async def edit(self, campaigns: List[Dict]) -> List[Dict]:
        """Edit Sponsored Products campaigns.

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

        response = await self._request("PUT", "/v2/sp/campaigns", json_data=campaigns)
        return response.json()

    async def delete(self, campaign_id: str) -> Dict:
        """Delete a Sponsored Products campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Deletion response dictionary
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        response = await self._request("DELETE", f"/v2/sp/campaigns/{campaign_id}")
        return response.json()
