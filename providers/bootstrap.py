"""
Arman StudioOS
Provider Bootstrap

Startup initialization layer for providers.
"""

from __future__ import annotations

from typing import List

from .discovery import discover_providers
from .registry import provider_registry


class ProviderBootstrap:
    """
    Initializes provider subsystem.

    Responsibilities:
    - Discover providers
    - Prepare registry
    - Expose startup state
    """


    def __init__(self) -> None:

        self.initialized = False

        self.providers: List[str] = []



    def initialize(self) -> List[str]:
        """
        Initialize provider system.
        """

        if self.initialized:

            return self.providers


        self.providers = (
            discover_providers()
        )


        self.initialized = True


        return self.providers



    def status(self) -> dict:
        """
        Return bootstrap status.
        """

        return {
            "initialized": self.initialized,
            "providers": list(
                self.providers
            ),
            "registry_size": len(
                provider_registry.list()
            ),
        }



provider_bootstrap = ProviderBootstrap()



__all__ = [
    "ProviderBootstrap",
    "provider_bootstrap",
]