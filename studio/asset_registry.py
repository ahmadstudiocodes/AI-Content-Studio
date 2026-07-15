# ============================================================
# File: studio/asset_registry.py
# Part: 1
# Enterprise Framework v1
# ============================================================

from __future__ import annotations

import hashlib
import json
import mimetypes
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


class SupportsPluginManager(Protocol):

    def emit(
        self,
        hook: str,
        **kwargs: Any,
    ) -> None: ...


class AssetType(str, Enum):

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    MODEL = "model"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    SCRIPT = "script"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class AssetMetadata:

    asset_id: str

    name: str

    asset_type: AssetType

    mime_type: str

    checksum: str

    size: int

    relative_path: str

    created_at: str

    updated_at: str

    tags: list[str] = field(default_factory=list)

    custom: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AssetRecord:

    metadata: AssetMetadata

    path: Path

    metadata_file: Path


class AssetRegistryError(Exception):
    pass


class AssetAlreadyExists(AssetRegistryError):
    pass


class AssetNotFound(AssetRegistryError):
    pass


class AssetRegistryStore:

    """
    Enterprise Thread-Safe Asset Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._assets: dict[str, AssetRecord] = {}

    def add(
        self,
        record: AssetRecord,
    ) -> None:

        with self._lock:

            if record.metadata.asset_id in self._assets:
                raise AssetAlreadyExists(
                    record.metadata.asset_id
                )

            self._assets[
                record.metadata.asset_id
            ] = record

    def get(
        self,
        asset_id: str,
    ) -> AssetRecord:

        with self._lock:

            try:
                return self._assets[asset_id]

            except KeyError as exc:
                raise AssetNotFound(
                    asset_id
                ) from exc

    def remove(
        self,
        asset_id: str,
    ) -> None:

        with self._lock:

            self._assets.pop(asset_id)

    def all(
        self,
    ) -> list[AssetRecord]:

        with self._lock:

            return list(
                self._assets.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._assets.clear()


class AssetRegistry:

    """
    StudioOS Enterprise Asset Registry

    Workspace Integration
    Runtime Integration
    Event Bus Integration
    Shared State Integration
    Plugin Integration

    Enterprise Upgrade Ready
    """

    REGISTRY_FILE = "asset.json"

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

        self._store = AssetRegistryStore()

        self._root = (
            self._workspace.root /
            "assets"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_assets()

# ============================================================
# File: studio/asset_registry.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _asset_id() -> str:

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
    def _checksum(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open(
            "rb",
        ) as stream:

            while chunk := stream.read(1024 * 1024):

                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _detect_type(
        path: Path,
    ) -> tuple[AssetType, str]:

        mime, _ = mimetypes.guess_type(
            path.name
        )

        mime = mime or "application/octet-stream"

        if mime.startswith("image/"):
            return AssetType.IMAGE, mime

        if mime.startswith("video/"):
            return AssetType.VIDEO, mime

        if mime.startswith("audio/"):
            return AssetType.AUDIO, mime

        if mime.startswith("text/"):
            return AssetType.SCRIPT, mime

        if "zip" in mime:
            return AssetType.ARCHIVE, mime

        if "pdf" in mime:
            return AssetType.DOCUMENT, mime

        return AssetType.UNKNOWN, mime

    def _load_existing_assets(
        self,
    ) -> None:

        for metadata in self._root.rglob(
            self.REGISTRY_FILE
        ):

            try:

                data = json.loads(
                    metadata.read_text(
                        encoding="utf-8",
                    )
                )

                record = AssetRecord(
                    metadata=AssetMetadata(
                        asset_id=data["asset_id"],
                        name=data["name"],
                        asset_type=AssetType(
                            data["asset_type"]
                        ),
                        mime_type=data["mime_type"],
                        checksum=data["checksum"],
                        size=data["size"],
                        relative_path=data[
                            "relative_path"
                        ],
                        created_at=data[
                            "created_at"
                        ],
                        updated_at=data[
                            "updated_at"
                        ],
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
                    path=self._root
                    / data["relative_path"],
                    metadata_file=metadata,
                )

                self._store.add(
                    record
                )

            except Exception:
                continue

    def _save(
        self,
        record: AssetRecord,
    ) -> None:

        record.metadata.updated_at = (
            self._utc()
        )

        record.metadata_file.write_text(
            json.dumps(
                asdict(
                    record.metadata
                ),
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def register_asset(
        self,
        file: Path,
        *,
        tags: Iterable[str] = (),
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> AssetRecord:

        with self._lock:

            if not file.exists():
                raise FileNotFoundError(file)

            asset_type, mime = (
                self._detect_type(file)
            )

            asset_id = self._asset_id()

            metadata_file = (
                file.parent /
                self.REGISTRY_FILE
            )

            record = AssetRecord(
                metadata=AssetMetadata(
                    asset_id=asset_id,
                    name=file.name,
                    asset_type=asset_type,
                    mime_type=mime,
                    checksum=self._checksum(file),
                    size=file.stat().st_size,
                    relative_path=str(
                        file.relative_to(
                            self._root
                        )
                    ),
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    tags=list(tags),
                    custom=dict(
                        custom or {}
                    ),
                ),
                path=file,
                metadata_file=metadata_file,
            )

            self._save(record)

            self._store.add(record)

            self._emit(
                "asset.registered",
                asset_id=asset_id,
                path=str(file),
            )

            return record
        
# ============================================================
# File: studio/asset_registry.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def get_asset(
        self,
        asset_id: str,
    ) -> AssetRecord:

        return self._store.get(
            asset_id
        )

    def list_assets(
        self,
    ) -> list[AssetRecord]:

        return sorted(
            self._store.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def update_metadata(
        self,
        asset_id: str,
        *,
        tags: Iterable[str] | None = None,
        custom: Mapping[str, Any] | None = None,
    ) -> AssetRecord:

        with self._lock:

            record = self._store.get(
                asset_id
            )

            if tags is not None:
                record.metadata.tags = list(tags)

            if custom is not None:
                record.metadata.custom.update(
                    custom
                )

            self._save(record)

            self._emit(
                "asset.updated",
                asset_id=asset_id,
            )

            return record

    def refresh_asset(
        self,
        asset_id: str,
    ) -> AssetRecord:

        with self._lock:

            record = self._store.get(
                asset_id
            )

            if not record.path.exists():
                raise FileNotFoundError(
                    record.path
                )

            record.metadata.size = (
                record.path.stat().st_size
            )

            record.metadata.checksum = (
                self._checksum(
                    record.path
                )
            )

            asset_type, mime = (
                self._detect_type(
                    record.path
                )
            )

            record.metadata.asset_type = (
                asset_type
            )

            record.metadata.mime_type = (
                mime
            )

            self._save(record)

            self._emit(
                "asset.refreshed",
                asset_id=asset_id,
            )

            return record

    def remove_asset(
        self,
        asset_id: str,
        *,
        delete_file: bool = False,
    ) -> None:

        with self._lock:

            record = self._store.get(
                asset_id
            )

            if delete_file and record.path.exists():

                record.path.unlink()

            if record.metadata_file.exists():

                record.metadata_file.unlink()

            self._store.remove(
                asset_id
            )

            self._emit(
                "asset.removed",
                asset_id=asset_id,
            )

# ============================================================
# File: studio/asset_registry.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def find_by_tag(
        self,
        tag: str,
    ) -> list[AssetRecord]:

        return [
            asset
            for asset in self._store.all()
            if tag in asset.metadata.tags
        ]

    def find_by_type(
        self,
        asset_type: AssetType,
    ) -> list[AssetRecord]:

        return [
            asset
            for asset in self._store.all()
            if asset.metadata.asset_type
            is asset_type
        ]

    def find_by_name(
        self,
        keyword: str,
    ) -> list[AssetRecord]:

        keyword = keyword.lower()

        return [
            asset
            for asset in self._store.all()
            if keyword
            in asset.metadata.name.lower()
        ]

    def statistics(
        self,
    ) -> dict[str, Any]:

        assets = self._store.all()

        by_type: dict[str, int] = {}

        total_size = 0

        for asset in assets:

            key = asset.metadata.asset_type.value

            by_type[key] = (
                by_type.get(key, 0) + 1
            )

            total_size += asset.metadata.size

        return {
            "workspace_id": self._workspace.workspace_id,
            "asset_count": len(assets),
            "total_size": total_size,
            "asset_types": by_type,
            "runtime_connected": self._runtime is not None,
            "shared_state_connected": self._shared_state is not None,
            "event_bus_connected": self._event_bus is not None,
            "plugin_manager_connected": self._plugins is not None,
        }

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for asset in self._store.all():

                if asset.path.exists():

                    self.refresh_asset(
                        asset.metadata.asset_id
                    )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.asset_count",
                    len(
                        self._store.all()
                    ),
                )

            self._emit(
                "asset_registry.synchronized",
                workspace=self._workspace.workspace_id,
            )

    def health_check(
        self,
    ) -> dict[str, Any]:

        missing: list[str] = []

        for asset in self._store.all():

            if not asset.path.exists():

                missing.append(
                    asset.metadata.asset_id
                )

        return {
            "healthy": not missing,
            "missing_assets": missing,
            "registered_assets": len(
                self._store.all()
            ),
            "timestamp": time.time(),
        }
    
# ============================================================
# File: studio/asset_registry.py
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
                    asset.metadata
                )
                for asset in self._store.all()
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

                path = (
                    self._root /
                    item["relative_path"]
                )

                if not path.exists():

                    continue

                record = AssetRecord(
                    metadata=AssetMetadata(
                        asset_id=item["asset_id"],
                        name=item["name"],
                        asset_type=AssetType(
                            item["asset_type"]
                        ),
                        mime_type=item["mime_type"],
                        checksum=item["checksum"],
                        size=item["size"],
                        relative_path=item[
                            "relative_path"
                        ],
                        created_at=item[
                            "created_at"
                        ],
                        updated_at=item[
                            "updated_at"
                        ],
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
                    path=path,
                    metadata_file=(
                        path.parent /
                        self.REGISTRY_FILE
                    ),
                )

                try:

                    self._store.add(
                        record
                    )

                    imported += 1

                except AssetAlreadyExists:

                    continue

            self._emit(
                "asset.registry.imported",
                count=imported,
            )

            return imported

    def clone_asset(
        self,
        asset_id: str,
        destination: Path,
    ) -> AssetRecord:

        with self._lock:

            source = self._store.get(
                asset_id
            )

            if not source.path.exists():

                raise FileNotFoundError(
                    source.path
                )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination.write_bytes(
                source.path.read_bytes()
            )

            cloned = self.register_asset(
                destination,
                tags=source.metadata.tags,
                custom=source.metadata.custom,
            )

            self._emit(
                "asset.cloned",
                source_asset=asset_id,
                asset_id=cloned.metadata.asset_id,
            )

            return cloned

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "asset_registry.shutdown",
                workspace=self._workspace.workspace_id,
            )

            self._store.clear()
