"""Portfolios service."""

import builtins
from collections.abc import AsyncGenerator
from typing import Any

from ...base import BaseService

Portfolio = dict[str, Any]


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
        from ...validation import validate_portfolio_id

        validate_portfolio_id(portfolio_id)

        response = await self._request("GET", f"/v2/portfolios/{portfolio_id}")
        return response.json()

    async def create(self, portfolios: builtins.list[dict]) -> builtins.list[Portfolio]:
        """Create portfolios.

        Args:
            portfolios: List of portfolio objects to create

        Returns:
            List of created portfolio dictionaries
        """
        from ...validation import validate_portfolios_for_create

        validate_portfolios_for_create(portfolios)

        response = await self._request("POST", "/v2/portfolios", json_data=portfolios)
        return response.json()

    async def edit(self, portfolios: builtins.list[dict]) -> builtins.list[Portfolio]:
        """Edit portfolios.

        Args:
            portfolios: List of portfolio objects to update

        Returns:
            List of updated portfolio dictionaries
        """
        from ...validation import validate_portfolios_for_update

        validate_portfolios_for_update(portfolios)

        response = await self._request("PUT", "/v2/portfolios", json_data=portfolios)
        return response.json()

    async def delete(self, portfolio_id: str) -> dict:
        """Delete a portfolio.

        Args:
            portfolio_id: Portfolio identifier

        Returns:
            Deletion response dictionary
        """
        from ...validation import validate_portfolio_id

        validate_portfolio_id(portfolio_id)

        response = await self._request("DELETE", f"/v2/portfolios/{portfolio_id}")
        return response.json()
