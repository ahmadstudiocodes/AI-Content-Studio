# ============================================================
# File: studio/config_manager.py
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

    def is_running(
        self,
    ) -> bool: ...


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


@dataclass(slots=True)
class ConfigMetadata:

    config_id: str

    name: str

    version: str

    created_at: str

    updated_at: str

    owner: str | None = None

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class ConfigRecord:

    metadata: ConfigMetadata

    path: Path

    data: dict[str, Any]


class ConfigError(Exception):
    pass


class ConfigNotFound(ConfigError):
    pass


class InvalidConfiguration(ConfigError):
    pass


class ConfigRegistry:

    """
    Enterprise Thread Safe Configuration Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._configs: dict[
            str,
            ConfigRecord,
        ] = {}

    def add(
        self,
        record: ConfigRecord,
    ) -> None:

        with self._lock:

            self._configs[
                record.metadata.config_id
            ] = record

    def get(
        self,
        config_id: str,
    ) -> ConfigRecord:

        with self._lock:

            try:

                return self._configs[
                    config_id
                ]

            except KeyError as exc:

                raise ConfigNotFound(
                    config_id
                ) from exc

    def remove(
        self,
        config_id: str,
    ) -> None:

        with self._lock:

            self._configs.pop(
                config_id
            )

    def all(
        self,
    ) -> list[ConfigRecord]:

        with self._lock:

            return list(
                self._configs.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._configs.clear()


class ConfigManager:

    """
    StudioOS Enterprise Configuration Manager

    Central configuration service

    Features:

    - Workspace Configuration
    - Project Configuration
    - Runtime Configuration
    - Plugin Configuration
    - Persistent Storage
    - Event Integration
    - Shared State Integration

    Enterprise Upgrade Ready
    """

    CONFIG_FILE = "config.json"

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

        self._registry = ConfigRegistry()

        self._root = (
            self._workspace.root /
            "config"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_configs()

# ============================================================
# File: studio/config_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _config_id() -> str:

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

    def _load_existing_configs(
        self,
    ) -> None:

        for config_file in self._root.rglob(
            self.CONFIG_FILE
        ):

            try:

                data = json.loads(
                    config_file.read_text(
                        encoding="utf-8",
                    )
                )

                metadata = ConfigMetadata(
                    config_id=data[
                        "config_id"
                    ],
                    name=data[
                        "name"
                    ],
                    version=data.get(
                        "version",
                        "1.0.0",
                    ),
                    created_at=data[
                        "created_at"
                    ],
                    updated_at=data[
                        "updated_at"
                    ],
                    owner=data.get(
                        "owner"
                    ),
                    custom=dict(
                        data.get(
                            "metadata",
                            {},
                        )
                    ),
                )

                record = ConfigRecord(
                    metadata=metadata,
                    path=config_file,
                    data=dict(
                        data.get(
                            "data",
                            {},
                        )
                    ),
                )

                self._registry.add(
                    record
                )

            except Exception:

                continue

    def _save(
        self,
        record: ConfigRecord,
    ) -> None:

        record.metadata.updated_at = (
            self._utc()
        )

        payload = {
            "config_id":
                record.metadata.config_id,
            "name":
                record.metadata.name,
            "version":
                record.metadata.version,
            "created_at":
                record.metadata.created_at,
            "updated_at":
                record.metadata.updated_at,
            "owner":
                record.metadata.owner,
            "metadata":
                record.metadata.custom,
            "data":
                record.data,
        }

        record.path.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create_config(
        self,
        *,
        name: str,
        data: Mapping[
            str,
            Any,
        ],
        version: str = "1.0.0",
        owner: str | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> ConfigRecord:

        with self._lock:

            config_id = (
                self._config_id()
            )

            root = (
                self._root /
                name
            )

            root.mkdir(
                parents=True,
                exist_ok=True,
            )

            record = ConfigRecord(
                metadata=ConfigMetadata(
                    config_id=config_id,
                    name=name,
                    version=version,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    owner=owner,
                    custom=dict(
                        custom or {}
                    ),
                ),
                path=(
                    root /
                    self.CONFIG_FILE
                ),
                data=dict(
                    data
                ),
            )

            self._save(
                record
            )

            self._registry.add(
                record
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    f"config:{name}",
                    config_id,
                )

            self._emit(
                "config.created",
                config_id=config_id,
                name=name,
            )

            return record
        
# ============================================================
# File: studio/config_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get_config(
        self,
        config_id: str,
    ) -> ConfigRecord:

        return self._registry.get(
            config_id
        )

    def list_configs(
        self,
    ) -> list[ConfigRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def update_config(
        self,
        config_id: str,
        updates: Mapping[
            str,
            Any,
        ],
    ) -> ConfigRecord:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            record.data.update(
                updates
            )

            self._save(
                record
            )

            self._emit(
                "config.updated",
                config_id=config_id,
            )

            return record

    def replace_config(
        self,
        config_id: str,
        data: Mapping[
            str,
            Any,
        ],
    ) -> ConfigRecord:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            record.data = dict(
                data
            )

            self._save(
                record
            )

            self._emit(
                "config.replaced",
                config_id=config_id,
            )

            return record

    def delete_config(
        self,
        config_id: str,
        *,
        delete_file: bool = True,
    ) -> None:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            if delete_file:

                if record.path.exists():

                    record.path.unlink()

                if record.path.parent.exists():

                    try:

                        record.path.parent.rmdir()

                    except OSError:

                        pass

            self._registry.remove(
                config_id
            )

            self._emit(
                "config.deleted",
                config_id=config_id,
            )

    def clone_config(
        self,
        config_id: str,
        new_name: str,
    ) -> ConfigRecord:

        with self._lock:

            source = (
                self._registry.get(
                    config_id
                )
            )

            clone = ConfigRecord(
                metadata=ConfigMetadata(
                    config_id=self._config_id(),
                    name=new_name,
                    version=(
                        source.metadata.version
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    owner=(
                        source.metadata.owner
                    ),
                    custom=dict(
                        source.metadata.custom
                    ),
                ),
                path=(
                    self._root /
                    new_name /
                    self.CONFIG_FILE
                ),
                data=dict(
                    source.data
                ),
            )

            clone.path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._save(
                clone
            )

            self._registry.add(
                clone
            )

            self._emit(
                "config.cloned",
                source=config_id,
                clone=(
                    clone.metadata.config_id
                ),
            )

            return clone

    def get_value(
        self,
        config_id: str,
        key: str,
        default: Any = None,
    ) -> Any:

        record = self._registry.get(
            config_id
        )

        return record.data.get(
            key,
            default,
        )
    
# ============================================================
# File: studio/config_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def set_value(
        self,
        config_id: str,
        key: str,
        value: Any,
    ) -> ConfigRecord:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            record.data[key] = value

            self._save(
                record
            )

            self._emit(
                "config.value.updated",
                config_id=config_id,
                key=key,
            )

            return record

    def remove_value(
        self,
        config_id: str,
        key: str,
    ) -> ConfigRecord:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            record.data.pop(
                key,
                None,
            )

            self._save(
                record
            )

            self._emit(
                "config.value.removed",
                config_id=config_id,
                key=key,
            )

            return record

    def export_config(
        self,
        config_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            record = self._registry.get(
                config_id
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
                                record.metadata
                            ),
                        "data":
                            record.data,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_config(
        self,
        source: Path,
    ) -> ConfigRecord:

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

            record = ConfigRecord(
                metadata=ConfigMetadata(
                    config_id=self._config_id(),
                    name=metadata[
                        "name"
                    ],
                    version=metadata.get(
                        "version",
                        "1.0.0",
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    owner=metadata.get(
                        "owner"
                    ),
                    custom=dict(
                        metadata.get(
                            "custom",
                            {},
                        )
                    ),
                ),
                path=(
                    self._root /
                    metadata["name"] /
                    self.CONFIG_FILE
                ),
                data=dict(
                    payload.get(
                        "data",
                        {},
                    )
                ),
            )

            record.path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._save(
                record
            )

            self._registry.add(
                record
            )

            self._emit(
                "config.imported",
                config_id=(
                    record.metadata.config_id
                ),
            )

            return record

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for config in self._registry.all():

                self._save(
                    config
                )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.config_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "config_manager.synchronized",
                workspace=self._workspace.workspace_id,
            )

# ============================================================
# File: studio/config_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def statistics(
        self,
    ) -> dict[str, Any]:

        configs = self._registry.all()

        total_keys = 0

        for config in configs:

            total_keys += len(
                config.data
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "config_count":
                len(configs),
            "total_keys":
                total_keys,
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

        for config in self._registry.all():

            if not config.path.exists():

                invalid.append(
                    config.metadata.config_id
                )

        return {
            "healthy": not invalid,
            "invalid_configs": invalid,
            "registered_configs": len(
                self._registry.all()
            ),
            "timestamp": time.time(),
        }

    def reload_config(
        self,
        config_id: str,
    ) -> ConfigRecord:

        with self._lock:

            record = self._registry.get(
                config_id
            )

            if not record.path.exists():

                raise ConfigNotFound(
                    config_id
                )

            payload = json.loads(
                record.path.read_text(
                    encoding="utf-8",
                )
            )

            record.data = dict(
                payload.get(
                    "data",
                    {},
                )
            )

            record.metadata.updated_at = (
                self._utc()
            )

            self._emit(
                "config.reloaded",
                config_id=config_id,
            )

            return record

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._registry.clear()

            self._emit(
                "config_manager.cleared",
                workspace=self._workspace.workspace_id,
            )

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "config_manager.shutdown",
                workspace=self._workspace.workspace_id,
            )

            self._registry.clear()
