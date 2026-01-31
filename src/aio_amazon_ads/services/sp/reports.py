"""Sponsored Products reports service."""


import httpx

from ...base import BaseService


class Reports(BaseService):
    """Sponsored Products report management."""

    async def create(self, report_date: str, metrics: list[str]) -> str:
        """Create a Sponsored Products report.

        Args:
            report_date: Report date in YYYYMMDD format
            metrics: List of metrics to include in report

        Returns:
            Report ID string
        """
        if not report_date:
            raise ValueError("report_date is required")
        if not metrics:
            raise ValueError("metrics list cannot be empty")

        data = {
            "reportDate": report_date,
            "metrics": metrics,
        }

        response = await self._request("POST", "/v2/sp/reports", json_data=data)
        return response.json()["reportId"]

    async def get_status(self, report_id: str) -> dict:
        """Get status of a Sponsored Products report.

        Args:
            report_id: Report identifier

        Returns:
            Report status dictionary containing status and fileUrl if ready
        """
        if not report_id:
            raise ValueError("report_id is required")

        response = await self._request("GET", f"/v2/sp/reports/{report_id}")
        return response.json()

    async def download(self, url: str) -> bytes:
        """Download a Sponsored Products report file.

        Args:
            url: Report download URL

        Returns:
            Report file content as bytes
        """
        if not url:
            raise ValueError("url is required")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise Exception(f"Download failed: {response.status_code}")
            return response.content
