# ============================================================
# File: studio/export_manager.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import json
import threading
import uuid

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Protocol


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


class ExportStatus(str, Enum):

    CREATED = "created"

    QUEUED = "queued"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class ExportType(str, Enum):

    SCENE = "scene"

    PROJECT = "project"

    ASSET = "asset"

    PACKAGE = "package"

    ARCHIVE = "archive"

    CUSTOM = "custom"


@dataclass(slots=True)
class ExportMetadata:

    export_id: str

    name: str

    export_type: ExportType

    created_at: str

    updated_at: str

    status: ExportStatus

    version: int

    source: str = ""

    destination: str = ""

    format: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    settings: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class ExportRecord:

    metadata: ExportMetadata

    logs: list[str] = field(
        default_factory=list
    )

    files: list[str] = field(
        default_factory=list
    )


class ExportManagerError(Exception):
    pass


class ExportNotFound(
    ExportManagerError
):
    pass


class ExportRegistry:

    """
    Enterprise Thread Safe Export Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._exports: dict[
            str,
            ExportRecord,
        ] = {}

    def add(
        self,
        export: ExportRecord,
    ) -> None:

        with self._lock:

            self._exports[
                export.metadata.export_id
            ] = export

    def get(
        self,
        export_id: str,
    ) -> ExportRecord:

        with self._lock:

            try:

                return self._exports[
                    export_id
                ]

            except KeyError as exc:

                raise ExportNotFound(
                    export_id
                ) from exc

    def all(
        self,
    ) -> list[ExportRecord]:

        with self._lock:

            return list(
                self._exports.values()
            )

    def remove(
        self,
        export_id: str,
    ) -> None:

        with self._lock:

            self._exports.pop(
                export_id
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._exports.clear()


class ExportManager:

    """
    StudioOS Enterprise Export Manager

    Features:

    - Export Lifecycle
    - Package Management
    - Artifact Tracking
    - Runtime Integration
    - Event Integration
    - Shared State Sync
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    EXPORT_FILE = "exports.json"

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

        self._registry = ExportRegistry()

        self._root = (
            self._workspace.root /
            "exports"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.EXPORT_FILE
        )

        self._load()

# ============================================================
# File: studio/export_manager.py
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

                metadata = item[
                    "metadata"
                ]

                export = ExportRecord(
                    metadata=ExportMetadata(
                        export_id=metadata[
                            "export_id"
                        ],
                        name=metadata[
                            "name"
                        ],
                        export_type=ExportType(
                            metadata[
                                "export_type"
                            ]
                        ),
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        status=ExportStatus(
                            metadata[
                                "status"
                            ]
                        ),
                        version=metadata.get(
                            "version",
                            1,
                        ),
                        source=metadata.get(
                            "source",
                            "",
                        ),
                        destination=metadata.get(
                            "destination",
                            "",
                        ),
                        format=metadata.get(
                            "format",
                            "",
                        ),
                        tags=list(
                            metadata.get(
                                "tags",
                                [],
                            )
                        ),
                        settings=dict(
                            metadata.get(
                                "settings",
                                {},
                            )
                        ),
                    ),
                    logs=list(
                        item.get(
                            "logs",
                            [],
                        )
                    ),
                    files=list(
                        item.get(
                            "files",
                            [],
                        )
                    ),
                )

                self._registry.add(
                    export
                )

        except Exception:

            return

    def _save(
        self,
    ) -> None:

        payload = [
            {
                "metadata":
                    asdict(
                        export.metadata
                    ),
                "logs":
                    export.logs,
                "files":
                    export.files,
            }
            for export
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

    def create(
        self,
        *,
        name: str,
        export_type: ExportType,
        source: str = "",
        destination: str = "",
        format: str = "",
        tags: list[str] | None = None,
        settings: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> ExportRecord:

        with self._lock:

            export = ExportRecord(
                metadata=ExportMetadata(
                    export_id=self._id(),
                    name=name,
                    export_type=export_type,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=ExportStatus.CREATED,
                    version=1,
                    source=source,
                    destination=destination,
                    format=format,
                    tags=list(
                        tags or []
                    ),
                    settings=dict(
                        settings or {}
                    ),
                )
            )

            self._registry.add(
                export
            )

            self._save()

            self._emit(
                "export.created",
                export_id=(
                    export.metadata.export_id
                ),
            )

            return export

    def get(
        self,
        export_id: str,
    ) -> ExportRecord:

        return self._registry.get(
            export_id
        )
    
# ============================================================
# File: studio/export_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def list_exports(
        self,
    ) -> list[ExportRecord]:

        return self._registry.all()

    def update(
        self,
        export_id: str,
        *,
        destination: str | None = None,
        settings: Mapping[
            str,
            Any,
        ] | None = None,
        tags: list[str] | None = None,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            if destination is not None:

                export.metadata.destination = (
                    destination
                )

            if settings is not None:

                export.metadata.settings.update(
                    settings
                )

            if tags is not None:

                export.metadata.tags = (
                    list(tags)
                )

            export.metadata.version += 1

            export.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "export.updated",
                export_id=export_id,
                version=(
                    export.metadata.version
                ),
            )

            return export

    def queue(
        self,
        export_id: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            export.metadata.status = (
                ExportStatus.QUEUED
            )

            export.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "export.queued",
                export_id=export_id,
            )

            return export

    def start(
        self,
        export_id: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            export.metadata.status = (
                ExportStatus.RUNNING
            )

            export.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                export_id,
                "Export started",
            )

            self._save()

            self._emit(
                "export.started",
                export_id=export_id,
            )

            return export

    def complete(
        self,
        export_id: str,
        *,
        files: list[str] | None = None,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            export.metadata.status = (
                ExportStatus.COMPLETED
            )

            if files is not None:

                for file in files:

                    if file not in export.files:

                        export.files.append(
                            file
                        )

            export.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                export_id,
                "Export completed successfully",
            )

            self._save()

            self._emit(
                "export.completed",
                export_id=export_id,
            )

            return export

    def fail(
        self,
        export_id: str,
        reason: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            export.metadata.status = (
                ExportStatus.FAILED
            )

            export.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                export_id,
                reason,
            )

            self._save()

            self._emit(
                "export.failed",
                export_id=export_id,
                reason=reason,
            )

            return export

    def cancel(
        self,
        export_id: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            export.metadata.status = (
                ExportStatus.CANCELLED
            )

            export.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "export.cancelled",
                export_id=export_id,
            )

            return export
        
# ============================================================
# File: studio/export_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def add_log(
        self,
        export_id: str,
        message: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            timestamp = self._utc()

            export.logs.append(
                f"{timestamp} | {message}"
            )

            export.metadata.updated_at = (
                self._utc()
            )

            self._save()

            return export

    def add_file(
        self,
        export_id: str,
        file_path: str,
    ) -> ExportRecord:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            if file_path not in export.files:

                export.files.append(
                    file_path
                )

            export.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "export.file.added",
                export_id=export_id,
                file=file_path,
            )

            return export

    def remove(
        self,
        export_id: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                export_id
            )

            self._save()

            self._emit(
                "export.deleted",
                export_id=export_id,
            )

    def find_by_type(
        self,
        export_type: ExportType,
    ) -> list[ExportRecord]:

        return [
            export
            for export
            in self._registry.all()
            if (
                export.metadata.export_type
                is export_type
            )
        ]

    def find_by_status(
        self,
        status: ExportStatus,
    ) -> list[ExportRecord]:

        return [
            export
            for export
            in self._registry.all()
            if (
                export.metadata.status
                is status
            )
        ]

    def export_record(
        self,
        export_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            export = self._registry.get(
                export_id
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    {
                        "metadata":
                            asdict(
                                export.metadata
                            ),
                        "logs":
                            export.logs,
                        "files":
                            export.files,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_record(
        self,
        source: Path,
    ) -> ExportRecord:

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

            metadata = payload[
                "metadata"
            ]

            export = ExportRecord(
                metadata=ExportMetadata(
                    export_id=self._id(),
                    name=metadata[
                        "name"
                    ],
                    export_type=ExportType(
                        metadata[
                            "export_type"
                        ]
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=ExportStatus.CREATED,
                    version=1,
                    source=metadata.get(
                        "source",
                        "",
                    ),
                    destination=metadata.get(
                        "destination",
                        "",
                    ),
                    format=metadata.get(
                        "format",
                        "",
                    ),
                    tags=list(
                        metadata.get(
                            "tags",
                            [],
                        )
                    ),
                    settings=dict(
                        metadata.get(
                            "settings",
                            {},
                        )
                    ),
                ),
                logs=list(
                    payload.get(
                        "logs",
                        [],
                    )
                ),
                files=list(
                    payload.get(
                        "files",
                        [],
                    )
                ),
            )

            self._registry.add(
                export
            )

            self._save()

            self._emit(
                "export.imported",
                export_id=(
                    export.metadata.export_id
                ),
            )

            return export
        
        # ============================================================
# File: studio/export_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            exports = (
                self._registry.all()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.export_count",
                    len(exports),
                )

            self._emit(
                "export_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        exports = (
            self._registry.all()
        )

        statuses: dict[
            str,
            int,
        ] = {}

        types: dict[
            str,
            int,
        ] = {}

        file_count = 0

        for export in exports:

            status = (
                export.metadata.status.value
            )

            export_type = (
                export.metadata.export_type.value
            )

            statuses[status] = (
                statuses.get(
                    status,
                    0,
                )
                + 1
            )

            types[export_type] = (
                types.get(
                    export_type,
                    0,
                )
                + 1
            )

            file_count += (
                len(
                    export.files
                )
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "export_count":
                len(exports),
            "file_count":
                file_count,
            "statuses":
                statuses,
            "types":
                types,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "shared_state_connected":
                self._shared_state is not None,
            "plugin_manager_connected":
                self._plugins is not None,
        }

    def health_check(
        self,
    ) -> dict[str, Any]:

        invalid = []

        for export in (
            self._registry.all()
        ):

            if not export.metadata.name:

                invalid.append(
                    export.metadata.export_id
                )

        return {
            "healthy":
                not invalid,
            "invalid_exports":
                invalid,
            "registered_exports":
                len(
                    self._registry.all()
                ),
        }

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._registry.clear()

            self._save()

            self._emit(
                "export.registry.cleared",
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
                "export_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
