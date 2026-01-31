"""aio-amazon-ads: Unofficial native async Python client for Amazon Advertising API."""

from .base import COUNTRY_TO_MARKETPLACE, Marketplace
from .client import AmazonAdsClient
from .exceptions import (
    AmazonAPIError,
    AuthenticationError,
    ServerError,
    ThrottlingError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "AmazonAdsClient",
    "Marketplace",
    "COUNTRY_TO_MARKETPLACE",
    "AmazonAPIError",
    "AuthenticationError",
    "ServerError",
    "ThrottlingError",
    "ValidationError",
]
