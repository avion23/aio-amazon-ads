"""Sponsored Brands ads service."""

from typing import Any, AsyncGenerator, Dict, List

from ...base import BaseService


class Ads(BaseService):
    """Sponsored Brands ad management."""

    async def list(self, **filters) -> AsyncGenerator[Dict, None]:
        """List Sponsored Brands ads with auto-pagination.

        Args:
            **filters: Optional query parameters (campaignIdFilter, adIdFilter, etc.)

        Yields:
            Ad dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/sb/ads", params=params)
            data = response.json()
            for ad in data.get("ads", []):
                yield ad
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, ad_id: str) -> Dict:
        """Get a specific Sponsored Brands ad.

        Args:
            ad_id: Ad identifier

        Returns:
            Ad dictionary
        """
        if not ad_id:
            raise ValueError("ad_id is required")

        response = await self._request("GET", f"/v2/sb/ads/{ad_id}")
        return response.json()

    async def create(self, ads: List[Dict]) -> List[Dict]:
        """Create Sponsored Brands ads.

        Args:
            ads: List of ad objects to create

        Returns:
            List of created ad dictionaries
        """
        if not ads:
            raise ValueError("ads list cannot be empty")

        response = await self._request("POST", "/v2/sb/ads", json_data=ads)
        return response.json()

    async def edit(self, ads: List[Dict]) -> List[Dict]:
        """Edit Sponsored Brands ads.

        Args:
            ads: List of ad objects to update

        Returns:
            List of updated ad dictionaries
        """
        if not ads:
            raise ValueError("ads list cannot be empty")

        for ad in ads:
            if "adId" not in ad:
                raise ValueError("Each ad must have adId")

        response = await self._request("PUT", "/v2/sb/ads", json_data=ads)
        return response.json()
