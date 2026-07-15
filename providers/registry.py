"""
Arman StudioOS
Provider Registry

Central registry for provider discovery and registration.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional, Type

from .base import BaseProvider
from .exceptions import ProviderNotFoundError
from .types import ProviderInfo


class ProviderRegistry:
    """
    Registry for AI providers.

    Uses explicit provider IDs.
    """


    def __init__(
        self,
    ) -> None:

        self._providers: Dict[
            str,
            Type[BaseProvider],
        ] = {}

        self._metadata: Dict[
            str,
            ProviderInfo,
        ] = {}


    def register(
        self,
        provider_class: Type[BaseProvider],
        provider_id: Optional[str] = None,
        info: Optional[ProviderInfo] = None,
    ) -> None:
        """
        Register provider class.

        Example:
            register(
                OllamaProvider,
                "ollama"
            )
        """


        if provider_id is None:

            provider_id = (
                provider_class.__name__
                .replace(
                    "Provider",
                    "",
                )
                .lower()
            )


        self._providers[
            provider_id
        ] = provider_class


        if info:

            self._metadata[
                provider_id
            ] = info



    def unregister(
        self,
        name: str,
    ) -> None:

        self._providers.pop(
            name,
            None,
        )

        self._metadata.pop(
            name,
            None,
        )



    def get(
        self,
        name: str,
    ) -> Type[BaseProvider]:

        if name not in self._providers:

            raise ProviderNotFoundError(
                f"Provider not registered: {name}",
                provider=name,
            )


        return self._providers[name]



    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._providers



    def list(
        self,
    ) -> Iterable[str]:

        return list(
            self._providers.keys()
        )



    def info(
        self,
        name: str,
    ) -> Optional[ProviderInfo]:

        return self._metadata.get(
            name
        )



    def all(
        self,
    ) -> Dict[str, Type[BaseProvider]]:

        return dict(
            self._providers
        )



    def clear(
        self,
    ) -> None:

        self._providers.clear()
        self._metadata.clear()



provider_registry = ProviderRegistry()



def register_provider(
    provider_class: Type[BaseProvider],
    provider_id: Optional[str] = None,
    info: Optional[ProviderInfo] = None,
):

    provider_registry.register(
        provider_class,
        provider_id,
        info,
    )

    return provider_class



__all__ = [
    "ProviderRegistry",
    "provider_registry",
    "register_provider",
]