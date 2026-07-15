"""
Arman StudioOS
Provider Manager

Runtime management layer for AI providers.
"""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseProvider
from .config import provider_config_manager
from .exceptions import (
    ProviderInitializationError,
    ProviderNotFoundError,
)
from .registry import provider_registry
from .types import (
    ProviderRequest,
    ProviderResponse,
)

from .cache import provider_cache
from .middleware import provider_middleware
from .metrics import provider_metrics


class ProviderManager:
    """
    Main provider runtime controller.

    Responsibilities:
    - Load providers
    - Initialize providers
    - Execute requests
    - Manage provider lifecycle
    - Cache responses
    - Collect metrics
    - Run middleware pipeline
    """

    def __init__(
        self,
    ) -> None:

        self._instances: Dict[
            str,
            BaseProvider,
        ] = {}


    async def load(
        self,
        name: str,
    ) -> BaseProvider:
        """
        Create and initialize provider instance.
        """

        if name in self._instances:
            return self._instances[name]


        try:

            provider_class = (
                provider_registry.get(
                    name
                )
            )

            config = (
                provider_config_manager.get(
                    name
                )
            )

            provider = provider_class(
                config
            )

            await provider.initialize()

            self._instances[
                name
            ] = provider

            return provider


        except Exception as exc:

            raise ProviderInitializationError(
                str(exc),
                provider=name,
            ) from exc



    async def unload(
        self,
        name: str,
    ) -> None:

        provider = self._instances.pop(
            name,
            None,
        )

        if provider:
            await provider.shutdown()



    def get(
        self,
        name: str,
    ) -> BaseProvider:

        if name not in self._instances:

            raise ProviderNotFoundError(
                f"Provider not loaded: {name}",
                provider=name,
            )

        return self._instances[name]



    async def generate(
        self,
        provider_name: str,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """
        Execute AI generation request
        through runtime pipeline.
        """

        provider = await self.load(
            provider_name
        )


        request = await provider_middleware.process_before(
            request
        )


        cached = provider_cache.get(
            provider=provider_name,
            prompt=request.prompt,
            model=request.model,
        )


        if cached:

            return cached



        if not provider.validate_request(
            request
        ):

            raise ValueError(
                "Invalid provider request"
            )


        start_time = provider_metrics.start(
            provider_name
        )


        try:

            response = await provider.generate(
                request
            )


            provider_cache.set(
                provider=provider_name,
                prompt=request.prompt,
                model=request.model,
                value=response,
            )


            provider_metrics.success(
                provider_name,
                start_time,
            )


            response = await provider_middleware.process_after(
                request,
                response,
            )


            return response


        except Exception:

            provider_metrics.failure(
                provider_name,
                start_time,
            )

            raise



    async def health(
        self,
    ) -> Dict[str, Any]:

        result = {}

        for name, provider in (
            self._instances.items()
        ):

            result[name] = (
                await provider.health_check()
            )

        return result



    async def shutdown_all(
        self,
    ) -> None:

        for provider in list(
            self._instances.values()
        ):

            await provider.shutdown()

        self._instances.clear()



    def loaded(
        self,
    ) -> Dict[str, BaseProvider]:

        return dict(
            self._instances
        )



provider_manager = ProviderManager()


__all__ = [
    "ProviderManager",
    "provider_manager",
]