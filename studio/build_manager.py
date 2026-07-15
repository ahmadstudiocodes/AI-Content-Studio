# ============================================================
# File: studio/build_manager.py
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


class BuildStatus(str, Enum):

    CREATED = "created"

    QUEUED = "queued"

    RUNNING = "running"

    SUCCESS = "success"

    FAILED = "failed"

    CANCELLED = "cancelled"


class BuildType(str, Enum):

    PROJECT = "project"

    SCENE = "scene"

    ASSET = "asset"

    PACKAGE = "package"

    CUSTOM = "custom"


@dataclass(slots=True)
class BuildMetadata:

    build_id: str

    name: str

    build_type: BuildType

    created_at: str

    updated_at: str

    status: BuildStatus

    version: int

    description: str = ""

    output_path: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    settings: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class BuildRecord:

    metadata: BuildMetadata

    logs: list[str] = field(
        default_factory=list
    )

    artifacts: list[str] = field(
        default_factory=list
    )


class BuildManagerError(Exception):
    pass


class BuildNotFound(
    BuildManagerError
):
    pass


class BuildRegistry:

    """
    Enterprise Thread Safe Build Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._builds: dict[
            str,
            BuildRecord,
        ] = {}

    def add(
        self,
        build: BuildRecord,
    ) -> None:

        with self._lock:

            self._builds[
                build.metadata.build_id
            ] = build

    def get(
        self,
        build_id: str,
    ) -> BuildRecord:

        with self._lock:

            try:

                return self._builds[
                    build_id
                ]

            except KeyError as exc:

                raise BuildNotFound(
                    build_id
                ) from exc

    def all(
        self,
    ) -> list[BuildRecord]:

        with self._lock:

            return list(
                self._builds.values()
            )

    def remove(
        self,
        build_id: str,
    ) -> None:

        with self._lock:

            self._builds.pop(
                build_id
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._builds.clear()


class BuildManager:

    """
    StudioOS Enterprise Build Manager

    Features:

    - Build Lifecycle
    - Build Queue Management
    - Artifact Tracking
    - Runtime Integration
    - Event Integration
    - Shared State Sync
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    BUILD_FILE = "builds.json"

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

        self._registry = BuildRegistry()

        self._root = (
            self._workspace.root /
            "builds"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.BUILD_FILE
        )

        self._load()

# ============================================================
# File: studio/build_manager.py
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

                build = BuildRecord(
                    metadata=BuildMetadata(
                        build_id=metadata[
                            "build_id"
                        ],
                        name=metadata[
                            "name"
                        ],
                        build_type=BuildType(
                            metadata[
                                "build_type"
                            ]
                        ),
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        status=BuildStatus(
                            metadata[
                                "status"
                            ]
                        ),
                        version=metadata.get(
                            "version",
                            1,
                        ),
                        description=metadata.get(
                            "description",
                            "",
                        ),
                        output_path=metadata.get(
                            "output_path",
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
                    artifacts=list(
                        item.get(
                            "artifacts",
                            [],
                        )
                    ),
                )

                self._registry.add(
                    build
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
                        build.metadata
                    ),
                "logs":
                    build.logs,
                "artifacts":
                    build.artifacts,
            }
            for build
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
        build_type: BuildType,
        description: str = "",
        output_path: str = "",
        tags: list[str] | None = None,
        settings: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> BuildRecord:

        with self._lock:

            build = BuildRecord(
                metadata=BuildMetadata(
                    build_id=self._id(),
                    name=name,
                    build_type=build_type,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=BuildStatus.CREATED,
                    version=1,
                    description=description,
                    output_path=output_path,
                    tags=list(
                        tags or []
                    ),
                    settings=dict(
                        settings or {}
                    ),
                )
            )

            self._registry.add(
                build
            )

            self._save()

            self._emit(
                "build.created",
                build_id=(
                    build.metadata.build_id
                ),
            )

            return build

    def get(
        self,
        build_id: str,
    ) -> BuildRecord:

        return self._registry.get(
            build_id
        )
    
# ============================================================
# File: studio/build_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def list_builds(
        self,
    ) -> list[BuildRecord]:

        return self._registry.all()

    def update(
        self,
        build_id: str,
        *,
        settings: Mapping[
            str,
            Any,
        ] | None = None,
        output_path: str | None = None,
        tags: list[str] | None = None,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            if settings is not None:

                build.metadata.settings.update(
                    settings
                )

            if output_path is not None:

                build.metadata.output_path = (
                    output_path
                )

            if tags is not None:

                build.metadata.tags = (
                    list(tags)
                )

            build.metadata.version += 1

            build.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "build.updated",
                build_id=build_id,
                version=(
                    build.metadata.version
                ),
            )

            return build

    def queue(
        self,
        build_id: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            build.metadata.status = (
                BuildStatus.QUEUED
            )

            build.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "build.queued",
                build_id=build_id,
            )

            return build

    def start(
        self,
        build_id: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            build.metadata.status = (
                BuildStatus.RUNNING
            )

            build.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                build_id,
                "Build started",
            )

            self._save()

            self._emit(
                "build.started",
                build_id=build_id,
            )

            return build

    def complete(
        self,
        build_id: str,
        *,
        artifacts: list[str] | None = None,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            build.metadata.status = (
                BuildStatus.SUCCESS
            )

            if artifacts is not None:

                build.artifacts.extend(
                    artifacts
                )

            build.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                build_id,
                "Build completed successfully",
            )

            self._save()

            self._emit(
                "build.completed",
                build_id=build_id,
            )

            return build

    def fail(
        self,
        build_id: str,
        reason: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            build.metadata.status = (
                BuildStatus.FAILED
            )

            build.metadata.updated_at = (
                self._utc()
            )

            self.add_log(
                build_id,
                reason,
            )

            self._save()

            self._emit(
                "build.failed",
                build_id=build_id,
                reason=reason,
            )

            return build

    def cancel(
        self,
        build_id: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            build.metadata.status = (
                BuildStatus.CANCELLED
            )

            build.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "build.cancelled",
                build_id=build_id,
            )

            return build
        
# ============================================================
# File: studio/build_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def add_log(
        self,
        build_id: str,
        message: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            timestamp = self._utc()

            build.logs.append(
                f"{timestamp} | {message}"
            )

            build.metadata.updated_at = (
                self._utc()
            )

            self._save()

            return build

    def add_artifact(
        self,
        build_id: str,
        artifact: str,
    ) -> BuildRecord:

        with self._lock:

            build = self._registry.get(
                build_id
            )

            if artifact not in build.artifacts:

                build.artifacts.append(
                    artifact
                )

            build.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "build.artifact.added",
                build_id=build_id,
                artifact=artifact,
            )

            return build

    def remove(
        self,
        build_id: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                build_id
            )

            self._save()

            self._emit(
                "build.deleted",
                build_id=build_id,
            )

    def find_by_type(
        self,
        build_type: BuildType,
    ) -> list[BuildRecord]:

        return [
            build
            for build
            in self._registry.all()
            if (
                build.metadata.build_type
                is build_type
            )
        ]

    def find_by_status(
        self,
        status: BuildStatus,
    ) -> list[BuildRecord]:

        return [
            build
            for build
            in self._registry.all()
            if (
                build.metadata.status
                is status
            )
        ]

    def export_build(
        self,
        build_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            build = self._registry.get(
                build_id
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
                                build.metadata
                            ),
                        "logs":
                            build.logs,
                        "artifacts":
                            build.artifacts,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_build(
        self,
        source: Path,
    ) -> BuildRecord:

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

            build = BuildRecord(
                metadata=BuildMetadata(
                    build_id=self._id(),
                    name=metadata[
                        "name"
                    ],
                    build_type=BuildType(
                        metadata[
                            "build_type"
                        ]
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=BuildStatus.CREATED,
                    version=1,
                    description=metadata.get(
                        "description",
                        "",
                    ),
                    output_path=metadata.get(
                        "output_path",
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
                artifacts=list(
                    payload.get(
                        "artifacts",
                        [],
                    )
                ),
            )

            self._registry.add(
                build
            )

            self._save()

            self._emit(
                "build.imported",
                build_id=(
                    build.metadata.build_id
                ),
            )

            return build
        
# ============================================================
# File: studio/build_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            builds = (
                self._registry.all()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.build_count",
                    len(builds),
                )

            self._emit(
                "build_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        builds = (
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

        artifacts = 0

        for build in builds:

            status = (
                build.metadata.status.value
            )

            build_type = (
                build.metadata.build_type.value
            )

            statuses[status] = (
                statuses.get(
                    status,
                    0,
                )
                + 1
            )

            types[build_type] = (
                types.get(
                    build_type,
                    0,
                )
                + 1
            )

            artifacts += (
                len(
                    build.artifacts
                )
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "build_count":
                len(builds),
            "artifact_count":
                artifacts,
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

        for build in (
            self._registry.all()
        ):

            if not build.metadata.name:

                invalid.append(
                    build.metadata.build_id
                )

        return {
            "healthy":
                not invalid,
            "invalid_builds":
                invalid,
            "registered_builds":
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
                "build.registry.cleared",
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
                "build_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
