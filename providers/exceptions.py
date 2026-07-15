# providers/exceptions.py
"""
Arman StudioOS
Provider Exception Layer

Centralized exceptions for AI provider operations.
"""

from __future__ import annotations


class ProviderError(Exception):
    """
    Base provider exception.
    """

    def __init__(
        self,
        message: str,
        provider: str | None = None,
    ) -> None:

        self.provider = provider

        super().__init__(
            message
        )


class ProviderNotFoundError(
    ProviderError,
):
    """
    Raised when provider is not registered.
    """

    pass


class ProviderInitializationError(
    ProviderError,
):
    """
    Raised when provider initialization fails.
    """

    pass


class ProviderConfigurationError(
    ProviderError,
):
    """
    Raised when provider configuration is invalid.
    """

    pass


class ProviderConnectionError(
    ProviderError,
):
    """
    Raised when provider connection fails.
    """

    pass


class ProviderAuthenticationError(
    ProviderError,
):
    """
    Raised when authentication fails.
    """

    pass


class ProviderTimeoutError(
    ProviderError,
):
    """
    Raised when provider request times out.
    """

    pass


class ProviderRequestError(
    ProviderError,
):
    """
    Raised for invalid provider requests.
    """

    pass


class ProviderResponseError(
    ProviderError,
):
    """
    Raised when provider response is invalid.
    """

    pass


class ProviderRateLimitError(
    ProviderError,
):
    """
    Raised when provider rate limit is exceeded.
    """

    pass


class ProviderUnavailableError(
    ProviderError,
):
    """
    Raised when provider service is unavailable.
    """

    pass


__all__ = [
    "ProviderError",
    "ProviderNotFoundError",
    "ProviderInitializationError",
    "ProviderConfigurationError",
    "ProviderConnectionError",
    "ProviderAuthenticationError",
    "ProviderTimeoutError",
    "ProviderRequestError",
    "ProviderResponseError",
    "ProviderRateLimitError",
    "ProviderUnavailableError",
]