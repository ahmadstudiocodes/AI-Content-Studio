"""
Arman StudioOS
Provider Request Pipeline

Request processing layer between
Runtime and AI Providers.
"""

from __future__ import annotations

from typing import Any, Dict

from .runtime import ProviderRuntime
from .events import (
    ProviderEvent,
    provider_event_bus,
)



class ProviderPipeline:
    """
    Provider request processing pipeline.

    Responsibilities:
    - Validate requests
    - Execute through runtime
    - Track lifecycle events
    - Return responses
    """


    def __init__(
        self,
        runtime: ProviderRuntime,
    ) -> None:

        self.runtime = runtime



    def validate(
        self,
        request: Any,
    ) -> bool:
        """
        Basic request validation.
        """

        if request is None:
            return False

        return True



    async def execute(
        self,
        provider_name: str,
        request: Any,
    ) -> Any:
        """
        Execute provider request.
        """


        if not self.validate(
            request
        ):

            raise ValueError(
                "Invalid provider request"
            )



        provider_event_bus.emit(
            ProviderEvent(
                name="provider.pipeline.started",
                provider=provider_name,
            )
        )


        response = await self.runtime.execute(
            provider_name,
            request,
        )


        provider_event_bus.emit(
            ProviderEvent(
                name="provider.pipeline.completed",
                provider=provider_name,
            )
        )


        return response



    async def health(
        self,
    ) -> Dict[str, Any]:
        """
        Pipeline health.
        """

        return await self.runtime.health()



__all__ = [
    "ProviderPipeline",
]