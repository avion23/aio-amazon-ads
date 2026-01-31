"""Sponsored Products targets service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService


class Targets(BaseService):
    """Sponsored Products target management."""

    async def list(
        self,
        campaign_id_filter: str | None = None,
        ad_group_id_filter: str | None = None,
        target_id_filter: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """List Sponsored Products targets.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID
            target_id_filter: Filter by target ID

        Yields:
            Target dictionaries
        """
        params: dict[str, Any] = {}
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter is not None:
            params["adGroupIdFilter"] = ad_group_id_filter
        if target_id_filter is not None:
            params["targetIdFilter"] = target_id_filter

        response = await self._request("GET", "/v2/sp/targets", params=params)
        targets = response.json()
        for target in targets:
            yield target

    async def get(self, target_id: str) -> dict:
        """Get a specific Sponsored Products target.

        Args:
            target_id: Target identifier

        Returns:
            Target dictionary
        """
        from ...validation import validate_target_id

        validate_target_id(target_id)

        response = await self._request("GET", f"/v2/sp/targets/{target_id}")
        return response.json()

    async def create(self, targets: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Products targets.

        Args:
            targets: List of target objects to create

        Returns:
            List of created target dictionaries
        """
        from ...validation import validate_targets_for_create

        validate_targets_for_create(targets)

        response = await self._request("POST", "/v2/sp/targets", json_data=targets)
        return response.json()

    async def edit(self, targets: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Products targets.

        Args:
            targets: List of target objects to update

        Returns:
            List of updated target dictionaries
        """
        from ...validation import validate_targets_for_update

        validate_targets_for_update(targets)

        response = await self._request("PUT", "/v2/sp/targets", json_data=targets)
        return response.json()

    async def delete(self, target_id: str) -> dict:
        """Delete a Sponsored Products target.

        Args:
            target_id: Target identifier

        Returns:
            Deletion response dictionary
        """
        from ...validation import validate_target_id

        validate_target_id(target_id)

        response = await self._request("DELETE", f"/v2/sp/targets/{target_id}")
        return response.json()
