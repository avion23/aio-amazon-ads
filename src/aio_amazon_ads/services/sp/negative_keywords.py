"""Sponsored Products negative keywords service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService


class NegativeKeywords(BaseService):
    """Sponsored Products negative keyword management."""

    async def list(
        self,
        campaign_id_filter: str | None = None,
        ad_group_id_filter: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """List Sponsored Products negative keywords.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID

        Yields:
            Negative keyword dictionaries
        """
        params: dict[str, Any] = {}
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter is not None:
            params["adGroupIdFilter"] = ad_group_id_filter

        response = await self._request("GET", "/v2/sp/negativeKeywords", params=params)
        for item in response.json():
            yield item

    async def create(self, keywords: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Products negative keywords.

        Args:
            keywords: List of negative keyword objects to create

        Returns:
            List of created negative keyword dictionaries
        """
        if not keywords:
            raise ValueError("keywords list cannot be empty")

        response = await self._request("POST", "/v2/sp/negativeKeywords", json_data=keywords)
        return response.json()

    async def delete(self, keyword_id: str) -> dict:
        """Delete a Sponsored Products negative keyword.

        Args:
            keyword_id: Negative keyword identifier

        Returns:
            Deletion response dictionary
        """
        if not keyword_id:
            raise ValueError("keyword_id is required")

        response = await self._request("DELETE", f"/v2/sp/negativeKeywords/{keyword_id}")
        return response.json()
