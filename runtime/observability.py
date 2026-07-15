from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RuntimeObservability:

    """
    Runtime observability dashboard.
    """

    events: int = 0

    metrics: int = 0

    requests: int = 0

    errors: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def record_event(self) -> None:

        self.events += 1

    def record_metric(self) -> None:

        self.metrics += 1

    def record_request(self) -> None:

        self.requests += 1

    def record_error(self) -> None:

        self.errors += 1

    def snapshot(self) -> dict[str, Any]:

        return {
            "events": self.events,
            "metrics": self.metrics,
            "requests": self.requests,
            "errors": self.errors,
            "metadata": dict(self.metadata),
        }


runtime_observability = RuntimeObservability()