"""Profiles service and models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ...base import BaseService


class Profile(BaseModel):
    profileId: str
    countryCode: str
    currencyCode: str
    timezone: str
    accountName: Optional[str] = None
    type: Optional[str] = None

    class Config:
        extra = "ignore"


class Profiles(BaseService):
    """Profile management service."""

    async def list(self) -> List[Dict]:
        """List all profiles.

        Returns:
            List of profile dictionaries
        """
        response = await self._request("GET", "/v2/profiles")
        return response.json()

    async def get(self, profile_id: str) -> Dict:
        """Get a single profile.

        Args:
            profile_id: Profile identifier

        Returns:
            Profile dictionary
        """
        if not profile_id:
            raise ValueError("profile_id is required")

        response = await self._request("GET", f"/v2/profiles/{profile_id}")
        return response.json()
