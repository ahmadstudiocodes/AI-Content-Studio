# ============================================================
# File: studio/state_manager.py
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


class StateError(Exception):
    pass


class StateNotFound(StateError):
    pass


@dataclass(slots=True)
class StateMetadata:

    state_id: str

    namespace: str

    created_at: str

    updated_at: str

    version: int

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class StateRecord:

    metadata: StateMetadata

    values: dict[str, Any]

    path: Path


class StateRegistry:

    """
    Enterprise Thread Safe State Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._states: dict[
            str,
            StateRecord,
        ] = {}

    def add(
        self,
        state: StateRecord,
    ) -> None:

        with self._lock:

            self._states[
                state.metadata.namespace
            ] = state

    def get(
        self,
        namespace: str,
    ) -> StateRecord:

        with self._lock:

            try:

                return self._states[
                    namespace
                ]

            except KeyError as exc:

                raise StateNotFound(
                    namespace
                ) from exc

    def remove(
        self,
        namespace: str,
    ) -> None:

        with self._lock:

            self._states.pop(
                namespace
            )

    def all(
        self,
    ) -> list[StateRecord]:

        with self._lock:

            return list(
                self._states.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._states.clear()


class StateManager:

    """
    StudioOS Enterprise State Manager

    Features:

    - Persistent State Storage
    - Namespace Isolation
    - Thread Safety
    - Runtime Integration
    - Event Integration
    - Plugin Integration

    Enterprise Upgrade Ready
    """

    STATE_FILE = "state.json"

    def __init__(
        self,
        workspace: SupportsWorkspace,
        *,
        event_bus: SupportsEventBus | None = None,
        runtime: SupportsRuntime | None = None,
        plugins: SupportsPluginManager | None = None,
    ) -> None:

        self._workspace = workspace

        self._event_bus = event_bus

        self._runtime = runtime

        self._plugins = plugins

        self._lock = threading.RLock()

        self._registry = StateRegistry()

        self._root = (
            self._workspace.root /
            "state"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_states()

# ============================================================
# File: studio/state_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _state_id() -> str:

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

    def _load_existing_states(
        self,
    ) -> None:

        for state_file in self._root.rglob(
            self.STATE_FILE
        ):

            try:

                payload = json.loads(
                    state_file.read_text(
                        encoding="utf-8",
                    )
                )

                metadata = StateMetadata(
                    state_id=payload[
                        "state_id"
                    ],
                    namespace=payload[
                        "namespace"
                    ],
                    created_at=payload[
                        "created_at"
                    ],
                    updated_at=payload[
                        "updated_at"
                    ],
                    version=payload.get(
                        "version",
                        1,
                    ),
                    custom=dict(
                        payload.get(
                            "custom",
                            {},
                        )
                    ),
                )

                record = StateRecord(
                    metadata=metadata,
                    values=dict(
                        payload.get(
                            "values",
                            {},
                        )
                    ),
                    path=state_file,
                )

                self._registry.add(
                    record
                )

            except Exception:

                continue

    def _save(
        self,
        state: StateRecord,
    ) -> None:

        state.metadata.updated_at = (
            self._utc()
        )

        payload = {
            "state_id":
                state.metadata.state_id,
            "namespace":
                state.metadata.namespace,
            "created_at":
                state.metadata.created_at,
            "updated_at":
                state.metadata.updated_at,
            "version":
                state.metadata.version,
            "custom":
                state.metadata.custom,
            "values":
                state.values,
        }

        state.path.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create_namespace(
        self,
        namespace: str,
        *,
        initial: Mapping[
            str,
            Any,
        ] | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> StateRecord:

        with self._lock:

            state = StateRecord(
                metadata=StateMetadata(
                    state_id=self._state_id(),
                    namespace=namespace,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    version=1,
                    custom=dict(
                        custom or {}
                    ),
                ),
                values=dict(
                    initial or {}
                ),
                path=(
                    self._root /
                    namespace /
                    self.STATE_FILE
                ),
            )

            state.path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._save(
                state
            )

            self._registry.add(
                state
            )

            self._emit(
                "state.namespace.created",
                namespace=namespace,
            )

            return state
        
# ============================================================
# File: studio/state_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get_namespace(
        self,
        namespace: str,
    ) -> StateRecord:

        return self._registry.get(
            namespace
        )

    def delete_namespace(
        self,
        namespace: str,
        *,
        delete_file: bool = True,
    ) -> None:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            if delete_file:

                if state.path.exists():

                    state.path.unlink()

                if state.path.parent.exists():

                    try:

                        state.path.parent.rmdir()

                    except OSError:

                        pass

            self._registry.remove(
                namespace
            )

            self._emit(
                "state.namespace.deleted",
                namespace=namespace,
            )

    def set_value(
        self,
        namespace: str,
        key: str,
        value: Any,
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            state.values[key] = value

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.value.updated",
                namespace=namespace,
                key=key,
            )

            return state

    def get_value(
        self,
        namespace: str,
        key: str,
        default: Any = None,
    ) -> Any:

        state = self._registry.get(
            namespace
        )

        return state.values.get(
            key,
            default,
        )

    def remove_value(
        self,
        namespace: str,
        key: str,
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            state.values.pop(
                key,
                None,
            )

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.value.removed",
                namespace=namespace,
                key=key,
            )

            return state

    def update(
        self,
        namespace: str,
        values: Mapping[
            str,
            Any,
        ],
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            state.values.update(
                values
            )

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.updated",
                namespace=namespace,
            )

            return state

    def clear_values(
        self,
        namespace: str,
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            state.values.clear()

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.cleared",
                namespace=namespace,
            )

            return state
        
# ============================================================
# File: studio/state_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def snapshot(
        self,
        namespace: str,
    ) -> dict[str, Any]:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            return {
                "state_id":
                    state.metadata.state_id,
                "namespace":
                    state.metadata.namespace,
                "version":
                    state.metadata.version,
                "timestamp":
                    self._utc(),
                "values":
                    dict(state.values),
            }

    def restore_snapshot(
        self,
        namespace: str,
        snapshot: Mapping[
            str,
            Any,
        ],
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            values = snapshot.get(
                "values",
                {},
            )

            state.values = dict(
                values
            )

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.snapshot.restored",
                namespace=namespace,
            )

            return state

    def export_state(
        self,
        namespace: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            state = self._registry.get(
                namespace
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
                                state.metadata
                            ),
                        "values":
                            state.values,
                    },
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_state(
        self,
        source: Path,
    ) -> StateRecord:

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

            namespace = metadata[
                "namespace"
            ]

            state = StateRecord(
                metadata=StateMetadata(
                    state_id=self._state_id(),
                    namespace=namespace,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    version=1,
                    custom=dict(
                        metadata.get(
                            "custom",
                            {},
                        )
                    ),
                ),
                values=dict(
                    payload.get(
                        "values",
                        {},
                    )
                ),
                path=(
                    self._root /
                    namespace /
                    self.STATE_FILE
                ),
            )

            state.path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._save(
                state
            )

            self._registry.add(
                state
            )

            self._emit(
                "state.imported",
                namespace=namespace,
            )

            return state

    def list_namespaces(
        self,
    ) -> list[str]:

        return [
            state.metadata.namespace
            for state
            in self._registry.all()
        ]
# ============================================================
# File: studio/state_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def statistics(
        self,
    ) -> dict[str, Any]:

        states = self._registry.all()

        total_values = 0

        versions: dict[str, int] = {}

        for state in states:

            total_values += len(
                state.values
            )

            versions[
                state.metadata.namespace
            ] = state.metadata.version

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "namespace_count":
                len(states),
            "total_values":
                total_values,
            "versions":
                versions,
            "runtime_connected":
                self._runtime is not None,
            "event_bus_connected":
                self._event_bus is not None,
            "plugin_manager_connected":
                self._plugins is not None,
        }

    def health_check(
        self,
    ) -> dict[str, Any]:

        invalid: list[str] = []

        for state in self._registry.all():

            if not state.path.exists():

                invalid.append(
                    state.metadata.namespace
                )

        return {
            "healthy":
                not invalid,
            "invalid_states":
                invalid,
            "registered_namespaces":
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

            for state in self._registry.all():

                self._save(
                    state
                )

            if self._event_bus is not None:

                self._event_bus.publish(
                    "state_manager.synchronized",
                    workspace=(
                        self._workspace.workspace_id
                    ),
                )

    def reset(
        self,
        namespace: str,
    ) -> StateRecord:

        with self._lock:

            state = self._registry.get(
                namespace
            )

            state.values.clear()

            state.metadata.version += 1

            self._save(
                state
            )

            self._emit(
                "state.reset",
                namespace=namespace,
            )

            return state

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "state_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
