# ============================================================
# File: studio/session_manager.py
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

    def is_running(self) -> bool: ...


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


class SessionStatus(str, Enum):

    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    CRASHED = "crashed"


@dataclass(slots=True)
class SessionMetadata:

    session_id: str

    project_id: str

    workspace_id: str

    status: SessionStatus

    created_at: str

    updated_at: str

    last_activity: str

    user: str | None = None

    custom: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SessionRecord:

    metadata: SessionMetadata

    root: Path

    state_file: Path

    log_file: Path

    recovery_file: Path


class SessionError(Exception):
    pass


class SessionAlreadyExists(SessionError):
    pass


class SessionNotFound(SessionError):
    pass


class SessionRegistry:

    """
    Enterprise Thread Safe Session Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._sessions: dict[str, SessionRecord] = {}

    def add(
        self,
        record: SessionRecord,
    ) -> None:

        with self._lock:

            if record.metadata.session_id in self._sessions:
                raise SessionAlreadyExists(
                    record.metadata.session_id
                )

            self._sessions[
                record.metadata.session_id
            ] = record

    def get(
        self,
        session_id: str,
    ) -> SessionRecord:

        with self._lock:

            try:
                return self._sessions[session_id]

            except KeyError as exc:
                raise SessionNotFound(
                    session_id
                ) from exc

    def remove(
        self,
        session_id: str,
    ) -> None:

        with self._lock:

            self._sessions.pop(session_id)

    def all(
        self,
    ) -> list[SessionRecord]:

        with self._lock:

            return list(
                self._sessions.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._sessions.clear()


class SessionManager:

    """
    StudioOS Enterprise Session Manager

    Workspace Integration
    Runtime Integration
    Shared State Integration
    Event Bus Integration
    Plugin Integration

    Enterprise Upgrade Ready
    """

    METADATA_FILE = "session.json"
    LOG_FILE = "session.log"
    RECOVERY_FILE = "recovery.json"

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

        self._registry = SessionRegistry()

        self._root = (
            self._workspace.root /
            "sessions"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_sessions()

# ============================================================
# File: studio/session_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _session_id() -> str:

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

    def _load_existing_sessions(
        self,
    ) -> None:

        for item in self._root.iterdir():

            if not item.is_dir():
                continue

            metadata = (
                item /
                self.METADATA_FILE
            )

            if not metadata.exists():
                continue

            try:

                data = json.loads(
                    metadata.read_text(
                        encoding="utf-8",
                    )
                )

                session = SessionRecord(
                    metadata=SessionMetadata(
                        session_id=data["session_id"],
                        project_id=data["project_id"],
                        workspace_id=data["workspace_id"],
                        status=SessionStatus(
                            data["status"]
                        ),
                        created_at=data["created_at"],
                        updated_at=data["updated_at"],
                        last_activity=data["last_activity"],
                        user=data.get("user"),
                        custom=dict(
                            data.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    root=item,
                    state_file=(
                        item /
                        self.METADATA_FILE
                    ),
                    log_file=(
                        item /
                        self.LOG_FILE
                    ),
                    recovery_file=(
                        item /
                        self.RECOVERY_FILE
                    ),
                )

                self._registry.add(session)

            except Exception:
                continue

    def _save(
        self,
        session: SessionRecord,
    ) -> None:

        session.metadata.updated_at = (
            self._utc()
        )

        session.state_file.write_text(
            json.dumps(
                asdict(
                    session.metadata
                ),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create_session(
        self,
        *,
        project_id: str,
        user: str | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> SessionRecord:

        with self._lock:

            session_id = (
                self._session_id()
            )

            root = (
                self._root /
                session_id
            )

            root.mkdir(
                parents=True,
                exist_ok=True,
            )

            session = SessionRecord(
                metadata=SessionMetadata(
                    session_id=session_id,
                    project_id=project_id,
                    workspace_id=self._workspace.workspace_id,
                    status=SessionStatus.CREATED,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    last_activity=self._utc(),
                    user=user,
                    custom=dict(
                        custom or {}
                    ),
                ),
                root=root,
                state_file=(
                    root /
                    self.METADATA_FILE
                ),
                log_file=(
                    root /
                    self.LOG_FILE
                ),
                recovery_file=(
                    root /
                    self.RECOVERY_FILE
                ),
            )

            self._save(session)

            session.log_file.touch(
                exist_ok=True
            )

            session.recovery_file.write_text(
                "{}",
                encoding="utf-8",
            )

            self._registry.add(
                session
            )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.active_session",
                    session_id,
                )

            self._emit(
                "session.created",
                session_id=session_id,
                project_id=project_id,
            )

            return session
# ============================================================
# File: studio/session_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def start_session(
        self,
        session_id: str,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.status = SessionStatus.ACTIVE
            session.metadata.last_activity = self._utc()

            self._save(session)

            if self._shared_state is not None:
                self._shared_state.set(
                    "studio.active_session",
                    session_id,
                )

            self._emit(
                "session.started",
                session_id=session_id,
                project_id=session.metadata.project_id,
            )

            return session

    def pause_session(
        self,
        session_id: str,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.status = SessionStatus.PAUSED
            session.metadata.last_activity = self._utc()

            self._save(session)

            self._emit(
                "session.paused",
                session_id=session_id,
            )

            return session

    def resume_session(
        self,
        session_id: str,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.status = SessionStatus.ACTIVE
            session.metadata.last_activity = self._utc()

            self._save(session)

            self._emit(
                "session.resumed",
                session_id=session_id,
            )

            return session

    def close_session(
        self,
        session_id: str,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.status = SessionStatus.CLOSED
            session.metadata.last_activity = self._utc()

            self._save(session)

            if self._shared_state is not None:

                active = self._shared_state.get(
                    "studio.active_session"
                )

                if active == session_id:

                    self._shared_state.set(
                        "studio.active_session",
                        None,
                    )

            self._emit(
                "session.closed",
                session_id=session_id,
            )

            return session

    def mark_crashed(
        self,
        session_id: str,
        reason: str,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.status = SessionStatus.CRASHED
            session.metadata.last_activity = self._utc()

            self._save(session)

            session.recovery_file.write_text(
                json.dumps(
                    {
                        "reason": reason,
                        "timestamp": self._utc(),
                    },
                    indent=4,
                ),
                encoding="utf-8",
            )

            self._emit(
                "session.crashed",
                session_id=session_id,
                reason=reason,
            )

            return session
# ============================================================
# File: studio/session_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def append_log(
        self,
        session_id: str,
        message: str,
    ) -> None:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.last_activity = self._utc()

            self._save(session)

            timestamp = datetime.now(
                UTC
            ).isoformat()

            with session.log_file.open(
                "a",
                encoding="utf-8",
            ) as stream:

                stream.write(
                    f"[{timestamp}] {message}\n"
                )

    def update_custom_state(
        self,
        session_id: str,
        key: str,
        value: Any,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            session.metadata.custom[key] = value

            session.metadata.last_activity = (
                self._utc()
            )

            self._save(session)

            self._emit(
                "session.custom.updated",
                session_id=session_id,
                key=key,
            )

            return session

    def export_session(
        self,
        session_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            session = self._registry.get(session_id)

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    asdict(session.metadata),
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_session(
        self,
        session_id: str,
        source: Path,
    ) -> SessionRecord:

        with self._lock:

            session = self._registry.get(session_id)

            data = json.loads(
                source.read_text(
                    encoding="utf-8",
                )
            )

            session.metadata.custom = dict(
                data.get(
                    "custom",
                    {},
                )
            )

            session.metadata.user = data.get(
                "user"
            )

            session.metadata.last_activity = (
                self._utc()
            )

            self._save(session)

            self._emit(
                "session.imported",
                session_id=session_id,
            )

            return session

    def get_session(
        self,
        session_id: str,
    ) -> SessionRecord:

        return self._registry.get(
            session_id
        )

    def list_sessions(
        self,
    ) -> list[SessionRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
            item.metadata.created_at,
        )
# ============================================================
# File: studio/session_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def delete_session(
        self,
        session_id: str,
        *,
        remove_files: bool = False,
    ) -> None:

        with self._lock:

            session = self._registry.get(session_id)

            if remove_files:

                for child in session.root.rglob("*"):

                    if child.is_file():
                        child.unlink()

                for child in sorted(
                    session.root.rglob("*"),
                    reverse=True,
                ):
                    if child.is_dir():
                        child.rmdir()

                session.root.rmdir()

            self._registry.remove(session_id)

            if self._shared_state is not None:

                active = self._shared_state.get(
                    "studio.active_session"
                )

                if active == session_id:

                    self._shared_state.set(
                        "studio.active_session",
                        None,
                    )

            self._emit(
                "session.deleted",
                session_id=session_id,
            )

    def statistics(
        self,
    ) -> dict[str, Any]:

        sessions = self._registry.all()

        status: dict[str, int] = {}

        for session in sessions:

            key = session.metadata.status.value

            status[key] = (
                status.get(key, 0) + 1
            )

        return {
            "workspace_id": self._workspace.workspace_id,
            "session_count": len(sessions),
            "status": status,
            "runtime_connected": self._runtime is not None,
            "shared_state_connected": self._shared_state is not None,
            "event_bus_connected": self._event_bus is not None,
            "plugin_manager_connected": self._plugins is not None,
        }

    def health_check(
        self,
    ) -> dict[str, Any]:

        broken: list[str] = []

        for session in self._registry.all():

            if not session.root.exists():

                broken.append(
                    session.metadata.session_id
                )

        return {
            "healthy": not broken,
            "broken_sessions": broken,
            "registered_sessions": len(
                self._registry.all()
            ),
            "timestamp": time.time(),
        }

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for session in self._registry.all():

                self._save(session)

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.session_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "session_manager.synchronized",
                workspace=self._workspace.workspace_id,
            )

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "session_manager.shutdown",
                workspace=self._workspace.workspace_id,
            )

            self._registry.clear()
