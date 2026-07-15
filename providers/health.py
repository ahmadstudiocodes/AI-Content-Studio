"""
Arman StudioOS
Provider Health Monitor

Central health aggregation for AI providers.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict


from .manager import ProviderManager



class ProviderHealthMonitor:
    """
    Central provider health monitoring.

    Responsibilities:
    - Check providers health
    - Aggregate status
    - Track health timestamp
    """


    def __init__(
        self,
        manager: ProviderManager,
    ) -> None:

        self.manager = manager

        self.last_check: datetime | None = None



    async def check_all(
        self,
    ) -> Dict[str, Any]:
        """
        Run health check on all loaded providers.
        """


        health = await (
            self.manager.health()
        )


        self.last_check = datetime.now(
            UTC
        )


        return {
            "timestamp": (
                self.last_check.isoformat()
            ),
            "providers": health,
            "total": len(
                health
            ),
            "available": sum(
                1
                for item in health.values()
                if item.get(
                    "available",
                    False,
                )
            ),
        }



    def status(
        self,
    ) -> Dict[str, Any]:
        """
        Return monitor status.
        """

        return {
            "last_check": (
                self.last_check.isoformat()
                if self.last_check
                else None
            )
        }



__all__ = [
    "ProviderHealthMonitor",
]