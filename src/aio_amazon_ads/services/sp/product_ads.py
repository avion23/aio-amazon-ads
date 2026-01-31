"""Sponsored Products product ads service."""

from typing import Any, AsyncGenerator, Dict, List, Optional

from ...base import BaseService


class ProductAds(BaseService):
    """Sponsored Products product ad management."""

    async def list(
        self,
        campaign_id_filter: Optional[str] = None,
        ad_group_id_filter: Optional[str] = None,
        ad_id_filter: Optional[str] = None,
    ) -> AsyncGenerator[Dict, None]:
        """List Sponsored Products product ads.

        Args:
            campaign_id_filter: Filter by campaign ID
            ad_group_id_filter: Filter by ad group ID
            ad_id_filter: Filter by specific ad ID

        Yields:
            Product ad dictionaries
        """
        params: Dict[str, Any] = {}
        if campaign_id_filter is not None:
            params["campaignIdFilter"] = campaign_id_filter
        if ad_group_id_filter is not None:
            params["adGroupIdFilter"] = ad_group_id_filter
        if ad_id_filter is not None:
            params["adIdFilter"] = ad_id_filter

        response = await self._request("GET", "/v2/sp/productAds", params=params)
        for item in response.json():
            yield item

    async def get(self, ad_id: str) -> Dict:
        """Get a specific Sponsored Products product ad.

        Args:
            ad_id: Product ad identifier

        Returns:
            Product ad dictionary
        """
        if not ad_id:
            raise ValueError("ad_id is required")

        response = await self._request("GET", f"/v2/sp/productAds/{ad_id}")
        return response.json()

    async def create(self, ads: List[Dict]) -> List[Dict]:
        """Create Sponsored Products product ads.

        Args:
            ads: List of product ad objects to create

        Returns:
            List of created product ad dictionaries
        """
        if not ads:
            raise ValueError("ads list cannot be empty")

        response = await self._request("POST", "/v2/sp/productAds", json_data=ads)
        return response.json()

    async def edit(self, ads: List[Dict]) -> List[Dict]:
        """Edit Sponsored Products product ads.

        Args:
            ads: List of product ad objects to update

        Returns:
            List of updated product ad dictionaries
        """
        if not ads:
            raise ValueError("ads list cannot be empty")

        for ad in ads:
            if "adId" not in ad:
                raise ValueError("Each ad must have adId")

        response = await self._request("PUT", "/v2/sp/productAds", json_data=ads)
        return response.json()

    async def delete(self, ad_id: str) -> Dict:
        """Delete a Sponsored Products product ad.

        Args:
            ad_id: Product ad identifier

        Returns:
            Deletion response dictionary
        """
        if not ad_id:
            raise ValueError("ad_id is required")

        response = await self._request("DELETE", f"/v2/sp/productAds/{ad_id}")
        return response.json()
