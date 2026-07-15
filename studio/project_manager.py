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
from typing import Any, Callable, Iterable, Mapping, Protocol

# ============================================================
# StudioOS Enterprise Framework v1
# studio/project_manager.py
#
# Part 1
# ============================================================


class SupportsEventBus(Protocol):
    def publish(self, event: str, **payload: Any) -> None: ...


class SupportsSharedState(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...


class SupportsRuntime(Protocol):
    def is_running(self) -> bool: ...


class SupportsPluginManager(Protocol):
    def emit(self, hook: str, **kwargs: Any) -> None: ...


class SupportsWorkspace(Protocol):
    @property
    def root(self) -> Path: ...

    @property
    def workspace_id(self) -> str: ...


class ProjectStatus(str, Enum):
    CREATED = "created"
    READY = "ready"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass(slots=True)
class ProjectMetadata:

    project_id: str
    name: str
    description: str
    version: str
    tags: list[str]

    created_at: str
    updated_at: str

    status: ProjectStatus

    author: str | None = None

    custom: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProjectRecord:

    metadata: ProjectMetadata

    root: Path

    config_path: Path

    assets_path: Path

    source_path: Path

    output_path: Path

    cache_path: Path

    temp_path: Path

    logs_path: Path


class ProjectException(Exception):
    pass


class ProjectAlreadyExists(ProjectException):
    pass


class ProjectNotFound(ProjectException):
    pass


class InvalidProject(ProjectException):
    pass


class ProjectRegistry:

    """
    Enterprise Thread-safe Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._projects: dict[str, ProjectRecord] = {}

        self._name_index: dict[str, str] = {}

    def add(self, record: ProjectRecord) -> None:

        with self._lock:

            if record.metadata.project_id in self._projects:
                raise ProjectAlreadyExists(record.metadata.project_id)

            if record.metadata.name in self._name_index:
                raise ProjectAlreadyExists(record.metadata.name)

            self._projects[record.metadata.project_id] = record
            self._name_index[record.metadata.name] = record.metadata.project_id

    def remove(self, project_id: str) -> None:

        with self._lock:

            record = self._projects.pop(project_id)

            self._name_index.pop(record.metadata.name, None)

    def get(self, project_id: str) -> ProjectRecord:

        with self._lock:

            try:
                return self._projects[project_id]
            except KeyError as exc:
                raise ProjectNotFound(project_id) from exc

    def get_by_name(self, name: str) -> ProjectRecord:

        with self._lock:

            pid = self._name_index.get(name)

            if pid is None:
                raise ProjectNotFound(name)

            return self._projects[pid]

    def exists(self, name: str) -> bool:

        with self._lock:
            return name in self._name_index

    def all(self) -> list[ProjectRecord]:

        with self._lock:
            return list(self._projects.values())

    def clear(self) -> None:

        with self._lock:

            self._projects.clear()

            self._name_index.clear()


class ProjectManager:

    """
    Enterprise Project Manager

    Integrates with:

    Workspace
    EventBus
    Runtime
    SharedState
    PluginManager

    Enterprise Upgrade Ready
    """

    METADATA_FILE = "project.json"

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

        self._registry = ProjectRegistry()

        self._projects_root = self._workspace.root / "projects"

        self._projects_root.mkdir(parents=True, exist_ok=True)

        self._load_existing_projects()

    @staticmethod
    def _utc() -> str:

        return datetime.now(UTC).isoformat()

    @staticmethod
    def _project_id() -> str:

        return uuid.uuid4().hex

    def _emit(self, event: str, **payload: Any) -> None:

        if self._event_bus is not None:
            self._event_bus.publish(event, **payload)

        if self._plugins is not None:
            self._plugins.emit(event, **payload)

    def _load_existing_projects(self) -> None:

        for item in self._projects_root.iterdir():

            if not item.is_dir():
                continue

            meta = item / self.METADATA_FILE

            if not meta.exists():
                continue

            try:
                record = self._load_project_record(item)
                self._registry.add(record)
            except Exception:
                continue

    def _load_project_record(self, project_root: Path) -> ProjectRecord:

        metadata_file = project_root / self.METADATA_FILE

        try:
            metadata_dict = json.loads(
                metadata_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as exc:
            raise InvalidProject(
                f"Invalid metadata: {project_root}"
            ) from exc

        metadata = ProjectMetadata(
            project_id=metadata_dict["project_id"],
            name=metadata_dict["name"],
            description=metadata_dict.get("description", ""),
            version=metadata_dict.get("version", "1.0.0"),
            tags=list(metadata_dict.get("tags", [])),
            created_at=metadata_dict["created_at"],
            updated_at=metadata_dict["updated_at"],
            status=ProjectStatus(metadata_dict["status"]),
            author=metadata_dict.get("author"),
            custom=dict(metadata_dict.get("custom", {})),
        )

        return ProjectRecord(
            metadata=metadata,
            root=project_root,
            config_path=project_root / "config",
            assets_path=project_root / "assets",
            source_path=project_root / "src",
            output_path=project_root / "output",
            cache_path=project_root / ".cache",
            temp_path=project_root / ".temp",
            logs_path=project_root / "logs",
        )

    def _write_metadata(
        self,
        record: ProjectRecord,
    ) -> None:

        record.metadata.updated_at = self._utc()

        metadata_path = (
            record.root /
            self.METADATA_FILE
        )

        metadata_path.write_text(
            json.dumps(
                asdict(record.metadata),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def _create_structure(
        self,
        root: Path,
    ) -> None:

        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "assets").mkdir(parents=True, exist_ok=True)
        (root / "config").mkdir(parents=True, exist_ok=True)
        (root / "output").mkdir(parents=True, exist_ok=True)
        (root / ".cache").mkdir(parents=True, exist_ok=True)
        (root / ".temp").mkdir(parents=True, exist_ok=True)
        (root / "logs").mkdir(parents=True, exist_ok=True)

    def create_project(
        self,
        *,
        name: str,
        description: str = "",
        version: str = "1.0.0",
        author: str | None = None,
        tags: Iterable[str] = (),
        custom: Mapping[str, Any] | None = None,
    ) -> ProjectRecord:

        with self._lock:

            if self._registry.exists(name):
                raise ProjectAlreadyExists(name)

            root = self._projects_root / name

            if root.exists():
                raise ProjectAlreadyExists(name)

            self._create_structure(root)

            metadata = ProjectMetadata(
                project_id=self._project_id(),
                name=name,
                description=description,
                version=version,
                tags=list(tags),
                created_at=self._utc(),
                updated_at=self._utc(),
                status=ProjectStatus.CREATED,
                author=author,
                custom=dict(custom or {}),
            )

            record = ProjectRecord(
                metadata=metadata,
                root=root,
                config_path=root / "config",
                assets_path=root / "assets",
                source_path=root / "src",
                output_path=root / "output",
                cache_path=root / ".cache",
                temp_path=root / ".temp",
                logs_path=root / "logs",
            )

            self._write_metadata(record)

            self._registry.add(record)

            if self._shared_state is not None:
                self._shared_state.set(
                    f"project:{metadata.project_id}",
                    metadata.name,
                )

            self._emit(
                "project.created",
                project_id=metadata.project_id,
                name=metadata.name,
                workspace=self._workspace.workspace_id,
            )

            return record
        
# ============================================================
# File: studio/project_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def open_project(
        self,
        project_id: str,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            record.metadata.status = ProjectStatus.ACTIVE

            self._write_metadata(record)

            if self._shared_state is not None:
                self._shared_state.set(
                    "studio.active_project",
                    record.metadata.project_id,
                )

            self._emit(
                "project.opened",
                project_id=record.metadata.project_id,
                name=record.metadata.name,
            )

            return record

    def close_project(
        self,
        project_id: str,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            record.metadata.status = ProjectStatus.READY

            self._write_metadata(record)

            if self._shared_state is not None:
                active = self._shared_state.get("studio.active_project")

                if active == project_id:
                    self._shared_state.set(
                        "studio.active_project",
                        None,
                    )

            self._emit(
                "project.closed",
                project_id=record.metadata.project_id,
                name=record.metadata.name,
            )

            return record

    def rename_project(
        self,
        project_id: str,
        new_name: str,
    ) -> ProjectRecord:

        with self._lock:

            if self._registry.exists(new_name):
                raise ProjectAlreadyExists(new_name)

            record = self._registry.get(project_id)

            old_root = record.root
            new_root = self._projects_root / new_name

            old_root.rename(new_root)

            self._registry.remove(project_id)

            record.root = new_root
            record.metadata.name = new_name

            record.config_path = new_root / "config"
            record.assets_path = new_root / "assets"
            record.source_path = new_root / "src"
            record.output_path = new_root / "output"
            record.cache_path = new_root / ".cache"
            record.temp_path = new_root / ".temp"
            record.logs_path = new_root / "logs"

            self._write_metadata(record)

            self._registry.add(record)

            self._emit(
                "project.renamed",
                project_id=record.metadata.project_id,
                name=new_name,
            )

            return record

    def archive_project(
        self,
        project_id: str,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            record.metadata.status = ProjectStatus.ARCHIVED

            self._write_metadata(record)

            self._emit(
                "project.archived",
                project_id=record.metadata.project_id,
            )

            return record

    def restore_project(
        self,
        project_id: str,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            record.metadata.status = ProjectStatus.READY

            self._write_metadata(record)

            self._emit(
                "project.restored",
                project_id=record.metadata.project_id,
            )

            return record
        
# ============================================================
# File: studio/project_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def clone_project(
        self,
        project_id: str,
        new_name: str,
    ) -> ProjectRecord:

        with self._lock:

            source = self._registry.get(project_id)

            if self._registry.exists(new_name):
                raise ProjectAlreadyExists(new_name)

            destination = self._projects_root / new_name

            shutil.copytree(
                source.root,
                destination,
            )

            record = self._load_project_record(destination)

            record.metadata.project_id = self._project_id()
            record.metadata.name = new_name
            record.metadata.status = ProjectStatus.CREATED
            record.metadata.created_at = self._utc()
            record.metadata.updated_at = self._utc()

            self._write_metadata(record)

            self._registry.add(record)

            self._emit(
                "project.cloned",
                source_project=project_id,
                project_id=record.metadata.project_id,
            )

            return record

    def delete_project(
        self,
        project_id: str,
        *,
        permanent: bool = False,
    ) -> None:

        with self._lock:

            record = self._registry.get(project_id)

            if permanent:

                shutil.rmtree(
                    record.root,
                    ignore_errors=False,
                )

            else:

                trash = (
                    self._projects_root /
                    ".trash"
                )

                trash.mkdir(
                    exist_ok=True,
                    parents=True,
                )

                shutil.move(
                    str(record.root),
                    str(
                        trash /
                        record.root.name
                    ),
                )

            self._registry.remove(project_id)

            self._emit(
                "project.deleted",
                project_id=project_id,
                permanent=permanent,
            )

    def update_metadata(
        self,
        project_id: str,
        **changes: Any,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            for key, value in changes.items():

                if hasattr(record.metadata, key):
                    setattr(
                        record.metadata,
                        key,
                        value,
                    )

            self._write_metadata(record)

            self._emit(
                "project.updated",
                project_id=project_id,
            )

            return record

    def get_project(
        self,
        project_id: str,
    ) -> ProjectRecord:

        return self._registry.get(project_id)

    def get_project_by_name(
        self,
        name: str,
    ) -> ProjectRecord:

        return self._registry.get_by_name(name)

    def list_projects(
        self,
    ) -> list[ProjectRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def project_exists(
        self,
        name: str,
    ) -> bool:

        return self._registry.exists(name)

    def count(self) -> int:

        return len(
            self._registry.all()
        )
    
# ============================================================
# File: studio/project_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def statistics(self) -> dict[str, Any]:

        projects = self._registry.all()

        status_counter: dict[str, int] = {}

        for record in projects:

            key = record.metadata.status.value

            status_counter[key] = (
                status_counter.get(key, 0) + 1
            )

        return {
            "workspace_id": self._workspace.workspace_id,
            "project_count": len(projects),
            "status": status_counter,
            "runtime_connected": self._runtime is not None,
            "event_bus_connected": self._event_bus is not None,
            "shared_state_connected": self._shared_state is not None,
            "plugin_manager_connected": self._plugins is not None,
        }

    def export_metadata(
        self,
        project_id: str,
        destination: Path,
    ) -> Path:

        with self._lock:

            record = self._registry.get(project_id)

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_text(
                json.dumps(
                    asdict(record.metadata),
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            return destination

    def import_metadata(
        self,
        project_id: str,
        metadata_file: Path,
    ) -> ProjectRecord:

        with self._lock:

            record = self._registry.get(project_id)

            data = json.loads(
                metadata_file.read_text(
                    encoding="utf-8",
                )
            )

            data["project_id"] = record.metadata.project_id
            data["name"] = record.metadata.name

            record.metadata = ProjectMetadata(
                project_id=data["project_id"],
                name=data["name"],
                description=data.get("description", ""),
                version=data.get("version", "1.0.0"),
                tags=list(data.get("tags", [])),
                created_at=data["created_at"],
                updated_at=self._utc(),
                status=ProjectStatus(
                    data["status"]
                ),
                author=data.get("author"),
                custom=dict(
                    data.get("custom", {})
                ),
            )

            self._write_metadata(record)

            self._emit(
                "project.metadata.imported",
                project_id=project_id,
            )

            return record

    def synchronize(self) -> None:

        with self._lock:

            for record in self._registry.all():

                self._write_metadata(record)

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.project_count",
                    self.count(),
                )

            self._emit(
                "project_manager.synchronized",
                workspace=self._workspace.workspace_id,
            )

    def health_check(self) -> dict[str, Any]:

        missing: list[str] = []

        for record in self._registry.all():

            if not record.root.exists():
                missing.append(record.metadata.name)

        return {
            "healthy": not missing,
            "missing_projects": missing,
            "registered_projects": self.count(),
            "timestamp": time.time(),
        }

    def shutdown(self) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "project_manager.shutdown",
                workspace=self._workspace.workspace_id,
            )

            self._registry.clear()
