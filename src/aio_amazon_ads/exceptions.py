"""Custom exceptions for Amazon Advertising API client."""


class AmazonAPIError(Exception):
    """Base exception for Amazon API errors."""

    pass


class AuthenticationError(AmazonAPIError):
    """Raised when authentication fails (401/403)."""

    pass


class ThrottlingError(AmazonAPIError):
    """Raised when API rate limit is exceeded (429)."""

    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after


class ValidationError(AmazonAPIError):
    """Raised when request validation fails (400)."""

    pass


class ServerError(AmazonAPIError):
    """Raised when server error occurs (5xx)."""

    pass
