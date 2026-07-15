# providers/base.py
"""
Arman StudioOS
Provider Base Layer

Defines the contract that every AI provider must implement.
(OpenAI, Ollama, Gemini, Claude, etc.)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional, Protocol

from .types import (
    ProviderCapabilities,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
)


class ProviderHealth(Protocol):
    """
    Provider health check contract.
    """

    def is_available(self) -> bool:
        ...


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.

    Every provider adapter must implement this interface.
    """

    def __init__(
        self,
        config: ProviderConfig,
    ) -> None:

        self.config = config
        self._initialized = False


    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider unique name.

        Example:
            ollama
            openai
        """
        raise NotImplementedError


    @property
    @abstractmethod
    def capabilities(
        self,
    ) -> ProviderCapabilities:
        """
        Supported provider capabilities.
        """
        raise NotImplementedError


    async def initialize(
        self,
    ) -> None:
        """
        Initialize provider resources.
        """

        self._initialized = True


    async def shutdown(
        self,
    ) -> None:
        """
        Release provider resources.
        """

        self._initialized = False


    @property
    def initialized(
        self,
    ) -> bool:
        """
        Provider initialization state.
        """

        return self._initialized


    @abstractmethod
    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """
        Generate AI response.

        Must be implemented by every provider.
        """

        raise NotImplementedError


    async def stream(
        self,
        request: ProviderRequest,
    ) -> AsyncIterator[str]:
        """
        Streaming generation.

        Providers can override this.
        """

        response = await self.generate(request)

        yield response.content


    async def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Provider health information.
        """

        return {
            "provider": self.name,
            "initialized": self.initialized,
            "available": True,
        }


    def validate_request(
        self,
        request: ProviderRequest,
    ) -> bool:
        """
        Validate incoming request.

        Base validation.
        """

        if request is None:
            return False

        return True


    def metadata(
        self,
    ) -> Dict[str, Any]:
        """
        Provider metadata.
        """

        return {
            "name": self.name,
            "capabilities": self.capabilities.to_dict(),
            "initialized": self.initialized,
        }


class ProviderFactory(Protocol):
    """
    Provider factory contract.
    """

    def create(
        self,
        config: ProviderConfig,
    ) -> BaseProvider:
        ...


class ProviderAdapter(Protocol):
    """
    External provider adapter contract.
    """

    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        ...


__all__ = [
    "BaseProvider",
    "ProviderFactory",
    "ProviderAdapter",
    "ProviderHealth",
]