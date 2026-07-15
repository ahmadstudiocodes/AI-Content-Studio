"""
Arman StudioOS
Enterprise Workspace Framework

File:
    studio/workspace.py

Description:
    Enterprise Workspace Management System

Python:
    3.12+
"""


from __future__ import annotations


import copy
import json
import logging
import shutil
import socket
import threading
import uuid


from contextlib import contextmanager

from dataclasses import (
    asdict,
    dataclass,
    field,
)

from datetime import (
    UTC,
    datetime,
)

from enum import Enum

from pathlib import Path

from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
)



try:

    from brain.event_bus import event_bus

except Exception:

    event_bus = None



logger = logging.getLogger(
    "studio.workspace"
)



# ==========================================================
# Exceptions
# ==========================================================


class WorkspaceError(Exception):
    """
    Base Workspace Exception.
    """


class WorkspaceExistsError(
    WorkspaceError
):
    pass


class WorkspaceNotFoundError(
    WorkspaceError
):
    pass


class WorkspaceValidationError(
    WorkspaceError
):
    pass


class WorkspaceLockedError(
    WorkspaceError
):
    pass


class WorkspacePersistenceError(
    WorkspaceError
):
    pass


class WorkspaceTransactionError(
    WorkspaceError
):
    pass



# ==========================================================
# Workspace Status
# ==========================================================


class WorkspaceStatus(
    str,
    Enum,
):

    CREATED = "created"

    OPEN = "open"

    CLOSED = "closed"

    ARCHIVED = "archived"

    DELETED = "deleted"

    BROKEN = "broken"



# ==========================================================
# Workspace Metadata
# ==========================================================


@dataclass(slots=True)
class WorkspaceMetadata:
    """
    Enterprise workspace metadata.
    """


    workspace_id: str


    name: str


    root: str


    description: str = ""


    owner: str = "local"


    version: str = "1.0"


    tags: List[str] = field(
        default_factory=list
    )


    created_at: str = field(
        default_factory=lambda:
        datetime.now(
            UTC
        ).isoformat()
    )


    updated_at: str = field(
        default_factory=lambda:
        datetime.now(
            UTC
        ).isoformat()
    )


    status: WorkspaceStatus = (
        WorkspaceStatus.CREATED
    )



    def touch(
        self,
    ) -> None:
        """
        Update modification timestamp.
        """

        self.updated_at = (
            datetime.now(
                UTC
            ).isoformat()
        )

# ==========================================================
# Workspace Config
# ==========================================================


@dataclass(slots=True)
class WorkspaceConfig:
    """
    Workspace runtime configuration.
    """


    autosave: bool = True


    autosave_interval: int = 300


    backup_enabled: bool = True


    snapshot_enabled: bool = True


    compression: bool = False


    readonly: bool = False


    values: Dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )



    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.values.get(
            key,
            default,
        )



    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.values[
            key
        ] = value



    def remove(
        self,
        key: str,
    ) -> None:

        self.values.pop(
            key,
            None,
        )



# ==========================================================
# Workspace Session
# ==========================================================


@dataclass(slots=True)
class WorkspaceSession:
    """
    Active workspace session.
    """


    session_id: str = field(
        default_factory=lambda:
        str(
            uuid.uuid4()
        )
    )


    opened_at: str = field(
        default_factory=lambda:
        datetime.now(
            UTC
        ).isoformat()
    )


    user: str = "local"



    machine: str = field(
        default_factory=socket.gethostname
    )



    data: Dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )



    active: bool = True



    def close(
        self,
    ) -> None:

        self.active = False



    def update(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.data[
            key
        ] = value



# ==========================================================
# Workspace Core Object
# ==========================================================


class Workspace:
    """
    Enterprise Workspace Object.

    Owns:

        Metadata
        Configuration
        Projects
        Assets
        Services
        Extensions
        Runtime
        Sessions
        History
        Snapshots
        Metrics
    """



    def __init__(

        self,

        metadata: WorkspaceMetadata,

        config: WorkspaceConfig | None = None,

    ) -> None:


        self._lock = (
            threading.RLock()
        )



        self.metadata = metadata



        self.config = (
            config
            or WorkspaceConfig()
        )



        self.session = (
            WorkspaceSession()
        )



        self.projects: Dict[
            str,
            Any,
        ] = {}



        self.assets: Dict[
            str,
            Any,
        ] = {}



        self.services: Dict[
            str,
            Any,
        ] = {}



        self.extensions: Dict[
            str,
            Any,
        ] = {}



        self.runtime: Dict[
            str,
            Any,
        ] = {}



        self.history: List[
            Dict[str, Any]
        ] = []



        self.snapshots: List[
            Dict[str, Any]
        ] = []



        self.statistics: Dict[
            str,
            Any,
        ] = {

            "opens": 0,

            "saves": 0,

            "backups": 0,

            "snapshots": 0,

        }



        self.health: Dict[
            str,
            Any,
        ] = {

            "healthy": True,

            "last_check": None,

            "errors": [],

            "warnings": [],

        }

# ==========================================================
# Workspace Properties
# ==========================================================


    @property
    def id(
        self,
    ) -> str:

        return self.metadata.workspace_id

    @property
    def workspace_id(
        self,
    ) -> str:
        """
        Backward compatibility alias.
        """

        return self.id

    @property
    def name(
        self,
    ) -> str:

        return self.metadata.name



    @property
    def root(
        self,
    ) -> Path:

        return Path(
            self.metadata.root
        )



    @property
    def status(
        self,
    ) -> WorkspaceStatus:

        return self.metadata.status



    @property
    def is_open(
        self,
    ) -> bool:

        return (
            self.status
            == WorkspaceStatus.OPEN
        )



    @property
    def is_closed(
        self,
    ) -> bool:

        return (
            self.status
            == WorkspaceStatus.CLOSED
        )



    @property
    def locked(
        self,
    ) -> bool:

        return (
            self.root
            /
            ".workspace.lock"
        ).exists()



# ==========================================================
# Workspace Lifecycle
# ==========================================================


    def open(
        self,
    ) -> None:
        """
        Open workspace.
        """


        with self._lock:


            self.root.mkdir(
                parents=True,
                exist_ok=True,
            )


            self.metadata.status = (
                WorkspaceStatus.OPEN
            )


            self.statistics[
                "opens"
            ] += 1


            self.metadata.touch()



            self.session = (
                WorkspaceSession()
            )



            self.add_history(
                "workspace.opened"
            )



    def close(
        self,
    ) -> None:
        """
        Close workspace.
        """


        with self._lock:


            if self.session:

                self.session.close()



            self.metadata.status = (
                WorkspaceStatus.CLOSED
            )


            self.metadata.touch()



            self.add_history(
                "workspace.closed"
            )



    def archive(
        self,
    ) -> None:
        """
        Archive workspace.
        """


        with self._lock:


            self.metadata.status = (
                WorkspaceStatus.ARCHIVED
            )


            self.metadata.touch()



            self.add_history(
                "workspace.archived"
            )



    def mark_broken(
        self,
        error: str,
    ) -> None:
        """
        Mark workspace as broken.
        """


        with self._lock:


            self.metadata.status = (
                WorkspaceStatus.BROKEN
            )


            self.health[
                "healthy"
            ] = False



            self.health[
                "errors"
            ].append(
                error
            )



            self.metadata.touch()



# ==========================================================
# Workspace History
# ==========================================================


    def add_history(
        self,
        event: str,
        **payload: Any,
    ) -> None:
        """
        Add workspace history event.
        """


        self.history.append(

            {

                "time":
                    datetime.now(
                        UTC
                    ).isoformat(),


                "event":
                    event,


                "payload":
                    payload,

            }

        )



# ==========================================================
# Workspace Runtime Binding
# ==========================================================


    def bind_runtime(
        self,
        runtime_id: str,
        **context: Any,
    ) -> None:
        """
        Bind runtime information.
        """


        self.runtime.update(

            {

                "runtime_id":
                    runtime_id,


                "context":
                    context,

            }

        )



        self.add_history(
            "runtime.bound",
            runtime_id=runtime_id,
        )

# ==========================================================
# Workspace Resource Registration
# ==========================================================


    def register_project(
        self,
        name: str,
        project: Any,
    ) -> None:
        """
        Register project resource.
        """

        with self._lock:

            self.projects[
                name
            ] = project


            self.add_history(
                "project.registered",
                name=name,
            )



    def unregister_project(
        self,
        name: str,
    ) -> None:
        """
        Remove project resource.
        """

        with self._lock:

            self.projects.pop(
                name,
                None,
            )


            self.add_history(
                "project.unregistered",
                name=name,
            )



    def register_asset(
        self,
        name: str,
        asset: Any,
    ) -> None:
        """
        Register asset resource.
        """

        with self._lock:

            self.assets[
                name
            ] = asset


            self.add_history(
                "asset.registered",
                name=name,
            )



    def unregister_asset(
        self,
        name: str,
    ) -> None:
        """
        Remove asset resource.
        """

        with self._lock:

            self.assets.pop(
                name,
                None,
            )


            self.add_history(
                "asset.unregistered",
                name=name,
            )



    def register_service(
        self,
        name: str,
        service: Any,
    ) -> None:
        """
        Register service.
        """

        with self._lock:

            self.services[
                name
            ] = service


            self.add_history(
                "service.registered",
                name=name,
            )



    def unregister_service(
        self,
        name: str,
    ) -> None:
        """
        Remove service.
        """

        with self._lock:

            self.services.pop(
                name,
                None,
            )


            self.add_history(
                "service.unregistered",
                name=name,
            )



    def register_extension(
        self,
        name: str,
        extension: Any,
    ) -> None:
        """
        Register extension/plugin.
        """

        with self._lock:

            self.extensions[
                name
            ] = extension


            self.add_history(
                "extension.registered",
                name=name,
            )



    def unregister_extension(
        self,
        name: str,
    ) -> None:
        """
        Remove extension.
        """

        with self._lock:

            self.extensions.pop(
                name,
                None,
            )


            self.add_history(
                "extension.unregistered",
                name=name,
            )



# ==========================================================
# Resource Lookup
# ==========================================================


    def has_project(
        self,
        name: str,
    ) -> bool:

        return (
            name
            in self.projects
        )



    def has_asset(
        self,
        name: str,
    ) -> bool:

        return (
            name
            in self.assets
        )



    def has_service(
        self,
        name: str,
    ) -> bool:

        return (
            name
            in self.services
        )



    def has_extension(
        self,
        name: str,
    ) -> bool:

        return (
            name
            in self.extensions
        )



    def resources_summary(
        self,
    ) -> Dict[str, int]:
        """
        Return resource statistics.
        """

        return {

            "projects":
                len(
                    self.projects
                ),


            "assets":
                len(
                    self.assets
                ),


            "services":
                len(
                    self.services
                ),


            "extensions":
                len(
                    self.extensions
                ),

        }
    
# ==========================================================
# Workspace Snapshot Engine
# ==========================================================


    def create_snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Create immutable workspace snapshot.
        """


        snapshot = {

            "created_at":
                datetime.now(
                    UTC
                ).isoformat(),


            "metadata":
                copy.deepcopy(
                    asdict(
                        self.metadata
                    )
                ),


            "config":
                copy.deepcopy(
                    asdict(
                        self.config
                    )
                ),


            "projects":
                list(
                    self.projects.keys()
                ),


            "assets":
                list(
                    self.assets.keys()
                ),


            "services":
                list(
                    self.services.keys()
                ),


            "extensions":
                list(
                    self.extensions.keys()
                ),


            "runtime":
                copy.deepcopy(
                    self.runtime
                ),


            "statistics":
                copy.deepcopy(
                    self.statistics
                ),

        }



        self.snapshots.append(
            snapshot
        )


        self.statistics[
            "snapshots"
        ] += 1



        self.add_history(
            "workspace.snapshot.created"
        )



        return snapshot



    def latest_snapshot(
        self,
    ) -> Dict[str, Any] | None:
        """
        Return latest snapshot.
        """


        if not self.snapshots:

            return None


        return self.snapshots[-1]



# ==========================================================
# Workspace Serialization
# ==========================================================


    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Convert workspace to serializable object.
        """


        return {


            "metadata":
                {

                    **asdict(
                        self.metadata
                    ),

                    "status":
                        self.status.value,

                },



            "config":
                asdict(
                    self.config
                ),



            "statistics":
                copy.deepcopy(
                    self.statistics
                ),



            "history":
                copy.deepcopy(
                    self.history
                ),



            "health":
                copy.deepcopy(
                    self.health
                ),



            "runtime":
                copy.deepcopy(
                    self.runtime
                ),



            "projects":
                list(
                    self.projects.keys()
                ),



            "assets":
                list(
                    self.assets.keys()
                ),



            "services":
                list(
                    self.services.keys()
                ),



            "extensions":
                list(
                    self.extensions.keys()
                ),


        }



    def restore_state(
        self,
        payload: Dict[str, Any],
    ) -> None:
        """
        Restore workspace runtime state.
        """


        metadata = payload.get(
            "metadata",
            {},
        )


        if "status" in metadata:

            metadata["status"] = (
                WorkspaceStatus(
                    metadata["status"]
                )
            )



        self.metadata = (
            WorkspaceMetadata(
                **metadata
            )
        )



        self.config = (
            WorkspaceConfig(
                **payload.get(
                    "config",
                    {},
                )
            )
        )



        self.statistics.update(

            payload.get(
                "statistics",
                {},
            )

        )



        self.history.extend(

            payload.get(
                "history",
                [],
            )

        )



        self.health.update(

            payload.get(
                "health",
                {},
            )

        )



        self.runtime.update(

            payload.get(
                "runtime",
                {},
            )

        )



        self.add_history(
            "workspace.state.restored"
        )

# ==========================================================
# Workspace Registry
# ==========================================================


class WorkspaceRegistry:
    """
    Enterprise Workspace Registry.

    Responsible for:

        - Register
        - Unregister
        - Lookup
        - Active Workspace
        - Enumeration
        - Thread Safety
    """



    def __init__(
        self,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self._workspaces: Dict[
            str,
            Workspace,
        ] = {}


        self._active_id: (
            str | None
        ) = None



# ==========================================================
# Register
# ==========================================================


    def register(
        self,
        workspace: Workspace,
    ) -> None:

        with self._lock:


            if workspace.id in self._workspaces:

                raise WorkspaceExistsError(
                    workspace.id
                )


            self._workspaces[
                workspace.id
            ] = workspace



            if self._active_id is None:

                self._active_id = (
                    workspace.id
                )



# ==========================================================
# Unregister
# ==========================================================


    def unregister(
        self,
        workspace_id: str,
    ) -> None:


        with self._lock:


            if workspace_id not in self._workspaces:

                raise WorkspaceNotFoundError(
                    workspace_id
                )


            del self._workspaces[
                workspace_id
            ]



            if self._active_id == workspace_id:

                self._active_id = None


                if self._workspaces:

                    self._active_id = next(
                        iter(
                            self._workspaces
                        )
                    )



# ==========================================================
# Lookup
# ==========================================================


    def get(
        self,
        workspace_id: str,
    ) -> Workspace:


        workspace = (
            self._workspaces.get(
                workspace_id
            )
        )


        if workspace is None:

            raise WorkspaceNotFoundError(
                workspace_id
            )


        return workspace



    def get_by_name(
        self,
        name: str,
    ) -> Workspace:


        for workspace in (
            self._workspaces.values()
        ):


            if workspace.name == name:

                return workspace



        raise WorkspaceNotFoundError(
            name
        )



    def exists(
        self,
        workspace_id: str,
    ) -> bool:


        return (
            workspace_id
            in self._workspaces
        )



    def contains_name(
        self,
        name: str,
    ) -> bool:


        return any(

            workspace.name == name

            for workspace
            in self._workspaces.values()

        )



# ==========================================================
# Active Workspace
# ==========================================================


    @property
    def active(
        self,
    ) -> Workspace | None:


        if self._active_id is None:

            return None


        return self._workspaces.get(
            self._active_id
        )



    def activate(
        self,
        workspace_id: str,
    ) -> Workspace:


        workspace = self.get(
            workspace_id
        )


        self._active_id = (
            workspace.id
        )


        return workspace



    def activate_by_name(
        self,
        name: str,
    ) -> Workspace:


        workspace = (
            self.get_by_name(
                name
            )
        )


        self._active_id = (
            workspace.id
        )


        return workspace



# ==========================================================
# Information
# ==========================================================


    def all(
        self,
    ) -> List[Workspace]:


        return list(
            self._workspaces.values()
        )



    def names(
        self,
    ) -> List[str]:


        return [

            workspace.name

            for workspace
            in self._workspaces.values()

        ]



    def ids(
        self,
    ) -> List[str]:


        return list(
            self._workspaces.keys()
        )



    def clear(
        self,
    ) -> None:


        with self._lock:

            self._workspaces.clear()

            self._active_id = None



    def __len__(
        self,
    ) -> int:

        return len(
            self._workspaces
        )



    def __contains__(
        self,
        workspace_id: str,
    ) -> bool:


        return (
            workspace_id
            in self._workspaces
        )



    def __iter__(
        self,
    ) -> Iterator[Workspace]:


        return iter(
            self._workspaces.values()
        )



# ==========================================================
# Global Workspace Registry
# ==========================================================


workspace_registry = (
    WorkspaceRegistry()
)

# ==========================================================
# Workspace Persistence Engine
# ==========================================================


class WorkspacePersistence:
    """
    Enterprise Workspace Persistence.

    Responsible for:

        - Save
        - Load
        - Delete
        - Backup
        - Restore
        - Snapshot Storage
    """



    WORKSPACE_FILE = (
        "workspace.json"
    )


    BACKUP_FOLDER = (
        "backups"
    )


    SNAPSHOT_FOLDER = (
        "snapshots"
    )



# ==========================================================
# Save
# ==========================================================


    @classmethod
    def save(
        cls,
        workspace: Workspace,
    ) -> None:


        try:


            workspace.root.mkdir(
                parents=True,
                exist_ok=True,
            )


            path = (
                workspace.root
                /
                cls.WORKSPACE_FILE
            )



            payload = (
                workspace.to_dict()
            )



            with path.open(
                "w",
                encoding="utf-8",
            ) as fp:


                json.dump(

                    payload,

                    fp,

                    indent=4,

                    ensure_ascii=False,

                )



            workspace.statistics[
                "saves"
            ] += 1



            workspace.metadata.touch()



            workspace.add_history(
                "workspace.saved"
            )



        except Exception as exc:


            raise WorkspacePersistenceError(
                str(exc)
            )



# ==========================================================
# Load
# ==========================================================


    @classmethod
    def load(
        cls,
        root: Path,
    ) -> Workspace:


        path = (
            root
            /
            cls.WORKSPACE_FILE
        )



        if not path.exists():


            raise WorkspaceNotFoundError(
                str(path)
            )



        try:


            with path.open(
                "r",
                encoding="utf-8",
            ) as fp:


                payload = json.load(
                    fp
                )



            metadata_data = payload[
                "metadata"
            ]



            if "status" in metadata_data:


                metadata_data[
                    "status"
                ] = WorkspaceStatus(

                    metadata_data[
                        "status"
                    ]

                )



            metadata = (
                WorkspaceMetadata(
                    **metadata_data
                )
            )



            config = (
                WorkspaceConfig(
                    **payload.get(
                        "config",
                        {},
                    )
                )
            )



            workspace = Workspace(

                metadata=metadata,

                config=config,

            )



            workspace.statistics.update(

                payload.get(
                    "statistics",
                    {},
                )

            )



            workspace.history.extend(

                payload.get(
                    "history",
                    [],
                )

            )



            workspace.health.update(

                payload.get(
                    "health",
                    {},
                )

            )



            workspace.runtime.update(

                payload.get(
                    "runtime",
                    {},
                )

            )



            return workspace



        except Exception as exc:


            raise WorkspacePersistenceError(
                str(exc)
            )



# ==========================================================
# Delete
# ==========================================================


    @classmethod
    def delete(
        cls,
        workspace: Workspace,
    ) -> None:


        try:


            if workspace.root.exists():


                shutil.rmtree(
                    workspace.root
                )



            workspace.metadata.status = (
                WorkspaceStatus.DELETED
            )



        except Exception as exc:


            raise WorkspacePersistenceError(
                str(exc)
            )



# ==========================================================
# Backup
# ==========================================================


    @classmethod
    def backup(
        cls,
        workspace: Workspace,
    ) -> Path:


        backup_root = (

            workspace.root
            /
            cls.BACKUP_FOLDER

        )



        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )



        filename = (

            datetime.now(
                UTC
            ).strftime(
                "%Y%m%d_%H%M%S"
            )

            +

            ".json"

        )



        backup_path = (
            backup_root
            /
            filename
        )



        with backup_path.open(
            "w",
            encoding="utf-8",
        ) as fp:


            json.dump(

                workspace.to_dict(),

                fp,

                indent=4,

                ensure_ascii=False,

            )



        workspace.statistics[
            "backups"
        ] += 1



        workspace.add_history(
            "workspace.backup.created",
            file=str(
                backup_path
            ),
        )



        return backup_path
    
# ==========================================================
# Workspace Persistence Restore
# ==========================================================


    @classmethod
    def restore_backup(
        cls,
        backup: Path,
    ) -> Workspace:
        """
        Restore workspace from backup file.
        """


        if not backup.exists():

            raise WorkspaceNotFoundError(
                str(backup)
            )



        try:


            with backup.open(
                "r",
                encoding="utf-8",
            ) as fp:


                payload = json.load(
                    fp
                )



            metadata_data = payload[
                "metadata"
            ]



            if "status" in metadata_data:


                metadata_data[
                    "status"
                ] = WorkspaceStatus(

                    metadata_data[
                        "status"
                    ]

                )



            metadata = (
                WorkspaceMetadata(
                    **metadata_data
                )
            )



            config = (
                WorkspaceConfig(
                    **payload.get(
                        "config",
                        {},
                    )
                )
            )



            workspace = Workspace(

                metadata=metadata,

                config=config,

            )



            workspace.statistics.update(

                payload.get(
                    "statistics",
                    {},
                )

            )



            workspace.history.extend(

                payload.get(
                    "history",
                    [],
                )

            )



            workspace.health.update(

                payload.get(
                    "health",
                    {},
                )

            )



            workspace.runtime.update(

                payload.get(
                    "runtime",
                    {},
                )

            )



            workspace.add_history(
                "workspace.restored"
            )



            return workspace



        except Exception as exc:


            raise WorkspacePersistenceError(
                str(exc)
            )



# ==========================================================
# Snapshot Persistence
# ==========================================================


    @classmethod
    def save_snapshot(
        cls,
        workspace: Workspace,
    ) -> Path:
        """
        Persist workspace snapshot.
        """


        snapshot_root = (

            workspace.root
            /
            cls.SNAPSHOT_FOLDER

        )



        snapshot_root.mkdir(
            parents=True,
            exist_ok=True,
        )



        filename = (

            datetime.now(
                UTC
            ).strftime(
                "%Y%m%d_%H%M%S"
            )

            +

            ".json"

        )



        path = (
            snapshot_root
            /
            filename
        )



        snapshot = (
            workspace.create_snapshot()
        )



        with path.open(
            "w",
            encoding="utf-8",
        ) as fp:


            json.dump(

                snapshot,

                fp,

                indent=4,

                ensure_ascii=False,

            )



        return path



# ==========================================================
# Workspace Validator
# ==========================================================


class WorkspaceValidator:
    """
    Enterprise Workspace Validation.
    """



    INVALID_NAMES = {

        "",

        ".",

        "..",

    }



    @classmethod
    def validate_name(
        cls,
        name: str,
    ) -> None:


        if (

            not name

            or

            name.strip()
            in cls.INVALID_NAMES

        ):


            raise WorkspaceValidationError(
                "Invalid workspace name"
            )



    @classmethod
    def validate_root(
        cls,
        root: Path,
    ) -> None:


        if not isinstance(
            root,
            Path,
        ):


            raise WorkspaceValidationError(
                "Workspace root must be Path"
            )



    @classmethod
    def validate(
        cls,
        name: str,
        root: Path,
    ) -> None:


        cls.validate_name(
            name
        )


        cls.validate_root(
            root
        )



# ==========================================================
# Workspace Manager
# ==========================================================


class WorkspaceManager:
    """
    Main Workspace Control Layer.
    """



    def __init__(
        self,
        registry: WorkspaceRegistry | None = None,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self._registry = (

            registry

            or

            workspace_registry

        )

# ==========================================================
# Workspace Manager - Create / Open / Save
# ==========================================================


    def create(
        self,
        name: str,
        root: Path,
        description: str = "",
        owner: str = "local",
    ) -> Workspace:
        """
        Create new workspace.
        """


        WorkspaceValidator.validate(
            name,
            root,
        )



        with self._lock:


            if self._registry.contains_name(
                name
            ):


                raise WorkspaceExistsError(
                    name
                )



            metadata = WorkspaceMetadata(

                workspace_id=str(
                    uuid.uuid4()
                ),

                name=name,

                root=str(
                    root
                ),

                description=description,

                owner=owner,

            )



            workspace = Workspace(
                metadata=metadata,
            )



            workspace.open()



            WorkspacePersistence.save(
                workspace
            )



            self._registry.register(
                workspace
            )



            workspace.add_history(
                "workspace.created"
            )



            logger.info(
                "Workspace created: %s",
                workspace.name,
            )



            if event_bus:


                try:


                    event_bus.publish(
                        "workspace.created",
                        workspace=workspace,
                    )


                except Exception:


                    logger.exception(
                        "Workspace event failed"
                    )



            return workspace



# ==========================================================
# Open Workspace
# ==========================================================


    def open(
        self,
        root: Path,
    ) -> Workspace:
        """
        Open existing workspace.
        """



        workspace = (
            WorkspacePersistence.load(
                root
            )
        )



        workspace.open()



        self._registry.register(
            workspace
        )



        workspace.add_history(
            "workspace.opened"
        )



        return workspace



# ==========================================================
# Save Workspace
# ==========================================================


    def save(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Save workspace.
        """



        WorkspacePersistence.save(
            workspace
        )



        logger.info(
            "Workspace saved: %s",
            workspace.name,
        )



        if event_bus:


            try:


                event_bus.publish(
                    "workspace.saved",
                    workspace=workspace,
                )


            except Exception:


                logger.exception(
                    "Workspace save event failed"
                )



    def save_all(
        self,
    ) -> None:
        """
        Save all registered workspaces.
        """



        for workspace in self._registry:


            self.save(
                workspace
            )



# ==========================================================
# Close Workspace
# ==========================================================


    def close(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Close workspace safely.
        """



        workspace.close()



        WorkspacePersistence.save(
            workspace
        )



        if event_bus:


            try:


                event_bus.publish(
                    "workspace.closed",
                    workspace=workspace,
                )


            except Exception:


                logger.exception(
                    "Workspace close event failed"
                )


# ==========================================================
# Workspace Manager - Delete / Archive / Backup / Restore
# ==========================================================


    def delete(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Delete workspace.
        """


        workspace.close()



        self._registry.unregister(
            workspace.id
        )



        WorkspacePersistence.delete(
            workspace
        )



        logger.info(
            "Workspace deleted: %s",
            workspace.name,
        )



        if event_bus:


            try:

                event_bus.publish(
                    "workspace.deleted",
                    workspace=workspace,
                )


            except Exception:

                logger.exception(
                    "Workspace delete event failed"
                )



    def archive(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Archive workspace.
        """


        workspace.archive()



        WorkspacePersistence.save(
            workspace
        )



        logger.info(
            "Workspace archived: %s",
            workspace.name,
        )



        if event_bus:


            try:

                event_bus.publish(
                    "workspace.archived",
                    workspace=workspace,
                )


            except Exception:

                logger.exception(
                    "Workspace archive event failed"
                )



    def backup(
        self,
        workspace: Workspace,
    ) -> Path:
        """
        Create workspace backup.
        """


        return (
            WorkspacePersistence.backup(
                workspace
            )
        )



    def restore_backup(
        self,
        backup: Path,
    ) -> Workspace:
        """
        Restore workspace from backup.
        """


        workspace = (
            WorkspacePersistence.restore_backup(
                backup
            )
        )



        self._registry.register(
            workspace
        )



        return workspace



# ==========================================================
# Workspace Clone
# ==========================================================


    def clone(
        self,
        workspace: Workspace,
        new_name: str,
        new_root: Path,
    ) -> Workspace:
        """
        Clone workspace.
        """



        WorkspaceValidator.validate(
            new_name,
            new_root,
        )



        cloned = self.create(

            name=new_name,

            root=new_root,

            description=
                workspace.metadata.description,

            owner=
                workspace.metadata.owner,

        )



        cloned.config = copy.deepcopy(
            workspace.config
        )


        cloned.projects = copy.deepcopy(
            workspace.projects
        )


        cloned.assets = copy.deepcopy(
            workspace.assets
        )


        cloned.services = copy.deepcopy(
            workspace.services
        )


        cloned.extensions = copy.deepcopy(
            workspace.extensions
        )


        WorkspacePersistence.save(
            cloned
        )



        cloned.add_history(
            "workspace.cloned",
            source=workspace.id,
        )



        return cloned



# ==========================================================
# Registry Helpers
# ==========================================================


    def get(
        self,
        workspace_id: str,
    ) -> Workspace:


        return self._registry.get(
            workspace_id
        )



    def get_by_name(
        self,
        name: str,
    ) -> Workspace:


        return self._registry.get_by_name(
            name
        )



    def active(
        self,
    ) -> Workspace | None:


        return self._registry.active



    def activate(
        self,
        workspace_id: str,
    ) -> Workspace:


        return self._registry.activate(
            workspace_id
        )



    def list(
        self,
    ) -> List[Workspace]:


        return self._registry.all()



    def exists(
        self,
        workspace_id: str,
    ) -> bool:


        return self._registry.exists(
            workspace_id
        )
    
# ==========================================================
# Workspace Manager - Health / Metrics / Search
# ==========================================================


    def health(
        self,
        workspace: Workspace,
    ) -> Dict[str, Any]:
        """
        Workspace health report.
        """


        report = {

            "healthy":
                True,


            "workspace":
                workspace.name,


            "status":
                workspace.status.value,


            "projects":
                len(
                    workspace.projects
                ),


            "assets":
                len(
                    workspace.assets
                ),


            "services":
                len(
                    workspace.services
                ),


            "extensions":
                len(
                    workspace.extensions
                ),


            "history":
                len(
                    workspace.history
                ),


            "snapshots":
                len(
                    workspace.snapshots
                ),


            "last_check":
                datetime.now(
                    UTC
                ).isoformat(),

        }



        workspace.health.update(
            report
        )



        return report



    def metrics(
        self,
        workspace: Workspace,
    ) -> Dict[str, Any]:
        """
        Workspace metrics.
        """


        return {


            "workspace_id":
                workspace.id,


            "name":
                workspace.name,


            "status":
                workspace.status.value,


            "statistics":
                copy.deepcopy(
                    workspace.statistics
                ),


            "projects":
                len(
                    workspace.projects
                ),


            "assets":
                len(
                    workspace.assets
                ),


            "services":
                len(
                    workspace.services
                ),


            "extensions":
                len(
                    workspace.extensions
                ),


            "snapshots":
                len(
                    workspace.snapshots
                ),

        }



    def search(
        self,
        keyword: str,
    ) -> List[Workspace]:
        """
        Search workspace by name.
        """


        keyword = keyword.lower()



        result = []



        for workspace in self._registry:


            if keyword in workspace.name.lower():

                result.append(
                    workspace
                )



        return result



# ==========================================================
# Transaction Manager
# ==========================================================


    @contextmanager
    def transaction(
        self,
        workspace: Workspace,
    ):
        """
        Safe workspace transaction.
        """


        backup = copy.deepcopy(
            workspace.to_dict()
        )



        try:


            workspace.add_history(
                "transaction.begin"
            )



            yield workspace



            WorkspacePersistence.save(
                workspace
            )



            workspace.add_history(
                "transaction.commit"
            )



        except Exception as exc:


            workspace.restore_state(
                backup
            )



            workspace.add_history(
                "transaction.rollback",
                error=str(exc),
            )



            raise WorkspaceTransactionError(
                str(exc)
            )



# ==========================================================
# Hook Manager
# ==========================================================


class WorkspaceHookManager:
    """
    Workspace lifecycle hooks.
    """



    def __init__(
        self,
    ) -> None:


        self._hooks: Dict[
            str,
            List[
                Callable[..., None]
            ]
        ] = {}



        self._lock = (
            threading.RLock()
        )



    def register(
        self,
        event: str,
        callback: Callable[..., None],
    ) -> None:


        with self._lock:


            self._hooks.setdefault(
                event,
                []
            ).append(
                callback
            )



    def emit(
        self,
        event: str,
        **payload: Any,
    ) -> None:


        callbacks = list(

            self._hooks.get(
                event,
                [],
            )

        )



        for callback in callbacks:


            try:

                callback(
                    **payload
                )


            except Exception:


                logger.exception(
                    "Workspace hook failed: %s",
                    event,
                )



# ==========================================================
# Global Services
# ==========================================================


workspace_hooks = (
    WorkspaceHookManager()
)



workspace_manager = (
    WorkspaceManager(
        workspace_registry
    )
)



# ==========================================================
# Public API
# ==========================================================


__all__ = [

    "Workspace",

    "WorkspaceConfig",

    "WorkspaceMetadata",

    "WorkspaceSession",

    "WorkspaceRegistry",

    "WorkspacePersistence",

    "WorkspaceValidator",

    "WorkspaceManager",

    "WorkspaceHookManager",

    "WorkspaceStatus",

    "WorkspaceError",

    "WorkspaceExistsError",

    "WorkspaceNotFoundError",

    "WorkspaceValidationError",

    "WorkspaceLockedError",

    "WorkspacePersistenceError",

    "WorkspaceTransactionError",

    "workspace_registry",

    "workspace_hooks",

    "workspace_manager",

]