"""Sponsored Products keywords service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService


class Keywords(BaseService):
    """Sponsored Products keyword management."""

    async def list(
        self,
        campaign_id_filter: str | None = None,
        ad_group_id_filter: str | None = None,
        keyword_id_filter: str | None = None,
    ) -> AsyncGenerator[dict, None]:
        """List Sponsored Products keywords.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID
            keyword_id_filter: Filter by keyword ID

        Returns:
            Async generator yielding keyword dictionaries
        """
        params: dict[str, Any] = {}
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter is not None:
            params["adGroupIdFilter"] = ad_group_id_filter
        if keyword_id_filter is not None:
            params["keywordIdFilter"] = keyword_id_filter

        response = await self._request("GET", "/v2/sp/keywords", params=params)
        for keyword in response.json():
            yield keyword

    async def get(self, keyword_id: str) -> dict:
        """Get a specific Sponsored Products keyword.

        Args:
            keyword_id: Keyword identifier

        Returns:
            Keyword dictionary
        """
        from ...validation import validate_keyword_id

        validate_keyword_id(keyword_id)

        response = await self._request("GET", f"/v2/sp/keywords/{keyword_id}")
        return response.json()

    async def create(self, keywords: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Products keywords.

        Args:
            keywords: List of keyword objects to create

        Returns:
            List of created keyword dictionaries
        """
        from ...validation import validate_keywords_for_create

        validate_keywords_for_create(keywords)

        response = await self._request("POST", "/v2/sp/keywords", json_data=keywords)
        return response.json()

    async def edit(self, keywords: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Products keywords.

        Args:
            keywords: List of keyword objects to update

        Returns:
            List of updated keyword dictionaries
        """
        from ...validation import validate_keywords_for_update

        validate_keywords_for_update(keywords)

        response = await self._request("PUT", "/v2/sp/keywords", json_data=keywords)
        return response.json()

    async def delete(self, keyword_id: str) -> dict:
        """Delete a Sponsored Products keyword.

        Args:
            keyword_id: Keyword identifier

        Returns:
            Deletion response dictionary
        """
        from ...validation import validate_keyword_id

        validate_keyword_id(keyword_id)

        response = await self._request("DELETE", f"/v2/sp/keywords/{keyword_id}")
        return response.json()
