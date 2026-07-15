# ============================================================
# File: studio/version_manager.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import json
import shutil
import threading
import time
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


class VersionStatus(str, Enum):

    CREATED = "created"

    ACTIVE = "active"

    RESTORED = "restored"

    ARCHIVED = "archived"

    FAILED = "failed"


@dataclass(slots=True)
class VersionMetadata:

    version_id: str

    name: str

    number: int

    created_at: str

    updated_at: str

    status: VersionStatus

    size: int

    description: str = ""

    parent_version: str | None = None

    tags: list[str] = field(
        default_factory=list
    )

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class VersionRecord:

    metadata: VersionMetadata

    path: Path

    metadata_file: Path


class VersionManagerError(Exception):
    pass


class VersionNotFound(
    VersionManagerError
):
    pass


class VersionRegistry:

    """
    Enterprise Thread Safe Version Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._versions: dict[
            str,
            VersionRecord,
        ] = {}

    def add(
        self,
        version: VersionRecord,
    ) -> None:

        with self._lock:

            self._versions[
                version.metadata.version_id
            ] = version

    def get(
        self,
        version_id: str,
    ) -> VersionRecord:

        with self._lock:

            try:

                return self._versions[
                    version_id
                ]

            except KeyError as exc:

                raise VersionNotFound(
                    version_id
                ) from exc

    def remove(
        self,
        version_id: str,
    ) -> None:

        with self._lock:

            self._versions.pop(
                version_id
            )

    def all(
        self,
    ) -> list[VersionRecord]:

        with self._lock:

            return list(
                self._versions.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._versions.clear()


class VersionManager:

    """
    StudioOS Enterprise Version Manager

    Features:

    - Snapshot Versioning
    - Restore System
    - History Tracking
    - Rollback Ready
    - Event Integration
    - Shared State Integration
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    VERSION_FILE = "version.json"

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

        self._registry = VersionRegistry()

        self._root = (
            self._workspace.root /
            "versions"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_versions()

# ============================================================
# File: studio/version_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _version_id() -> str:

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

    def _load_existing_versions(
        self,
    ) -> None:

        for metadata_file in self._root.rglob(
            self.VERSION_FILE
        ):

            try:

                data = json.loads(
                    metadata_file.read_text(
                        encoding="utf-8",
                    )
                )

                record = VersionRecord(
                    metadata=VersionMetadata(
                        version_id=data[
                            "version_id"
                        ],
                        name=data[
                            "name"
                        ],
                        number=data[
                            "number"
                        ],
                        created_at=data[
                            "created_at"
                        ],
                        updated_at=data[
                            "updated_at"
                        ],
                        status=VersionStatus(
                            data[
                                "status"
                            ]
                        ),
                        size=data.get(
                            "size",
                            0,
                        ),
                        description=data.get(
                            "description",
                            "",
                        ),
                        parent_version=data.get(
                            "parent_version"
                        ),
                        tags=list(
                            data.get(
                                "tags",
                                [],
                            )
                        ),
                        custom=dict(
                            data.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    path=metadata_file.parent,
                    metadata_file=metadata_file,
                )

                self._registry.add(
                    record
                )

            except Exception:

                continue

    def _save_metadata(
        self,
        version: VersionRecord,
    ) -> None:

        version.metadata.updated_at = (
            self._utc()
        )

        version.metadata_file.write_text(
            json.dumps(
                asdict(
                    version.metadata
                ),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def _next_number(
        self,
    ) -> int:

        versions = self._registry.all()

        if not versions:

            return 1

        return max(
            item.metadata.number
            for item in versions
        ) + 1

    def create_version(
        self,
        *,
        name: str,
        description: str = "",
        tags: list[str] | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> VersionRecord:

        with self._lock:

            version_id = (
                self._version_id()
            )

            number = (
                self._next_number()
            )

            destination = (
                self._root /
                version_id
            )

            shutil.copytree(
                self._workspace.root,
                destination,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "versions",
                    "backups",
                ),
            )

            size = sum(
                item.stat().st_size
                for item in destination.rglob("*")
                if item.is_file()
            )

            record = VersionRecord(
                metadata=VersionMetadata(
                    version_id=version_id,
                    name=name,
                    number=number,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=VersionStatus.CREATED,
                    size=size,
                    description=description,
                    tags=list(
                        tags or []
                    ),
                    custom=dict(
                        custom or {}
                    ),
                ),
                path=destination,
                metadata_file=(
                    destination /
                    self.VERSION_FILE
                ),
            )

            self._save_metadata(
                record
            )

            self._registry.add(
                record
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.latest_version",
                    version_id,
                )

            self._emit(
                "version.created",
                version_id=version_id,
                number=number,
            )

            return record
        
# ============================================================
# File: studio/version_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get_version(
        self,
        version_id: str,
    ) -> VersionRecord:

        return self._registry.get(
            version_id
        )

    def list_versions(
        self,
    ) -> list[VersionRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
                item.metadata.number,
        )

    def activate_version(
        self,
        version_id: str,
    ) -> VersionRecord:

        with self._lock:

            version = self._registry.get(
                version_id
            )

            for item in self._registry.all():

                if (
                    item.metadata.status
                    is VersionStatus.ACTIVE
                ):

                    item.metadata.status = (
                        VersionStatus.CREATED
                    )

                    self._save_metadata(
                        item
                    )

            version.metadata.status = (
                VersionStatus.ACTIVE
            )

            self._save_metadata(
                version
            )

            self._emit(
                "version.activated",
                version_id=version_id,
            )

            return version

    def restore_version(
        self,
        version_id: str,
        *,
        include_metadata: bool = False,
    ) -> Path:

        with self._lock:

            version = self._registry.get(
                version_id
            )

            if not version.path.exists():

                raise VersionManagerError(
                    "Version data unavailable"
                )

            source = version.path

            target = (
                self._workspace.root
            )

            for item in source.iterdir():

                if (
                    not include_metadata
                    and item.name
                    == self.VERSION_FILE
                ):

                    continue

                destination = (
                    target /
                    item.name
                )

                if item.is_dir():

                    shutil.copytree(
                        item,
                        destination,
                        dirs_exist_ok=True,
                    )

                else:

                    shutil.copy2(
                        item,
                        destination,
                    )

            version.metadata.status = (
                VersionStatus.RESTORED
            )

            self._save_metadata(
                version
            )

            self._emit(
                "version.restored",
                version_id=version_id,
            )

            return target

    def delete_version(
        self,
        version_id: str,
    ) -> None:

        with self._lock:

            version = self._registry.get(
                version_id
            )

            if version.path.exists():

                shutil.rmtree(
                    version.path
                )

            self._registry.remove(
                version_id
            )

            self._emit(
                "version.deleted",
                version_id=version_id,
            )

    def find_by_tag(
        self,
        tag: str,
    ) -> list[VersionRecord]:

        return [
            version
            for version
            in self._registry.all()
            if tag
            in version.metadata.tags
        ]

    def find_by_name(
        self,
        keyword: str,
    ) -> list[VersionRecord]:

        keyword = keyword.lower()

        return [
            version
            for version
            in self._registry.all()
            if keyword
            in version.metadata.name.lower()
        ]
    
# ============================================================
# File: studio/version_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def compare_versions(
        self,
        first_version: str,
        second_version: str,
    ) -> dict[str, Any]:

        with self._lock:

            first = self._registry.get(
                first_version
            )

            second = self._registry.get(
                second_version
            )

            first_files = {
                str(
                    item.relative_to(
                        first.path
                    )
                ): item.stat().st_size
                for item
                in first.path.rglob("*")
                if item.is_file()
                and item.name
                != self.VERSION_FILE
            }

            second_files = {
                str(
                    item.relative_to(
                        second.path
                    )
                ): item.stat().st_size
                for item
                in second.path.rglob("*")
                if item.is_file()
                and item.name
                != self.VERSION_FILE
            }

            added = [
                file
                for file in second_files
                if file not in first_files
            ]

            removed = [
                file
                for file in first_files
                if file not in second_files
            ]

            changed = [
                file
                for file in first_files
                if (
                    file in second_files
                    and first_files[file]
                    != second_files[file]
                )
            ]

            return {
                "first":
                    first_version,
                "second":
                    second_version,
                "added":
                    added,
                "removed":
                    removed,
                "changed":
                    changed,
            }

    def export_registry(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            data = [
                asdict(
                    version.metadata
                )
                for version
                in self._registry.all()
            ]

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_registry(
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

            for item in payload:

                version_path = (
                    self._root /
                    item["version_id"]
                )

                if not version_path.exists():

                    continue

                record = VersionRecord(
                    metadata=VersionMetadata(
                        version_id=item[
                            "version_id"
                        ],
                        name=item[
                            "name"
                        ],
                        number=item[
                            "number"
                        ],
                        created_at=item[
                            "created_at"
                        ],
                        updated_at=item[
                            "updated_at"
                        ],
                        status=VersionStatus(
                            item["status"]
                        ),
                        size=item.get(
                            "size",
                            0,
                        ),
                        description=item.get(
                            "description",
                            "",
                        ),
                        parent_version=item.get(
                            "parent_version"
                        ),
                        tags=list(
                            item.get(
                                "tags",
                                [],
                            )
                        ),
                        custom=dict(
                            item.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    path=version_path,
                    metadata_file=(
                        version_path /
                        self.VERSION_FILE
                    ),
                )

                self._registry.add(
                    record
                )

                imported += 1

            self._emit(
                "version.registry.imported",
                count=imported,
            )

            return imported
        
# ============================================================
# File: studio/version_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def statistics(
        self,
    ) -> dict[str, Any]:

        versions = self._registry.all()

        status_count: dict[str, int] = {}

        total_size = 0

        for version in versions:

            total_size += (
                version.metadata.size
            )

            key = (
                version.metadata.status.value
            )

            status_count[key] = (
                status_count.get(
                    key,
                    0,
                )
                + 1
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "version_count":
                len(versions),
            "total_size":
                total_size,
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

    def health_check(
        self,
    ) -> dict[str, Any]:

        invalid: list[str] = []

        for version in self._registry.all():

            if not version.path.exists():

                invalid.append(
                    version.metadata.version_id
                )

        return {
            "healthy":
                not invalid,
            "invalid_versions":
                invalid,
            "registered_versions":
                len(
                    self._registry.all()
                ),
            "timestamp":
                time.time(),
        }

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for version in self._registry.all():

                self._save_metadata(
                    version
                )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.version_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "version_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def archive_version(
        self,
        version_id: str,
    ) -> VersionRecord:

        with self._lock:

            version = self._registry.get(
                version_id
            )

            version.metadata.status = (
                VersionStatus.ARCHIVED
            )

            self._save_metadata(
                version
            )

            self._emit(
                "version.archived",
                version_id=version_id,
            )

            return version

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "version_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
