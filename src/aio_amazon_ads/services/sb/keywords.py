"""Sponsored Brands keywords service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService
from ...validation import (
    validate_keyword_id,
    validate_keywords_for_create,
    validate_keywords_for_update,
)


class Keywords(BaseService):
    """Sponsored Brands keyword management."""

    async def list(self, **filters: Any) -> AsyncGenerator[dict, None]:
        """List Sponsored Brands keywords with auto-pagination.

        Args:
            **filters: Optional query parameters (campaignIdFilter, adGroupIdFilter, etc.)

        Yields:
            Keyword dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sb/keywords", params=params)
            data = response.json()
            for keyword in data.get("keywords", []):
                yield keyword
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, keyword_id: str) -> dict:
        """Get a specific Sponsored Brands keyword.

        Args:
            keyword_id: Keyword identifier

        Returns:
            Keyword dictionary
        """
        validate_keyword_id(keyword_id)

        response = await self._request("GET", f"/v2/sb/keywords/{keyword_id}")
        return response.json()

    async def create(self, keywords: builtins.list[dict]) -> builtins.list[dict]:
        """Create Sponsored Brands keywords.

        Args:
            keywords: List of keyword objects to create

        Returns:
            List of created keyword dictionaries
        """
        validate_keywords_for_create(keywords)

        response = await self._request("POST", "/v2/sb/keywords", json_data=keywords)
        return response.json()

    async def edit(self, keywords: builtins.list[dict]) -> builtins.list[dict]:
        """Edit Sponsored Brands keywords.

        Args:
            keywords: List of keyword objects to update

        Returns:
            List of updated keyword dictionaries
        """
        validate_keywords_for_update(keywords)

        response = await self._request("PUT", "/v2/sb/keywords", json_data=keywords)
        return response.json()
