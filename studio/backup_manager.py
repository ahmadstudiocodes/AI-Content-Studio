# ============================================================
# File: studio/backup_manager.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import hashlib
import json
import shutil
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

    def is_running(
        self,
    ) -> bool: ...


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


class BackupStatus(str, Enum):

    CREATED = "created"

    VERIFIED = "verified"

    RESTORED = "restored"

    FAILED = "failed"

    DELETED = "deleted"


@dataclass(slots=True)
class BackupMetadata:

    backup_id: str

    name: str

    created_at: str

    updated_at: str

    status: BackupStatus

    size: int

    checksum: str

    source: str

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class BackupRecord:

    metadata: BackupMetadata

    path: Path

    metadata_file: Path


class BackupError(Exception):
    pass


class BackupNotFound(BackupError):
    pass


class BackupRegistry:

    """
    Enterprise Thread Safe Backup Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._backups: dict[
            str,
            BackupRecord,
        ] = {}

    def add(
        self,
        backup: BackupRecord,
    ) -> None:

        with self._lock:

            self._backups[
                backup.metadata.backup_id
            ] = backup

    def get(
        self,
        backup_id: str,
    ) -> BackupRecord:

        with self._lock:

            try:

                return self._backups[
                    backup_id
                ]

            except KeyError as exc:

                raise BackupNotFound(
                    backup_id
                ) from exc

    def remove(
        self,
        backup_id: str,
    ) -> None:

        with self._lock:

            self._backups.pop(
                backup_id
            )

    def all(
        self,
    ) -> list[BackupRecord]:

        with self._lock:

            return list(
                self._backups.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._backups.clear()


class BackupManager:

    """
    StudioOS Enterprise Backup Manager

    Features:

    - Workspace Backup
    - Incremental Ready Architecture
    - Checksum Validation
    - Restore Support
    - Runtime Integration
    - Event Bus Integration
    - Shared State Integration
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    METADATA_FILE = "backup.json"

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

        self._registry = BackupRegistry()

        self._root = (
            self._workspace.root /
            "backups"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_backups()

# ============================================================
# File: studio/backup_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _backup_id() -> str:

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

    @staticmethod
    def _calculate_checksum(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open(
            "rb"
        ) as stream:

            while chunk := stream.read(
                1024 * 1024
            ):

                digest.update(
                    chunk
                )

        return digest.hexdigest()

    def _load_existing_backups(
        self,
    ) -> None:

        for metadata_file in self._root.rglob(
            self.METADATA_FILE
        ):

            try:

                data = json.loads(
                    metadata_file.read_text(
                        encoding="utf-8",
                    )
                )

                record = BackupRecord(
                    metadata=BackupMetadata(
                        backup_id=data[
                            "backup_id"
                        ],
                        name=data[
                            "name"
                        ],
                        created_at=data[
                            "created_at"
                        ],
                        updated_at=data[
                            "updated_at"
                        ],
                        status=BackupStatus(
                            data[
                                "status"
                            ]
                        ),
                        size=data[
                            "size"
                        ],
                        checksum=data[
                            "checksum"
                        ],
                        source=data[
                            "source"
                        ],
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
        backup: BackupRecord,
    ) -> None:

        backup.metadata.updated_at = (
            self._utc()
        )

        backup.metadata_file.write_text(
            json.dumps(
                asdict(
                    backup.metadata
                ),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create_backup(
        self,
        *,
        name: str,
        source: Path | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> BackupRecord:

        with self._lock:

            backup_id = (
                self._backup_id()
            )

            source_path = (
                source
                if source is not None
                else self._workspace.root
            )

            if not source_path.exists():

                raise FileNotFoundError(
                    source_path
                )

            destination = (
                self._root /
                backup_id
            )

            shutil.copytree(
                source_path,
                destination,
                dirs_exist_ok=True,
            )

            size = sum(
                item.stat().st_size
                for item
                in destination.rglob("*")
                if item.is_file()
            )

            checksum_file = (
                destination /
                "backup.checksum"
            )

            checksum_file.write_text(
                str(size),
                encoding="utf-8",
            )

            checksum = (
                self._calculate_checksum(
                    checksum_file
                )
            )

            record = BackupRecord(
                metadata=BackupMetadata(
                    backup_id=backup_id,
                    name=name,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=BackupStatus.CREATED,
                    size=size,
                    checksum=checksum,
                    source=str(
                        source_path
                    ),
                    custom=dict(
                        custom or {}
                    ),
                ),
                path=destination,
                metadata_file=(
                    destination /
                    self.METADATA_FILE
                ),
            )

            self._save_metadata(
                record
            )

            self._registry.add(
                record
            )

            self._emit(
                "backup.created",
                backup_id=backup_id,
                name=name,
            )

            return record
        
# ============================================================
# File: studio/backup_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get_backup(
        self,
        backup_id: str,
    ) -> BackupRecord:

        return self._registry.get(
            backup_id
        )

    def list_backups(
        self,
    ) -> list[BackupRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def verify_backup(
        self,
        backup_id: str,
    ) -> bool:

        with self._lock:

            backup = self._registry.get(
                backup_id
            )

            checksum_file = (
                backup.path /
                "backup.checksum"
            )

            if not checksum_file.exists():

                backup.metadata.status = (
                    BackupStatus.FAILED
                )

                self._save_metadata(
                    backup
                )

                return False

            checksum = (
                self._calculate_checksum(
                    checksum_file
                )
            )

            valid = (
                checksum
                ==
                backup.metadata.checksum
            )

            backup.metadata.status = (
                BackupStatus.VERIFIED
                if valid
                else BackupStatus.FAILED
            )

            self._save_metadata(
                backup
            )

            self._emit(
                "backup.verified",
                backup_id=backup_id,
                valid=valid,
            )

            return valid

    def restore_backup(
        self,
        backup_id: str,
        destination: Path | None = None,
    ) -> Path:

        with self._lock:

            backup = self._registry.get(
                backup_id
            )

            if not self.verify_backup(
                backup_id
            ):

                raise BackupError(
                    "Backup verification failed"
                )

            target = (
                destination
                if destination is not None
                else self._workspace.root
            )

            target.mkdir(
                parents=True,
                exist_ok=True,
            )

            for item in backup.path.iterdir():

                if item.name == self.METADATA_FILE:
                    continue

                if item.name == "backup.checksum":
                    continue

                destination_item = (
                    target /
                    item.name
                )

                if item.is_dir():

                    shutil.copytree(
                        item,
                        destination_item,
                        dirs_exist_ok=True,
                    )

                else:

                    shutil.copy2(
                        item,
                        destination_item,
                    )

            backup.metadata.status = (
                BackupStatus.RESTORED
            )

            self._save_metadata(
                backup
            )

            self._emit(
                "backup.restored",
                backup_id=backup_id,
                destination=str(target),
            )

            return target

    def delete_backup(
        self,
        backup_id: str,
    ) -> None:

        with self._lock:

            backup = self._registry.get(
                backup_id
            )

            if backup.path.exists():

                shutil.rmtree(
                    backup.path
                )

            backup.metadata.status = (
                BackupStatus.DELETED
            )

            self._registry.remove(
                backup_id
            )

            self._emit(
                "backup.deleted",
                backup_id=backup_id,
            )

    def cleanup(
        self,
        keep: int,
    ) -> int:

        with self._lock:

            backups = sorted(
                self._registry.all(),
                key=lambda item:
                    item.metadata.created_at,
                reverse=True,
            )

            removed = 0

            for backup in backups[keep:]:

                self.delete_backup(
                    backup.metadata.backup_id
                )

                removed += 1

            return removed
        
# ============================================================
# File: studio/backup_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def export_registry(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            data = [
                asdict(
                    backup.metadata
                )
                for backup in self._registry.all()
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

                backup_path = (
                    self._root /
                    item["backup_id"]
                )

                if not backup_path.exists():

                    continue

                record = BackupRecord(
                    metadata=BackupMetadata(
                        backup_id=item[
                            "backup_id"
                        ],
                        name=item[
                            "name"
                        ],
                        created_at=item[
                            "created_at"
                        ],
                        updated_at=item[
                            "updated_at"
                        ],
                        status=BackupStatus(
                            item["status"]
                        ),
                        size=item[
                            "size"
                        ],
                        checksum=item[
                            "checksum"
                        ],
                        source=item[
                            "source"
                        ],
                        custom=dict(
                            item.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    path=backup_path,
                    metadata_file=(
                        backup_path /
                        self.METADATA_FILE
                    ),
                )

                self._registry.add(
                    record
                )

                imported += 1

            self._emit(
                "backup.registry.imported",
                count=imported,
            )

            return imported

    def statistics(
        self,
    ) -> dict[str, Any]:

        backups = self._registry.all()

        total_size = sum(
            backup.metadata.size
            for backup in backups
        )

        statuses: dict[str, int] = {}

        for backup in backups:

            key = (
                backup.metadata.status.value
            )

            statuses[key] = (
                statuses.get(
                    key,
                    0,
                )
                + 1
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "backup_count":
                len(backups),
            "total_size":
                total_size,
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

        failed: list[str] = []

        for backup in self._registry.all():

            if (
                backup.metadata.status
                is BackupStatus.FAILED
            ):

                failed.append(
                    backup.metadata.backup_id
                )

        return {
            "healthy":
                not failed,
            "failed_backups":
                failed,
            "registered_backups":
                len(
                    self._registry.all()
                ),
            "timestamp":
                time.time(),
        }
    
# ============================================================
# File: studio/backup_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for backup in self._registry.all():

                self._save_metadata(
                    backup
                )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.backup_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "backup_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def create_incremental_backup(
        self,
        *,
        name: str,
        base_backup_id: str,
        source: Path | None = None,
    ) -> BackupRecord:

        with self._lock:

            base = self._registry.get(
                base_backup_id
            )

            source_path = (
                source
                if source is not None
                else self._workspace.root
            )

            if not source_path.exists():

                raise FileNotFoundError(
                    source_path
                )

            backup_id = (
                self._backup_id()
            )

            destination = (
                self._root /
                backup_id
            )

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            for item in source_path.rglob("*"):

                if not item.is_file():

                    continue

                relative = (
                    item.relative_to(
                        source_path
                    )
                )

                target = (
                    destination /
                    relative
                )

                previous = (
                    base.path /
                    relative
                )

                if (
                    not previous.exists()
                    or
                    self._calculate_checksum(
                        item
                    )
                    !=
                    self._calculate_checksum(
                        previous
                    )
                ):

                    target.parent.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                    shutil.copy2(
                        item,
                        target,
                    )

            size = sum(
                item.stat().st_size
                for item
                in destination.rglob("*")
                if item.is_file()
            )

            checksum_file = (
                destination /
                "backup.checksum"
            )

            checksum_file.write_text(
                str(size),
                encoding="utf-8",
            )

            record = BackupRecord(
                metadata=BackupMetadata(
                    backup_id=backup_id,
                    name=name,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=BackupStatus.CREATED,
                    size=size,
                    checksum=(
                        self._calculate_checksum(
                            checksum_file
                        )
                    ),
                    source=str(
                        source_path
                    ),
                    custom={
                        "base_backup":
                            base_backup_id,
                        "type":
                            "incremental",
                    },
                ),
                path=destination,
                metadata_file=(
                    destination /
                    self.METADATA_FILE
                ),
            )

            self._save_metadata(
                record
            )

            self._registry.add(
                record
            )

            self._emit(
                "backup.incremental.created",
                backup_id=backup_id,
                base_backup=base_backup_id,
            )

            return record

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "backup_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
