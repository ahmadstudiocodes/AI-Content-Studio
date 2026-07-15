# ============================================================
# File: studio/health_manager.py
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


class HealthStatus(str, Enum):

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"

    UNKNOWN = "unknown"


class CheckLevel(str, Enum):

    SYSTEM = "system"

    COMPONENT = "component"

    SERVICE = "service"


@dataclass(slots=True)
class HealthCheck:

    check_id: str

    name: str

    level: CheckLevel

    status: HealthStatus

    message: str

    created_at: str

    updated_at: str

    latency: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class HealthReport:

    report_id: str

    status: HealthStatus

    created_at: str

    checks: list[HealthCheck]

    summary: dict[str, Any] = field(
        default_factory=dict
    )


class HealthError(Exception):
    pass


class HealthRegistry:

    """
    Enterprise Thread Safe Health Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._checks: dict[
            str,
            HealthCheck,
        ] = {}

    def add(
        self,
        check: HealthCheck,
    ) -> None:

        with self._lock:

            self._checks[
                check.name
            ] = check

    def get(
        self,
        name: str,
    ) -> HealthCheck:

        with self._lock:

            return self._checks[
                name
            ]

    def all(
        self,
    ) -> list[HealthCheck]:

        with self._lock:

            return list(
                self._checks.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._checks.clear()


class HealthManager:

    """
    StudioOS Enterprise Health Manager

    Features:

    - System Health Monitoring
    - Component Diagnostics
    - Runtime Checks
    - Plugin Health Hooks
    - Event Integration
    - Persistent Reports

    Enterprise Upgrade Ready
    """

    HEALTH_FILE = "health.json"

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

        self._registry = HealthRegistry()

        self._root = (
            self._workspace.root /
            "health"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.HEALTH_FILE
        )

        self._load()

# ============================================================
# File: studio/health_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _id() -> str:

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

                check = HealthCheck(
                    check_id=item[
                        "check_id"
                    ],
                    name=item[
                        "name"
                    ],
                    level=CheckLevel(
                        item[
                            "level"
                        ]
                    ),
                    status=HealthStatus(
                        item[
                            "status"
                        ]
                    ),
                    message=item[
                        "message"
                    ],
                    created_at=item[
                        "created_at"
                    ],
                    updated_at=item[
                        "updated_at"
                    ],
                    latency=item.get(
                        "latency",
                        0.0,
                    ),
                    metadata=dict(
                        item.get(
                            "metadata",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    check
                )

        except Exception:

            return

    def _save(
        self,
    ) -> None:

        payload = [
            asdict(
                check
            )
            for check
            in self._registry.all()
        ]

        self._file.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def register_check(
        self,
        *,
        name: str,
        level: CheckLevel,
        message: str = "",
        metadata: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> HealthCheck:

        with self._lock:

            check = HealthCheck(
                check_id=self._id(),
                name=name,
                level=level,
                status=(
                    HealthStatus.UNKNOWN
                ),
                message=message,
                created_at=self._utc(),
                updated_at=self._utc(),
                metadata=dict(
                    metadata or {}
                ),
            )

            self._registry.add(
                check
            )

            self._save()

            self._emit(
                "health.check.registered",
                name=name,
            )

            return check

    def update_check(
        self,
        name: str,
        status: HealthStatus,
        *,
        message: str = "",
        latency: float = 0.0,
        metadata: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> HealthCheck:

        with self._lock:

            check = self._registry.get(
                name
            )

            check.status = status

            check.message = message

            check.latency = latency

            check.updated_at = (
                self._utc()
            )

            if metadata is not None:

                check.metadata.update(
                    metadata
                )

            self._save()

            self._emit(
                "health.check.updated",
                name=name,
                status=status.value,
            )

            return check
        
# ============================================================
# File: studio/health_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def run_check(
        self,
        name: str,
        checker: Callable[
            [],
            bool,
        ],
    ) -> HealthCheck:

        start = time.perf_counter()

        try:

            result = checker()

            latency = (
                time.perf_counter()
                - start
            )

            status = (
                HealthStatus.HEALTHY
                if result
                else HealthStatus.UNHEALTHY
            )

            return self.update_check(
                name,
                status,
                latency=latency,
                message=(
                    "Health check completed"
                    if result
                    else
                    "Health check failed"
                ),
            )

        except Exception as exc:

            latency = (
                time.perf_counter()
                - start
            )

            return self.update_check(
                name,
                HealthStatus.UNHEALTHY,
                latency=latency,
                message=str(exc),
            )

    def get_check(
        self,
        name: str,
    ) -> HealthCheck:

        return self._registry.get(
            name
        )

    def list_checks(
        self,
    ) -> list[HealthCheck]:

        return self._registry.all()

    def remove_check(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._registry._checks.pop(
                name,
                None,
            )

            self._save()

            self._emit(
                "health.check.removed",
                name=name,
            )

    def generate_report(
        self,
    ) -> HealthReport:

        with self._lock:

            checks = (
                self._registry.all()
            )

            if not checks:

                status = (
                    HealthStatus.UNKNOWN
                )

            elif any(
                check.status
                is HealthStatus.UNHEALTHY
                for check in checks
            ):

                status = (
                    HealthStatus.UNHEALTHY
                )

            elif any(
                check.status
                is HealthStatus.DEGRADED
                for check in checks
            ):

                status = (
                    HealthStatus.DEGRADED
                )

            else:

                status = (
                    HealthStatus.HEALTHY
                )

            report = HealthReport(
                report_id=self._id(),
                status=status,
                created_at=self._utc(),
                checks=list(
                    checks
                ),
                summary={
                    "total":
                        len(checks),
                    "healthy":
                        len(
                            [
                                check
                                for check
                                in checks
                                if check.status
                                is HealthStatus.HEALTHY
                            ]
                        ),
                    "unhealthy":
                        len(
                            [
                                check
                                for check
                                in checks
                                if check.status
                                is HealthStatus.UNHEALTHY
                            ]
                        ),
                },
            )

            self._emit(
                "health.report.generated",
                status=status.value,
            )

            return report

    def system_check(
        self,
    ) -> HealthReport:

        with self._lock:

            runtime_ok = (
                self._runtime.is_running()
                if self._runtime is not None
                else True
            )

            self.register_check(
                name="runtime",
                level=CheckLevel.SYSTEM,
            )

            self.update_check(
                "runtime",
                (
                    HealthStatus.HEALTHY
                    if runtime_ok
                    else HealthStatus.UNHEALTHY
                ),
                message=(
                    "Runtime active"
                    if runtime_ok
                    else
                    "Runtime unavailable"
                ),
            )

            return self.generate_report()
        
# ============================================================
# File: studio/health_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def export_report(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            report = self.generate_report()

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    {
                        "report_id":
                            report.report_id,
                        "status":
                            report.status.value,
                        "created_at":
                            report.created_at,
                        "summary":
                            report.summary,
                        "checks":
                            [
                                asdict(
                                    check
                                )
                                for check
                                in report.checks
                            ],
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_report(
        self,
        source: Path,
    ) -> HealthReport:

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

            checks: list[
                HealthCheck
            ] = []

            for item in payload.get(
                "checks",
                [],
            ):

                checks.append(
                    HealthCheck(
                        check_id=item[
                            "check_id"
                        ],
                        name=item[
                            "name"
                        ],
                        level=CheckLevel(
                            item[
                                "level"
                            ]
                        ),
                        status=HealthStatus(
                            item[
                                "status"
                            ]
                        ),
                        message=item[
                            "message"
                        ],
                        created_at=item[
                            "created_at"
                        ],
                        updated_at=item[
                            "updated_at"
                        ],
                        latency=item.get(
                            "latency",
                            0.0,
                        ),
                        metadata=dict(
                            item.get(
                                "metadata",
                                {},
                            )
                        ),
                    )
                )

            return HealthReport(
                report_id=payload[
                    "report_id"
                ],
                status=HealthStatus(
                    payload[
                        "status"
                    ]
                ),
                created_at=payload[
                    "created_at"
                ],
                checks=checks,
                summary=dict(
                    payload.get(
                        "summary",
                        {},
                    )
                ),
            )

    def component_health(
        self,
        component: str,
        details: Mapping[
            str,
            Any,
        ],
    ) -> HealthCheck:

        return self.update_check(
            component,
            HealthStatus.HEALTHY,
            message=(
                "Component operational"
            ),
            metadata=dict(
                details
            ),
        )

    def statistics(
        self,
    ) -> dict[str, Any]:

        checks = (
            self._registry.all()
        )

        status_count: dict[
            str,
            int,
        ] = {}

        for check in checks:

            status = (
                check.status.value
            )

            status_count[status] = (
                status_count.get(
                    status,
                    0,
                )
                + 1
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "check_count":
                len(checks),
            "statuses":
                status_count,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "shared_state_connected":
                self._shared_state is not None,
            "plugin_manager_connected":
                self._plugins is not None,
        }

    def health_summary(
        self,
    ) -> dict[str, Any]:

        report = (
            self.generate_report()
        )

        summary = {
            "status":
                report.status.value,
            "checks":
                report.summary,
            "timestamp":
                report.created_at,
        }

        if self._shared_state is not None:

            self._shared_state.set(
                "studio.health_summary",
                summary,
            )

        return summary
    
# ============================================================
# File: studio/health_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            report = (
                self.generate_report()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.health_report",
                    {
                        "status":
                            report.status.value,
                        "summary":
                            report.summary,
                    },
                )

            self._emit(
                "health_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def monitor(
        self,
        checks: Mapping[
            str,
            Callable[
                [],
                bool,
            ],
        ],
    ) -> HealthReport:

        with self._lock:

            for name, checker in checks.items():

                if name not in {
                    item.name
                    for item
                    in self._registry.all()
                }:

                    self.register_check(
                        name=name,
                        level=(
                            CheckLevel.COMPONENT
                        ),
                    )

                self.run_check(
                    name,
                    checker,
                )

            return self.generate_report()

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._registry.clear()

            self._save()

            self._emit(
                "health.cleared",
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
                "health_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
