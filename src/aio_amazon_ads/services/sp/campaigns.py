"""Sponsored Products campaigns service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService


class Campaigns(BaseService):
    """Sponsored Products campaign management."""

    async def list(
        self,
        state_filter: str | None = None,
        campaign_id_filter: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """List Sponsored Products campaigns with auto-pagination.

        Args:
            state_filter: Filter by campaign state (ENABLED, PAUSED, ARCHIVED)
            campaign_id_filter: Filter by specific campaign ID

        Yields:
            Campaign dictionaries
        """
        from ...validation import validate_campaign_state

        validate_campaign_state(state_filter)

        params: dict[str, Any] = {}
        if state_filter is not None:
            params["stateFilter"] = state_filter
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter

        while True:
            response = await self._request("GET", "/v2/sp/campaigns", params=params)
            data = response.json()

            if isinstance(data, list):
                campaigns = data
                next_token = None
            else:
                campaigns = data.get("campaigns", [])
                next_token = data.get("nextToken")

            for campaign in campaigns:
                yield campaign

            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, campaign_id: str) -> dict:
        """Get a specific Sponsored Products campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Campaign dictionary
        """
        from ...validation import validate_campaign_id

        validate_campaign_id(campaign_id)

        response = await self._request("GET", f"/v2/sp/campaigns/{campaign_id}")
        return response.json()

    async def create(self, campaigns: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Products campaigns.

        Args:
            campaigns: List of campaign objects to create

        Returns:
            List of created campaign dictionaries
        """
        from ...validation import validate_campaigns_for_create

        validate_campaigns_for_create(campaigns)

        response = await self._request("POST", "/v2/sp/campaigns", json_data=campaigns)
        return response.json()

    async def edit(self, campaigns: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Products campaigns.

        Args:
            campaigns: List of campaign objects to update

        Returns:
            List of updated campaign dictionaries
        """
        from ...validation import validate_campaigns_for_update

        validate_campaigns_for_update(campaigns)

        response = await self._request("PUT", "/v2/sp/campaigns", json_data=campaigns)
        return response.json()

    async def delete(self, campaign_id: str) -> dict:
        """Delete a Sponsored Products campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Deletion response dictionary
        """
        from ...validation import validate_campaign_id

        validate_campaign_id(campaign_id)

        response = await self._request("DELETE", f"/v2/sp/campaigns/{campaign_id}")
        return response.json()
