"""
Arman StudioOS
Provider Runtime Adapter

Unified execution layer for providers.
"""

from __future__ import annotations

from typing import Dict, Any

from .manager import ProviderManager
from .retry import ProviderRetryEngine
from .failover import ProviderFailover
from .metrics import ProviderMetrics
from .events import (
    ProviderEvent,
    provider_event_bus,
)



class ProviderRuntime:
    """
    Unified provider execution runtime.
    """


    def __init__(
        self,
        manager: ProviderManager,
        retry: ProviderRetryEngine | None = None,
        failover: ProviderFailover | None = None,
        metrics: ProviderMetrics | None = None,
    ) -> None:

        self.manager = manager

        self.retry = (
            retry
            or ProviderRetryEngine()
        )

        self.failover = (
            failover
            or ProviderFailover()
        )

        self.metrics = (
            metrics
            or ProviderMetrics()
        )



    async def execute(
        self,
        provider_name: str,
        request,
    ):

        provider_event_bus.emit(
            ProviderEvent(
                name="provider.request.started",
                provider=provider_name,
            )
        )


        try:

            provider = (
                await self.manager.load(
                    provider_name
                )
            )


            result = await self.retry.execute(
                provider.generate,
                request,
            )


            self.metrics.record_success(
                provider_name,
                0.0,
            )


            provider_event_bus.emit(
                ProviderEvent(
                    name="provider.request.completed",
                    provider=provider_name,
                )
            )


            return result


        except Exception as exc:

            self.metrics.record_failure(
                provider_name,
            )


            self.failover.record_failure(
                provider_name
            )


            provider_event_bus.emit(
                ProviderEvent(
                    name="provider.request.failed",
                    provider=provider_name,
                    data={
                        "error": str(exc)
                    },
                )
            )


            raise



    async def health(
        self,
    ) -> Dict[str, Any]:

        return await self.manager.health()



__all__ = [
    "ProviderRuntime",
]