# ============================================================
# File: studio/scene_manager.py
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


class SceneStatus(str, Enum):

    ACTIVE = "active"

    SAVED = "saved"

    ARCHIVED = "archived"

    LOCKED = "locked"


class SceneType(str, Enum):

    EMPTY = "empty"

    ARCHITECTURE = "architecture"

    ANIMATION = "animation"

    VFX = "vfx"

    CUSTOM = "custom"


@dataclass(slots=True)
class SceneMetadata:

    scene_id: str

    name: str

    scene_type: SceneType

    created_at: str

    updated_at: str

    status: SceneStatus

    version: int

    description: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class SceneRecord:

    metadata: SceneMetadata

    objects: list[dict[str, Any]] = field(
        default_factory=list
    )

    settings: dict[str, Any] = field(
        default_factory=dict
    )


class SceneManagerError(Exception):
    pass


class SceneNotFound(
    SceneManagerError
):
    pass


class SceneRegistry:

    """
    Enterprise Thread Safe Scene Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._scenes: dict[
            str,
            SceneRecord,
        ] = {}

    def add(
        self,
        scene: SceneRecord,
    ) -> None:

        with self._lock:

            self._scenes[
                scene.metadata.scene_id
            ] = scene

    def get(
        self,
        scene_id: str,
    ) -> SceneRecord:

        with self._lock:

            try:

                return self._scenes[
                    scene_id
                ]

            except KeyError as exc:

                raise SceneNotFound(
                    scene_id
                ) from exc

    def all(
        self,
    ) -> list[SceneRecord]:

        with self._lock:

            return list(
                self._scenes.values()
            )

    def remove(
        self,
        scene_id: str,
    ) -> None:

        with self._lock:

            self._scenes.pop(
                scene_id
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._scenes.clear()


class SceneManager:

    """
    StudioOS Enterprise Scene Manager

    Features:

    - Scene Lifecycle
    - Object Management
    - Scene Versioning
    - Runtime Integration
    - Event Integration
    - Shared State Sync
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    SCENE_FILE = "scenes.json"

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

        self._registry = SceneRegistry()

        self._root = (
            self._workspace.root /
            "scenes"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._file = (
            self._root /
            self.SCENE_FILE
        )

        self._load()

# ============================================================
# File: studio/scene_manager.py
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

                scene = SceneRecord(
                    metadata=SceneMetadata(
                        scene_id=metadata[
                            "scene_id"
                        ],
                        name=metadata[
                            "name"
                        ],
                        scene_type=SceneType(
                            metadata[
                                "scene_type"
                            ]
                        ),
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        status=SceneStatus(
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
                        tags=list(
                            metadata.get(
                                "tags",
                                [],
                            )
                        ),
                        properties=dict(
                            metadata.get(
                                "properties",
                                {},
                            )
                        ),
                    ),
                    objects=list(
                        item.get(
                            "objects",
                            [],
                        )
                    ),
                    settings=dict(
                        item.get(
                            "settings",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    scene
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
                        scene.metadata
                    ),
                "objects":
                    scene.objects,
                "settings":
                    scene.settings,
            }
            for scene
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
        scene_type: SceneType,
        description: str = "",
        tags: list[str] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> SceneRecord:

        with self._lock:

            scene = SceneRecord(
                metadata=SceneMetadata(
                    scene_id=self._id(),
                    name=name,
                    scene_type=scene_type,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=SceneStatus.ACTIVE,
                    version=1,
                    description=description,
                    tags=list(
                        tags or []
                    ),
                    properties=dict(
                        properties or {}
                    ),
                )
            )

            self._registry.add(
                scene
            )

            self._save()

            self._emit(
                "scene.created",
                scene_id=(
                    scene.metadata.scene_id
                ),
            )

            return scene

    def get(
        self,
        scene_id: str,
    ) -> SceneRecord:

        return self._registry.get(
            scene_id
        )
    
# ============================================================
# File: studio/scene_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def list_scenes(
        self,
    ) -> list[SceneRecord]:

        return self._registry.all()

    def update(
        self,
        scene_id: str,
        *,
        settings: Mapping[
            str,
            Any,
        ] | None = None,
        properties: Mapping[
            str,
            Any,
        ] | None = None,
        tags: list[str] | None = None,
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            if settings is not None:

                scene.settings.update(
                    settings
                )

            if properties is not None:

                scene.metadata.properties.update(
                    properties
                )

            if tags is not None:

                scene.metadata.tags = (
                    list(tags)
                )

            scene.metadata.version += 1

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.updated",
                scene_id=scene_id,
                version=(
                    scene.metadata.version
                ),
            )

            return scene

    def add_object(
        self,
        scene_id: str,
        obj: Mapping[
            str,
            Any,
        ],
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            object_data = dict(
                obj
            )

            if "id" not in object_data:

                object_data[
                    "id"
                ] = self._id()

            scene.objects.append(
                object_data
            )

            scene.metadata.version += 1

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.object.added",
                scene_id=scene_id,
                object_id=(
                    object_data["id"]
                ),
            )

            return scene

    def remove_object(
        self,
        scene_id: str,
        object_id: str,
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            scene.objects = [
                obj
                for obj
                in scene.objects
                if obj.get(
                    "id"
                )
                != object_id
            ]

            scene.metadata.version += 1

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.object.removed",
                scene_id=scene_id,
                object_id=object_id,
            )

            return scene

    def duplicate(
        self,
        scene_id: str,
        new_name: str,
    ) -> SceneRecord:

        with self._lock:

            source = self._registry.get(
                scene_id
            )

            clone = SceneRecord(
                metadata=SceneMetadata(
                    scene_id=self._id(),
                    name=new_name,
                    scene_type=(
                        source.metadata.scene_type
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=SceneStatus.ACTIVE,
                    version=1,
                    description=(
                        source.metadata.description
                    ),
                    tags=list(
                        source.metadata.tags
                    ),
                    properties=dict(
                        source.metadata.properties
                    ),
                ),
                objects=[
                    dict(obj)
                    for obj
                    in source.objects
                ],
                settings=dict(
                    source.settings
                ),
            )

            self._registry.add(
                clone
            )

            self._save()

            self._emit(
                "scene.duplicated",
                source=scene_id,
                scene_id=(
                    clone.metadata.scene_id
                ),
            )

            return clone

    def archive(
        self,
        scene_id: str,
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            scene.metadata.status = (
                SceneStatus.ARCHIVED
            )

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.archived",
                scene_id=scene_id,
            )

            return scene
        
# ============================================================
# File: studio/scene_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def lock(
        self,
        scene_id: str,
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            scene.metadata.status = (
                SceneStatus.LOCKED
            )

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.locked",
                scene_id=scene_id,
            )

            return scene

    def unlock(
        self,
        scene_id: str,
    ) -> SceneRecord:

        with self._lock:

            scene = self._registry.get(
                scene_id
            )

            scene.metadata.status = (
                SceneStatus.ACTIVE
            )

            scene.metadata.updated_at = (
                self._utc()
            )

            self._save()

            self._emit(
                "scene.unlocked",
                scene_id=scene_id,
            )

            return scene

    def delete(
        self,
        scene_id: str,
    ) -> None:

        with self._lock:

            self._registry.remove(
                scene_id
            )

            self._save()

            self._emit(
                "scene.deleted",
                scene_id=scene_id,
            )

    def find_by_type(
        self,
        scene_type: SceneType,
    ) -> list[SceneRecord]:

        return [
            scene
            for scene
            in self._registry.all()
            if (
                scene.metadata.scene_type
                is scene_type
            )
        ]

    def find_by_tag(
        self,
        tag: str,
    ) -> list[SceneRecord]:

        return [
            scene
            for scene
            in self._registry.all()
            if tag
            in scene.metadata.tags
        ]

    def export_scene(
        self,
        scene_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            scene = self._registry.get(
                scene_id
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
                                scene.metadata
                            ),
                        "objects":
                            scene.objects,
                        "settings":
                            scene.settings,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_scene(
        self,
        source: Path,
    ) -> SceneRecord:

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

            scene = SceneRecord(
                metadata=SceneMetadata(
                    scene_id=self._id(),
                    name=metadata[
                        "name"
                    ],
                    scene_type=SceneType(
                        metadata[
                            "scene_type"
                        ]
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=SceneStatus.ACTIVE,
                    version=1,
                    description=metadata.get(
                        "description",
                        "",
                    ),
                    tags=list(
                        metadata.get(
                            "tags",
                            [],
                        )
                    ),
                    properties=dict(
                        metadata.get(
                            "properties",
                            {},
                        )
                    ),
                ),
                objects=list(
                    payload.get(
                        "objects",
                        [],
                    )
                ),
                settings=dict(
                    payload.get(
                        "settings",
                        {},
                    )
                ),
            )

            self._registry.add(
                scene
            )

            self._save()

            self._emit(
                "scene.imported",
                scene_id=(
                    scene.metadata.scene_id
                ),
            )

            return scene
        
        # ============================================================
# File: studio/scene_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            self._save()

            scenes = (
                self._registry.all()
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.scene_count",
                    len(scenes),
                )

            self._emit(
                "scene_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        scenes = (
            self._registry.all()
        )

        types: dict[
            str,
            int,
        ] = {}

        statuses: dict[
            str,
            int,
        ] = {}

        total_objects = 0

        for scene in scenes:

            scene_type = (
                scene.metadata.scene_type.value
            )

            status = (
                scene.metadata.status.value
            )

            types[scene_type] = (
                types.get(
                    scene_type,
                    0,
                )
                + 1
            )

            statuses[status] = (
                statuses.get(
                    status,
                    0,
                )
                + 1
            )

            total_objects += (
                len(
                    scene.objects
                )
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "scene_count":
                len(scenes),
            "object_count":
                total_objects,
            "types":
                types,
            "statuses":
                statuses,
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

        for scene in (
            self._registry.all()
        ):

            if not scene.metadata.name:

                invalid.append(
                    scene.metadata.scene_id
                )

        return {
            "healthy":
                not invalid,
            "invalid_scenes":
                invalid,
            "registered_scenes":
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
                "scene.registry.cleared",
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
                "scene_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
