# ============================================================
# File: studio/resource_manager.py
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


class ResourceType(str, Enum):

    FILE = "file"

    DIRECTORY = "directory"

    MODEL = "model"

    TEXTURE = "texture"

    AUDIO = "audio"

    VIDEO = "video"

    DATA = "data"

    OTHER = "other"


class ResourceStatus(str, Enum):

    AVAILABLE = "available"

    MISSING = "missing"

    LOCKED = "locked"

    ARCHIVED = "archived"


@dataclass(slots=True)
class ResourceMetadata:

    resource_id: str

    name: str

    resource_type: ResourceType

    path: str

    created_at: str

    updated_at: str

    size: int

    status: ResourceStatus

    tags: list[str] = field(
        default_factory=list
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class ResourceRecord:

    metadata: ResourceMetadata


class ResourceManagerError(Exception):
    pass


class ResourceNotFound(
    ResourceManagerError
):
    pass


class ResourceRegistry:

    """
    Enterprise Thread Safe Resource Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._resources: dict[
            str,
            ResourceRecord,
        ] = {}

    def add(
        self,
        resource: ResourceRecord,
    ) -> None:

        with self._lock:

            self._resources[
                resource.metadata.resource_id
            ] = resource

    def get(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        with self._lock:

            try:

                return self._resources[
                    resource_id
                ]

            except KeyError as exc:

                raise ResourceNotFound(
                    resource_id
                ) from exc

    def all(
        self,
    ) -> list[ResourceRecord]:

        with self._lock:

            return list(
                self._resources.values()
            )

    def remove(
        self,
        resource_id: str,
    ) -> None:

        with self._lock:

            self._resources.pop(
                resource_id
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._resources.clear()


class ResourceManager:

    """
    StudioOS Enterprise Resource Manager

    Features:

    - Resource Registration
    - File Tracking
    - Metadata Management
    - Resource Discovery
    - Event Integration
    - Shared State Integration
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    RESOURCE_FILE = "resources.json"

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

        self._registry = ResourceRegistry()

        self._root = (
            self._workspace.root /
            "resources"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.RESOURCE_FILE
        )

        self._load()

# ============================================================
# File: studio/resource_manager.py
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

                metadata = ResourceMetadata(
                    resource_id=item[
                        "resource_id"
                    ],
                    name=item[
                        "name"
                    ],
                    resource_type=ResourceType(
                        item[
                            "resource_type"
                        ]
                    ),
                    path=item[
                        "path"
                    ],
                    created_at=item[
                        "created_at"
                    ],
                    updated_at=item[
                        "updated_at"
                    ],
                    size=item.get(
                        "size",
                        0,
                    ),
                    status=ResourceStatus(
                        item[
                            "status"
                        ]
                    ),
                    tags=list(
                        item.get(
                            "tags",
                            [],
                        )
                    ),
                    properties=dict(
                        item.get(
                            "properties",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    ResourceRecord(
                        metadata=metadata
                    )
                )

        except Exception:

            return

    def _save(
        self,
    ) -> None:

        payload = [
            asdict(
                resource.metadata
            )
            for resource
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

    def register(
        self,
        *,
        name: str,
        resource_type: ResourceType,
        path: Path,
        tags: list[str] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> ResourceRecord:

        with self._lock:

            record = ResourceRecord(
                metadata=ResourceMetadata(
                    resource_id=self._id(),
                    name=name,
                    resource_type=resource_type,
                    path=str(
                        path
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    size=(
                        path.stat().st_size
                        if path.exists()
                        and path.is_file()
                        else 0
                    ),
                    status=(
                        ResourceStatus.AVAILABLE
                    ),
                    tags=list(
                        tags or []
                    ),
                    properties=dict(
                        properties or {}
                    ),
                )
            )

            self._registry.add(
                record
            )

            self._save()

            self._emit(
                "resource.registered",
                resource_id=(
                    record.metadata.resource_id
                ),
            )

            return record

    def update(
        self,
        resource_id: str,
        *,
        tags: list[str] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            if tags is not None:

                resource.metadata.tags = (
                    list(tags)
                )

            if properties is not None:

                resource.metadata.properties.update(
                    properties
                )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "resource.updated",
                resource_id=resource_id,
            )

            return resource
        
# ============================================================
# File: studio/resource_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        return self._registry.get(
            resource_id
        )

    def list_resources(
        self,
    ) -> list[ResourceRecord]:

        return self._registry.all()

    def remove(
        self,
        resource_id: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                resource_id
            )

            self._save()

            self._emit(
                "resource.removed",
                resource_id=resource_id,
            )

    def exists(
        self,
        resource_id: str,
    ) -> bool:

        try:

            self._registry.get(
                resource_id
            )

            return True

        except ResourceNotFound:

            return False

    def find_by_type(
        self,
        resource_type: ResourceType,
    ) -> list[ResourceRecord]:

        return [
            resource
            for resource
            in self._registry.all()
            if (
                resource.metadata.resource_type
                is resource_type
            )
        ]

    def find_by_tag(
        self,
        tag: str,
    ) -> list[ResourceRecord]:

        return [
            resource
            for resource
            in self._registry.all()
            if tag
            in resource.metadata.tags
        ]

    def scan_workspace(
        self,
    ) -> int:

        with self._lock:

            discovered = 0

            for item in (
                self._workspace.root.rglob("*")
            ):

                if (
                    not item.is_file()
                    or
                    str(item).startswith(
                        str(self._root)
                    )
                ):

                    continue

                resource = ResourceRecord(
                    metadata=ResourceMetadata(
                        resource_id=self._id(),
                        name=item.name,
                        resource_type=(
                            self._detect_type(
                                item
                            )
                        ),
                        path=str(item),
                        created_at=self._utc(),
                        updated_at=self._utc(),
                        size=item.stat().st_size,
                        status=(
                            ResourceStatus.AVAILABLE
                        ),
                    )
                )

                self._registry.add(
                    resource
                )

                discovered += 1

            self._save()

            self._emit(
                "resource.scan.completed",
                count=discovered,
            )

            return discovered

    def _detect_type(
        self,
        path: Path,
    ) -> ResourceType:

        extension = (
            path.suffix.lower()
        )

        if extension in {
            ".png",
            ".jpg",
            ".jpeg",
            ".exr",
            ".tga",
        }:

            return ResourceType.TEXTURE

        if extension in {
            ".obj",
            ".fbx",
            ".max",
            ".blend",
        }:

            return ResourceType.MODEL

        if extension in {
            ".mp3",
            ".wav",
            ".flac",
        }:

            return ResourceType.AUDIO

        if extension in {
            ".mp4",
            ".mov",
            ".avi",
        }:

            return ResourceType.VIDEO

        if extension in {
            ".json",
            ".csv",
            ".xml",
        }:

            return ResourceType.DATA

        return ResourceType.FILE

    def refresh(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            path = Path(
                resource.metadata.path
            )

            if not path.exists():

                resource.metadata.status = (
                    ResourceStatus.MISSING
                )

            else:

                resource.metadata.status = (
                    ResourceStatus.AVAILABLE
                )

                resource.metadata.size = (
                    path.stat().st_size
                    if path.is_file()
                    else 0
                )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            return resource
        
# ============================================================
# File: studio/resource_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def archive(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            resource.metadata.status = (
                ResourceStatus.ARCHIVED
            )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "resource.archived",
                resource_id=resource_id,
            )

            return resource

    def lock(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            resource.metadata.status = (
                ResourceStatus.LOCKED
            )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "resource.locked",
                resource_id=resource_id,
            )

            return resource

    def unlock(
        self,
        resource_id: str,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            resource.metadata.status = (
                ResourceStatus.AVAILABLE
            )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "resource.unlocked",
                resource_id=resource_id,
            )

            return resource

    def move(
        self,
        resource_id: str,
        destination: Path,
    ) -> ResourceRecord:

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            source = Path(
                resource.metadata.path
            )

            if source.exists():

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                source.rename(
                    destination
                )

            resource.metadata.path = (
                str(destination)
            )

            resource.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "resource.moved",
                resource_id=resource_id,
                destination=str(
                    destination
                ),
            )

            return resource

    def duplicate(
        self,
        resource_id: str,
        destination: Path,
    ) -> ResourceRecord:

        import shutil

        with self._lock:

            resource = self._registry.get(
                resource_id
            )

            source = Path(
                resource.metadata.path
            )

            if source.is_file():

                shutil.copy2(
                    source,
                    destination,
                )

            elif source.is_dir():

                shutil.copytree(
                    source,
                    destination,
                    dirs_exist_ok=True,
                )

            return self.register(
                name=destination.name,
                resource_type=(
                    resource.metadata.resource_type
                ),
                path=destination,
                tags=(
                    resource.metadata.tags
                ),
                properties=(
                    resource.metadata.properties
                ),
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        resources = (
            self._registry.all()
        )

        types: dict[str, int] = {}

        total_size = 0

        for resource in resources:

            key = (
                resource.metadata.resource_type.value
            )

            types[key] = (
                types.get(
                    key,
                    0,
                )
                + 1
            )

            total_size += (
                resource.metadata.size
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "resource_count":
                len(resources),
            "total_size":
                total_size,
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
    
# ============================================================
# File: studio/resource_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def export_registry(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            payload = [
                asdict(
                    resource.metadata
                )
                for resource
                in self._registry.all()
            ]

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    payload,
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

                metadata = ResourceMetadata(
                    resource_id=item[
                        "resource_id"
                    ],
                    name=item[
                        "name"
                    ],
                    resource_type=ResourceType(
                        item[
                            "resource_type"
                        ]
                    ),
                    path=item[
                        "path"
                    ],
                    created_at=item[
                        "created_at"
                    ],
                    updated_at=item[
                        "updated_at"
                    ],
                    size=item.get(
                        "size",
                        0,
                    ),
                    status=ResourceStatus(
                        item[
                            "status"
                        ]
                    ),
                    tags=list(
                        item.get(
                            "tags",
                            [],
                        )
                    ),
                    properties=dict(
                        item.get(
                            "properties",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    ResourceRecord(
                        metadata=metadata
                    )
                )

                imported += 1

            self._save()

            self._emit(
                "resource.registry.imported",
                count=imported,
            )

            return imported

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.resource_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "resource_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def health_check(
        self,
    ) -> dict[str, Any]:

        missing = [
            resource.metadata.resource_id
            for resource
            in self._registry.all()
            if (
                resource.metadata.status
                is ResourceStatus.MISSING
            )
        ]

        return {
            "healthy":
                not missing,
            "missing_resources":
                missing,
            "registered_resources":
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
                "resource.registry.cleared",
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
                "resource_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
