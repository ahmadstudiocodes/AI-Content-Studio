from __future__ import annotations

from dataclasses import dataclass

from runtime.observability import (
    runtime_observability,
)


@dataclass(slots=True)
class RuntimeMetrics:

    total_executions: int = 0

    successful_executions: int = 0

    failed_executions: int = 0

    total_duration: float = 0.0

    def record_success(
        self,
        duration: float,
    ) -> None:

        self.total_executions += 1

        self.successful_executions += 1

        self.total_duration += duration

        # Record metric in observability dashboard
        runtime_observability.record_metric()

    def record_failure(
        self,
        duration: float,
    ) -> None:

        self.total_executions += 1

        self.failed_executions += 1

        self.total_duration += duration

        # Record metric in observability dashboard
        runtime_observability.record_metric()

    @property
    def average_duration(
        self,
    ) -> float:

        if self.total_executions == 0:
            return 0.0

        return (
            self.total_duration
            / self.total_executions
        )


runtime_metrics = RuntimeMetrics()