"""Portfolios service."""

from typing import Any, AsyncGenerator, Dict, List

from ...base import BaseService


Portfolio = Dict[str, Any]


class Portfolios(BaseService):
    """Portfolio management service."""

    async def list(self, **filters) -> AsyncGenerator[Portfolio, None]:
        """List portfolios with auto-pagination.

        Args:
            **filters: Optional query parameters (portfolioIdFilter, stateFilter, etc.)

        Yields:
            Portfolio dictionaries
        """
        params = filters.copy() if filters else {}
        while True:
            response = await self._request("GET", "/v2/portfolios", params=params)
            data = response.json()
            for portfolio in data.get("portfolios", []):
                yield portfolio
            next_token = data.get("nextToken")
            if not next_token:
                break
            params["nextToken"] = next_token

    async def get(self, portfolio_id: str) -> Portfolio:
        """Get a specific portfolio.

        Args:
            portfolio_id: Portfolio identifier

        Returns:
            Portfolio dictionary
        """
        if not portfolio_id:
            raise ValueError("portfolio_id is required")

        response = await self._request("GET", f"/v2/portfolios/{portfolio_id}")
        return response.json()

    async def create(self, portfolios: List[Dict]) -> List[Portfolio]:
        """Create portfolios.

        Args:
            portfolios: List of portfolio objects to create

        Returns:
            List of created portfolio dictionaries
        """
        if not portfolios:
            raise ValueError("portfolios list cannot be empty")

        response = await self._request("POST", "/v2/portfolios", json_data=portfolios)
        return response.json()

    async def edit(self, portfolios: List[Dict]) -> List[Portfolio]:
        """Edit portfolios.

        Args:
            portfolios: List of portfolio objects to update

        Returns:
            List of updated portfolio dictionaries
        """
        if not portfolios:
            raise ValueError("portfolios list cannot be empty")

        for portfolio in portfolios:
            if "portfolioId" not in portfolio:
                raise ValueError("Each portfolio must have portfolioId")

        response = await self._request("PUT", "/v2/portfolios", json_data=portfolios)
        return response.json()

    async def delete(self, portfolio_id: str) -> Dict:
        """Delete a portfolio.

        Args:
            portfolio_id: Portfolio identifier

        Returns:
            Deletion response dictionary
        """
        if not portfolio_id:
            raise ValueError("portfolio_id is required")

        response = await self._request("DELETE", f"/v2/portfolios/{portfolio_id}")
        return response.json()
