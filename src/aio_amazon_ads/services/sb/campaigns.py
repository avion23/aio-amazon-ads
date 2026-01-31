"""Sponsored Brands campaigns service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService
from ...validation import (
    validate_campaign_id,
    validate_campaigns_for_create,
    validate_campaigns_for_update,
)


class Campaigns(BaseService):
    """Sponsored Brands campaign management."""

    async def list(self, **filters: Any) -> AsyncGenerator[dict, None]:
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

    async def get(self, campaign_id: str) -> dict:
        """Get a specific Sponsored Brands campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Campaign dictionary
        """
        validate_campaign_id(campaign_id)

        response = await self._request("GET", f"/v2/sb/campaigns/{campaign_id}")
        return response.json()

    async def create(self, campaigns: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Brands campaigns.

        Args:
            campaigns: List of campaign objects to create

        Returns:
            List of created campaign dictionaries
        """
        validate_campaigns_for_create(campaigns)

        response = await self._request("POST", "/v2/sb/campaigns", json_data=campaigns)
        return response.json()

    async def edit(self, campaigns: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Brands campaigns.

        Args:
            campaigns: List of campaign objects to update

        Returns:
            List of updated campaign dictionaries
        """
        validate_campaigns_for_update(campaigns)

        response = await self._request("PUT", "/v2/sb/campaigns", json_data=campaigns)
        return response.json()

    async def delete(self, campaign_id: str) -> dict:
        """Delete a Sponsored Brands campaign.

        Args:
            campaign_id: Campaign identifier

        Returns:
            Deletion response dictionary
        """
        validate_campaign_id(campaign_id)

        response = await self._request("DELETE", f"/v2/sb/campaigns/{campaign_id}")
        return response.json()
