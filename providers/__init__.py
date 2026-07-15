# providers/__init__.py
"""
Arman StudioOS
AI Providers Package

Unified access layer for all AI model providers.
"""

from .base import (
    BaseProvider,
    ProviderAdapter,
    ProviderFactory,
    ProviderHealth,
)

from .config import (
    ProviderConfigManager,
    provider_config_manager,
)

from .exceptions import (
    ProviderError,
    ProviderNotFoundError,
    ProviderInitializationError,
    ProviderConfigurationError,
    ProviderConnectionError,
    ProviderAuthenticationError,
    ProviderTimeoutError,
    ProviderRequestError,
    ProviderResponseError,
    ProviderRateLimitError,
    ProviderUnavailableError,
)

from .manager import (
    ProviderManager,
    provider_manager,
)

from .registry import (
    ProviderRegistry,
    provider_registry,
    register_provider,
)

from .types import (
    ProviderType,
    ProviderCapability,
    ProviderCapabilities,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
    ProviderInfo,
)


__all__ = [

    # Base
    "BaseProvider",
    "ProviderAdapter",
    "ProviderFactory",
    "ProviderHealth",

    # Config
    "ProviderConfigManager",
    "provider_config_manager",

    # Exceptions
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

    # Manager
    "ProviderManager",
    "provider_manager",

    # Registry
    "ProviderRegistry",
    "provider_registry",
    "register_provider",

    # Types
    "ProviderType",
    "ProviderCapability",
    "ProviderCapabilities",
    "ProviderConfig",
    "ProviderRequest",
    "ProviderResponse",
    "ProviderInfo",
]