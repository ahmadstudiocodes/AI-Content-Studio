# ============================================================
# File: studio/metrics_manager.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import json
import threading
import time
import uuid

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol


class SupportsWorkspace(Protocol):

    @property
    def root(self) -> Path: ...

    @property
    def workspace_id(self) -> str: ...


class SupportsEventBus(Protocol):

    def publish(
        self,
        event: str,
        **payload: Any,
    ) -> None: ...


class SupportsSharedState(Protocol):

    def set(
        self,
        key: str,
        value: Any,
    ) -> None: ...

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any: ...


class SupportsRuntime(Protocol):

    def is_running(
        self,
    ) -> bool: ...


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


class MetricType(str, Enum):

    COUNTER = "counter"

    GAUGE = "gauge"

    HISTOGRAM = "histogram"

    EVENT = "event"


@dataclass(slots=True)
class MetricMetadata:

    metric_id: str

    name: str

    metric_type: MetricType

    created_at: str

    updated_at: str

    description: str = ""

    unit: str = ""

    tags: dict[str, str] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class MetricRecord:

    metadata: MetricMetadata

    values: list[float] = field(
        default_factory=list
    )

    count: int = 0

    total: float = 0.0

    minimum: float | None = None

    maximum: float | None = None


class MetricsError(Exception):
    pass


class MetricNotFound(
    MetricsError
):
    pass


class MetricRegistry:

    """
    Enterprise Thread Safe Metrics Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._metrics: dict[
            str,
            MetricRecord,
        ] = {}

    def add(
        self,
        metric: MetricRecord,
    ) -> None:

        with self._lock:

            self._metrics[
                metric.metadata.name
            ] = metric

    def get(
        self,
        name: str,
    ) -> MetricRecord:

        with self._lock:

            try:

                return self._metrics[
                    name
                ]

            except KeyError as exc:

                raise MetricNotFound(
                    name
                ) from exc

    def all(
        self,
    ) -> list[MetricRecord]:

        with self._lock:

            return list(
                self._metrics.values()
            )

    def remove(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._metrics.pop(
                name
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._metrics.clear()


class MetricsManager:

    """
    StudioOS Enterprise Metrics Manager

    Features:

    - Runtime Metrics Collection
    - Performance Tracking
    - Event Integration
    - Statistics Engine
    - Plugin Hooks
    - Persistent Metrics

    Enterprise Upgrade Ready
    """

    METRICS_FILE = "metrics.json"

    def __init__(
        self,
        workspace: SupportsWorkspace,
        *,
        event_bus: SupportsEventBus | None = None,
        shared_state: SupportsSharedState | None = None,
        runtime: SupportsRuntime | None = None,
        plugins: SupportsPluginManager | None = None,
    ) -> None:

        self._workspace = workspace

        self._event_bus = event_bus

        self._shared_state = shared_state

        self._runtime = runtime

        self._plugins = plugins

        self._lock = threading.RLock()

        self._registry = MetricRegistry()

        self._root = (
            self._workspace.root /
            "metrics"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.METRICS_FILE
        )

        self._load()

# ============================================================
# File: studio/metrics_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _metric_id() -> str:

        return uuid.uuid4().hex

    def _emit(
        self,
        event: str,
        **payload: Any,
    ) -> None:

        if self._event_bus is not None:

            self._event_bus.publish(
                event,
                **payload,
            )

        if self._plugins is not None:

            self._plugins.emit(
                event,
                **payload,
            )

    def _load(
        self,
    ) -> None:

        if not self._file.exists():

            return

        try:

            payload = json.loads(
                self._file.read_text(
                    encoding="utf-8",
                )
            )

            for item in payload:

                metadata = item[
                    "metadata"
                ]

                metric = MetricRecord(
                    metadata=MetricMetadata(
                        metric_id=metadata[
                            "metric_id"
                        ],
                        name=metadata[
                            "name"
                        ],
                        metric_type=MetricType(
                            metadata[
                                "metric_type"
                            ]
                        ),
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        description=metadata.get(
                            "description",
                            "",
                        ),
                        unit=metadata.get(
                            "unit",
                            "",
                        ),
                        tags=dict(
                            metadata.get(
                                "tags",
                                {},
                            )
                        ),
                    ),
                    values=list(
                        item.get(
                            "values",
                            [],
                        )
                    ),
                    count=item.get(
                        "count",
                        0,
                    ),
                    total=item.get(
                        "total",
                        0.0,
                    ),
                    minimum=item.get(
                        "minimum"
                    ),
                    maximum=item.get(
                        "maximum"
                    ),
                )

                self._registry.add(
                    metric
                )

        except Exception:

            return

    def _save(
        self,
    ) -> None:

        payload = []

        for metric in (
            self._registry.all()
        ):

            metric.metadata.updated_at = (
                self._utc()
            )

            payload.append(
                {
                    "metadata":
                        asdict(
                            metric.metadata
                        ),
                    "values":
                        metric.values,
                    "count":
                        metric.count,
                    "total":
                        metric.total,
                    "minimum":
                        metric.minimum,
                    "maximum":
                        metric.maximum,
                }
            )

        self._file.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def register_metric(
        self,
        *,
        name: str,
        metric_type: MetricType,
        description: str = "",
        unit: str = "",
        tags: Mapping[
            str,
            str,
        ] | None = None,
    ) -> MetricRecord:

        with self._lock:

            metric = MetricRecord(
                metadata=MetricMetadata(
                    metric_id=self._metric_id(),
                    name=name,
                    metric_type=metric_type,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    description=description,
                    unit=unit,
                    tags=dict(
                        tags or {}
                    ),
                )
            )

            self._registry.add(
                metric
            )

            self._save()

            self._emit(
                "metric.registered",
                name=name,
            )

            return metric

    def record(
        self,
        name: str,
        value: float,
    ) -> MetricRecord:

        with self._lock:

            metric = self._registry.get(
                name
            )

            metric.values.append(
                value
            )

            metric.count += 1

            metric.total += value

            if (
                metric.minimum is None
                or
                value < metric.minimum
            ):

                metric.minimum = value

            if (
                metric.maximum is None
                or
                value > metric.maximum
            ):

                metric.maximum = value

            self._save()

            self._emit(
                "metric.recorded",
                name=name,
                value=value,
            )

            return metric
        
# ============================================================
# File: studio/metrics_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def increment(
        self,
        name: str,
        amount: float = 1.0,
    ) -> MetricRecord:

        return self.record(
            name,
            amount,
        )

    def set_value(
        self,
        name: str,
        value: float,
    ) -> MetricRecord:

        with self._lock:

            metric = self._registry.get(
                name
            )

            metric.values.append(
                value
            )

            metric.count += 1

            metric.total = value

            metric.minimum = value

            metric.maximum = value

            self._save()

            self._emit(
                "metric.value.set",
                name=name,
                value=value,
            )

            return metric

    def get_metric(
        self,
        name: str,
    ) -> MetricRecord:

        return self._registry.get(
            name
        )

    def list_metrics(
        self,
    ) -> list[MetricRecord]:

        return self._registry.all()

    def remove_metric(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                name
            )

            self._save()

            self._emit(
                "metric.removed",
                name=name,
            )

    def average(
        self,
        name: str,
    ) -> float:

        metric = self._registry.get(
            name
        )

        if metric.count == 0:

            return 0.0

        return (
            metric.total /
            metric.count
        )

    def percentile(
        self,
        name: str,
        percentage: float,
    ) -> float:

        metric = self._registry.get(
            name
        )

        if not metric.values:

            return 0.0

        values = sorted(
            metric.values
        )

        index = int(
            (
                percentage /
                100
            )
            *
            (
                len(values) - 1
            )
        )

        return values[index]

    def snapshot(
        self,
    ) -> dict[str, Any]:

        with self._lock:

            return {
                metric.metadata.name:
                    {
                        "count":
                            metric.count,
                        "total":
                            metric.total,
                        "minimum":
                            metric.minimum,
                        "maximum":
                            metric.maximum,
                        "average":
                            (
                                metric.total /
                                metric.count
                                if metric.count
                                else 0
                            ),
                    }
                for metric
                in self._registry.all()
            }

    def reset_metric(
        self,
        name: str,
    ) -> MetricRecord:

        with self._lock:

            metric = self._registry.get(
                name
            )

            metric.values.clear()

            metric.count = 0

            metric.total = 0.0

            metric.minimum = None

            metric.maximum = None

            self._save()

            self._emit(
                "metric.reset",
                name=name,
            )

            return metric
        
# ============================================================
# File: studio/metrics_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def export_metrics(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    self.snapshot(),
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_metrics(
        self,
        source: Path,
    ) -> int:

        with self._lock:

            if not source.exists():

                raise FileNotFoundError(
                    source
                )

            payload = json.loads(
                source.read_text(
                    encoding="utf-8",
                )
            )

            imported = 0

            for name, data in payload.items():

                metric = MetricRecord(
                    metadata=MetricMetadata(
                        metric_id=self._metric_id(),
                        name=name,
                        metric_type=MetricType.GAUGE,
                        created_at=self._utc(),
                        updated_at=self._utc(),
                        description=(
                            "Imported metric"
                        ),
                    ),
                    values=list(
                        data.get(
                            "values",
                            [],
                        )
                    ),
                    count=data.get(
                        "count",
                        0,
                    ),
                    total=data.get(
                        "total",
                        0.0,
                    ),
                    minimum=data.get(
                        "minimum"
                    ),
                    maximum=data.get(
                        "maximum"
                    ),
                )

                self._registry.add(
                    metric
                )

                imported += 1

            self._save()

            self._emit(
                "metrics.imported",
                count=imported,
            )

            return imported

    def collect_runtime_metrics(
        self,
    ) -> dict[str, Any]:

        runtime_status = (
            self._runtime.is_running()
            if self._runtime is not None
            else False
        )

        metrics = {
            "runtime_active":
                runtime_status,
            "workspace":
                self._workspace.workspace_id,
            "timestamp":
                self._utc(),
        }

        if self._shared_state is not None:

            self._shared_state.set(
                "studio.runtime_metrics",
                metrics,
            )

        self._emit(
            "runtime.metrics.collected",
            metrics=metrics,
        )

        return metrics

    def health_check(
        self,
    ) -> dict[str, Any]:

        errors: list[str] = []

        for metric in (
            self._registry.all()
        ):

            if metric.metadata.name == "":

                errors.append(
                    metric.metadata.metric_id
                )

        return {
            "healthy":
                not errors,
            "errors":
                errors,
            "metric_count":
                len(
                    self._registry.all()
                ),
            "timestamp":
                time.time(),
        }

    def statistics(
        self,
    ) -> dict[str, Any]:

        metrics = (
            self._registry.all()
        )

        total_records = sum(
            metric.count
            for metric
            in metrics
        )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "metric_count":
                len(metrics),
            "record_count":
                total_records,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "shared_state_connected":
                self._shared_state is not None,
            "plugin_manager_connected":
                self._plugins is not None,
        }
    
# ============================================================
# File: studio/metrics_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            snapshot = (
                self.snapshot()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.metrics_snapshot",
                    snapshot,
                )

            self._emit(
                "metrics_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def track_execution(
        self,
        name: str,
        callback: Callable[
            [],
            Any,
        ],
    ) -> Any:

        start = time.perf_counter()

        try:

            result = callback()

            duration = (
                time.perf_counter()
                - start
            )

            self.record(
                f"{name}.duration",
                duration,
            )

            self.increment(
                f"{name}.success",
            )

            return result

        except Exception:

            duration = (
                time.perf_counter()
                - start
            )

            self.record(
                f"{name}.duration",
                duration,
            )

            self.increment(
                f"{name}.failure",
            )

            raise

    def remove_all(
        self,
    ) -> None:

        with self._lock:

            self._registry.clear()

            self._save()

            self._emit(
                "metrics.cleared",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "metrics_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
