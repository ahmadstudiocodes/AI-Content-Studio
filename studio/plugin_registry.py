# ============================================================
# File: studio/plugin_registry.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import importlib
import json
import threading
import time
import uuid

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol


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

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any: ...

    def set(
        self,
        key: str,
        value: Any,
    ) -> None: ...


class SupportsRuntime(Protocol):

    def is_running(self) -> bool: ...


class PluginStatus(str, Enum):

    REGISTERED = "registered"
    ENABLED = "enabled"
    DISABLED = "disabled"
    FAILED = "failed"
    REMOVED = "removed"


@dataclass(slots=True)
class PluginMetadata:

    plugin_id: str

    name: str

    version: str

    module: str

    description: str

    status: PluginStatus

    created_at: str

    updated_at: str

    author: str | None = None

    dependencies: list[str] = field(
        default_factory=list
    )

    hooks: list[str] = field(
        default_factory=list
    )

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class PluginRecord:

    metadata: PluginMetadata

    root: Path

    metadata_file: Path

    instance: Any | None = None


class PluginRegistryError(Exception):
    pass


class PluginAlreadyExists(
    PluginRegistryError
):
    pass


class PluginNotFound(
    PluginRegistryError
):
    pass


class PluginRegistryStore:

    """
    Enterprise Thread Safe Plugin Store
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._plugins: dict[
            str,
            PluginRecord,
        ] = {}

    def add(
        self,
        plugin: PluginRecord,
    ) -> None:

        with self._lock:

            if (
                plugin.metadata.plugin_id
                in self._plugins
            ):
                raise PluginAlreadyExists(
                    plugin.metadata.plugin_id
                )

            self._plugins[
                plugin.metadata.plugin_id
            ] = plugin

    def get(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        with self._lock:

            try:

                return self._plugins[
                    plugin_id
                ]

            except KeyError as exc:

                raise PluginNotFound(
                    plugin_id
                ) from exc

    def remove(
        self,
        plugin_id: str,
    ) -> None:

        with self._lock:

            self._plugins.pop(
                plugin_id
            )

    def all(
        self,
    ) -> list[PluginRecord]:

        with self._lock:

            return list(
                self._plugins.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._plugins.clear()


class PluginRegistry:

    """
    StudioOS Enterprise Plugin Registry

    Plugin Discovery
    Plugin Metadata Management
    Runtime Integration
    Event Bus Integration
    Shared State Integration

    Enterprise Upgrade Ready
    """

    REGISTRY_FILE = "plugin.json"

    def __init__(
        self,
        workspace: SupportsWorkspace,
        *,
        event_bus: SupportsEventBus | None = None,
        shared_state: SupportsSharedState | None = None,
        runtime: SupportsRuntime | None = None,
    ) -> None:

        self._workspace = workspace

        self._event_bus = event_bus

        self._shared_state = shared_state

        self._runtime = runtime

        self._lock = threading.RLock()

        self._store = PluginRegistryStore()

        self._root = (
            self._workspace.root /
            "plugins"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_plugins()

# ============================================================
# File: studio/plugin_registry.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _plugin_id() -> str:

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

    def _load_existing_plugins(
        self,
    ) -> None:

        for metadata_file in self._root.rglob(
            self.REGISTRY_FILE
        ):

            try:

                data = json.loads(
                    metadata_file.read_text(
                        encoding="utf-8",
                    )
                )

                plugin_root = (
                    metadata_file.parent
                )

                record = PluginRecord(
                    metadata=PluginMetadata(
                        plugin_id=data[
                            "plugin_id"
                        ],
                        name=data[
                            "name"
                        ],
                        version=data[
                            "version"
                        ],
                        module=data[
                            "module"
                        ],
                        description=data.get(
                            "description",
                            "",
                        ),
                        status=PluginStatus(
                            data[
                                "status"
                            ]
                        ),
                        created_at=data[
                            "created_at"
                        ],
                        updated_at=data[
                            "updated_at"
                        ],
                        author=data.get(
                            "author"
                        ),
                        dependencies=list(
                            data.get(
                                "dependencies",
                                [],
                            )
                        ),
                        hooks=list(
                            data.get(
                                "hooks",
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
                    root=plugin_root,
                    metadata_file=metadata_file,
                )

                self._store.add(
                    record
                )

            except Exception:

                continue

    def _save(
        self,
        plugin: PluginRecord,
    ) -> None:

        plugin.metadata.updated_at = (
            self._utc()
        )

        plugin.metadata_file.write_text(
            json.dumps(
                asdict(
                    plugin.metadata
                ),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def register_plugin(
        self,
        *,
        name: str,
        module: str,
        version: str = "1.0.0",
        description: str = "",
        author: str | None = None,
        dependencies: Iterable[str] = (),
        hooks: Iterable[str] = (),
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> PluginRecord:

        with self._lock:

            plugin_id = (
                self._plugin_id()
            )

            root = (
                self._root /
                name
            )

            root.mkdir(
                parents=True,
                exist_ok=True,
            )

            record = PluginRecord(
                metadata=PluginMetadata(
                    plugin_id=plugin_id,
                    name=name,
                    version=version,
                    module=module,
                    description=description,
                    status=PluginStatus.REGISTERED,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    author=author,
                    dependencies=list(
                        dependencies
                    ),
                    hooks=list(
                        hooks
                    ),
                    custom=dict(
                        custom or {}
                    ),
                ),
                root=root,
                metadata_file=(
                    root /
                    self.REGISTRY_FILE
                ),
            )

            self._save(
                record
            )

            self._store.add(
                record
            )

            self._emit(
                "plugin.registered",
                plugin_id=plugin_id,
                name=name,
            )

            return record
        
# ============================================================
# File: studio/plugin_registry.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def load_plugin(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        with self._lock:

            plugin = self._store.get(
                plugin_id
            )

            if plugin.instance is not None:

                return plugin

            try:

                module = importlib.import_module(
                    plugin.metadata.module
                )

                if hasattr(
                    module,
                    "Plugin",
                ):

                    plugin.instance = (
                        module.Plugin()
                    )

                else:

                    plugin.instance = module

                plugin.metadata.status = (
                    PluginStatus.ENABLED
                )

                self._save(
                    plugin
                )

                self._emit(
                    "plugin.loaded",
                    plugin_id=plugin_id,
                    name=plugin.metadata.name,
                )

                return plugin

            except Exception as exc:

                plugin.metadata.status = (
                    PluginStatus.FAILED
                )

                plugin.metadata.custom[
                    "error"
                ] = str(exc)

                self._save(
                    plugin
                )

                self._emit(
                    "plugin.failed",
                    plugin_id=plugin_id,
                    error=str(exc),
                )

                raise

    def unload_plugin(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        with self._lock:

            plugin = self._store.get(
                plugin_id
            )

            if plugin.instance is not None:

                shutdown = getattr(
                    plugin.instance,
                    "shutdown",
                    None,
                )

                if callable(shutdown):

                    shutdown()

            plugin.instance = None

            plugin.metadata.status = (
                PluginStatus.DISABLED
            )

            self._save(
                plugin
            )

            self._emit(
                "plugin.unloaded",
                plugin_id=plugin_id,
            )

            return plugin

    def enable_plugin(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        plugin = self.load_plugin(
            plugin_id
        )

        with self._lock:

            plugin.metadata.status = (
                PluginStatus.ENABLED
            )

            self._save(
                plugin
            )

            self._emit(
                "plugin.enabled",
                plugin_id=plugin_id,
            )

            return plugin

    def disable_plugin(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        with self._lock:

            plugin = self._store.get(
                plugin_id
            )

            plugin.metadata.status = (
                PluginStatus.DISABLED
            )

            self._save(
                plugin
            )

            self._emit(
                "plugin.disabled",
                plugin_id=plugin_id,
            )

            return plugin

    def remove_plugin(
        self,
        plugin_id: str,
        *,
        delete_files: bool = False,
    ) -> None:

        with self._lock:

            plugin = self._store.get(
                plugin_id
            )

            if plugin.instance is not None:

                self.unload_plugin(
                    plugin_id
                )

            if delete_files:

                for item in plugin.root.rglob("*"):

                    if item.is_file():

                        item.unlink()

                for item in sorted(
                    plugin.root.rglob("*"),
                    reverse=True,
                ):

                    if item.is_dir():

                        item.rmdir()

                plugin.root.rmdir()

            self._store.remove(
                plugin_id
            )

            self._emit(
                "plugin.removed",
                plugin_id=plugin_id,
            )

# ============================================================
# File: studio/plugin_registry.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def get_plugin(
        self,
        plugin_id: str,
    ) -> PluginRecord:

        return self._store.get(
            plugin_id
        )

    def list_plugins(
        self,
    ) -> list[PluginRecord]:

        return sorted(
            self._store.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def find_by_name(
        self,
        name: str,
    ) -> list[PluginRecord]:

        keyword = name.lower()

        return [
            plugin
            for plugin in self._store.all()
            if keyword
            in plugin.metadata.name.lower()
        ]

    def find_by_hook(
        self,
        hook: str,
    ) -> list[PluginRecord]:

        return [
            plugin
            for plugin in self._store.all()
            if hook
            in plugin.metadata.hooks
        ]

    def execute_hook(
        self,
        hook: str,
        **payload: Any,
    ) -> list[Any]:

        results: list[Any] = []

        with self._lock:

            plugins = self.find_by_hook(
                hook
            )

            for plugin in plugins:

                if (
                    plugin.metadata.status
                    is not PluginStatus.ENABLED
                ):
                    continue

                if plugin.instance is None:

                    continue

                handler = getattr(
                    plugin.instance,
                    hook,
                    None,
                )

                if callable(handler):

                    results.append(
                        handler(
                            **payload
                        )
                    )

        return results

    def update_metadata(
        self,
        plugin_id: str,
        *,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
        hooks: Iterable[str] | None = None,
    ) -> PluginRecord:

        with self._lock:

            plugin = self._store.get(
                plugin_id
            )

            if custom is not None:

                plugin.metadata.custom.update(
                    custom
                )

            if hooks is not None:

                plugin.metadata.hooks = list(
                    hooks
                )

            self._save(
                plugin
            )

            self._emit(
                "plugin.updated",
                plugin_id=plugin_id,
            )

            return plugin

    def statistics(
        self,
    ) -> dict[str, Any]:

        plugins = self._store.all()

        status: dict[str, int] = {}

        for plugin in plugins:

            key = (
                plugin.metadata.status.value
            )

            status[key] = (
                status.get(key, 0)
                + 1
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "plugin_count":
                len(plugins),
            "status":
                status,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "shared_state_connected":
                self._shared_state is not None,
        }
# ============================================================
# File: studio/plugin_registry.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def export_registry(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            data = [
                asdict(
                    plugin.metadata
                )
                for plugin in self._store.all()
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

            data = json.loads(
                source.read_text(
                    encoding="utf-8",
                )
            )

            imported = 0

            for item in data:

                root = (
                    self._root /
                    item["name"]
                )

                record = PluginRecord(
                    metadata=PluginMetadata(
                        plugin_id=item[
                            "plugin_id"
                        ],
                        name=item[
                            "name"
                        ],
                        version=item[
                            "version"
                        ],
                        module=item[
                            "module"
                        ],
                        description=item.get(
                            "description",
                            "",
                        ),
                        status=PluginStatus(
                            item["status"]
                        ),
                        created_at=item[
                            "created_at"
                        ],
                        updated_at=item[
                            "updated_at"
                        ],
                        author=item.get(
                            "author"
                        ),
                        dependencies=list(
                            item.get(
                                "dependencies",
                                [],
                            )
                        ),
                        hooks=list(
                            item.get(
                                "hooks",
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
                    root=root,
                    metadata_file=(
                        root /
                        self.REGISTRY_FILE
                    ),
                )

                try:

                    self._store.add(
                        record
                    )

                    imported += 1

                except PluginAlreadyExists:

                    continue

            self._emit(
                "plugin.registry.imported",
                count=imported,
            )

            return imported

    def health_check(
        self,
    ) -> dict[str, Any]:

        failed: list[str] = []

        for plugin in self._store.all():

            if (
                plugin.metadata.status
                is PluginStatus.FAILED
            ):

                failed.append(
                    plugin.metadata.plugin_id
                )

        return {
            "healthy": not failed,
            "failed_plugins": failed,
            "registered_plugins": len(
                self._store.all()
            ),
            "timestamp": time.time(),
        }

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for plugin in self._store.all():

                self._save(
                    plugin
                )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.plugin_count",
                    len(
                        self._store.all()
                    ),
                )

            self._emit(
                "plugin_registry.synchronized",
                workspace=self._workspace.workspace_id,
            )

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            for plugin in self._store.all():

                if plugin.instance is not None:

                    self.unload_plugin(
                        plugin.metadata.plugin_id
                    )

            self.synchronize()

            self._emit(
                "plugin_registry.shutdown",
                workspace=self._workspace.workspace_id,
            )

            self._store.clear()
