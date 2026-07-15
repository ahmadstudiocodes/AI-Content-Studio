"""
Arman StudioOS
Provider Events

Event definitions for provider lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict


@dataclass
class ProviderEvent:
    """
    Base provider event.
    """

    name: str

    provider: str

    timestamp: datetime = field(
        default_factory=lambda:
        datetime.now(UTC)
    )

    data: Dict[str, Any] = field(
        default_factory=dict
    )


class ProviderEventBus:
    """
    Lightweight provider event dispatcher.
    """


    def __init__(self):

        self._events: list[
            ProviderEvent
        ] = []


    def emit(
        self,
        event: ProviderEvent,
    ) -> None:

        self._events.append(
            event
        )


    def history(
        self,
    ) -> list[ProviderEvent]:

        return list(
            self._events
        )


    def clear(
        self,
    ) -> None:

        self._events.clear()



provider_event_bus = ProviderEventBus()



__all__ = [
    "ProviderEvent",
    "ProviderEventBus",
    "provider_event_bus",
]
