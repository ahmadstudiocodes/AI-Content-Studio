from __future__ import annotations

import time

from dataclasses import dataclass, field
from typing import Any, Dict, List

from runtime.observability import (
    runtime_observability,
)


@dataclass(slots=True)
class RuntimeEvent:

    name: str

    trace_id: str

    timestamp: float = field(
        default_factory=time.time
    )

    payload: Dict[str, Any] = field(
        default_factory=dict
    )


class RuntimeEventBus:
    """
    Runtime internal event collector.
    """

    def __init__(self):

        self.events: List[RuntimeEvent] = []

    def emit(
        self,
        event: RuntimeEvent,
    ) -> None:

        self.events.append(event)

        # Record event in observability dashboard
        runtime_observability.record_event()

    def all_events(
        self,
    ) -> List[RuntimeEvent]:

        return list(self.events)


runtime_event_bus = RuntimeEventBus()