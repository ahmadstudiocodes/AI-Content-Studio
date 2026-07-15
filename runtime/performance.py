from __future__ import annotations

import time

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class PerformanceRecord:

    name: str

    duration: float


@dataclass(slots=True)
class RuntimePerformance:

    records: Dict[str, PerformanceRecord] = field(
        default_factory=dict,
    )

    def start(self) -> float:

        return time.perf_counter()

    def stop(
        self,
        name: str,
        started_at: float,
    ) -> float:

        duration = (
            time.perf_counter()
            - started_at
        )

        self.records[name] = PerformanceRecord(
            name=name,
            duration=duration,
        )

        return duration

    def get_duration(
        self,
        name: str,
    ) -> float:

        record = self.records.get(name)

        if record is None:
            return 0.0

        return record.duration

    def report(
        self,
    ) -> Dict[str, Any]:

        return {
            "total_records": len(self.records),
            "records": {
                name: record.duration
                for name, record in self.records.items()
            },
        }

    def clear(self) -> None:

        self.records.clear()


runtime_performance = RuntimePerformance()