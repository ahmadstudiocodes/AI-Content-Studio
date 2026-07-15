# ============================================================
# File: studio/transaction_manager.py
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
from typing import Any, Callable, Mapping, Protocol


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


class TransactionStatus(str, Enum):

    CREATED = "created"

    RUNNING = "running"

    COMMITTED = "committed"

    ROLLED_BACK = "rolled_back"

    FAILED = "failed"


@dataclass(slots=True)
class TransactionMetadata:

    transaction_id: str

    name: str

    created_at: str

    updated_at: str

    status: TransactionStatus

    operations: int

    error: str | None = None

    custom: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class TransactionRecord:

    metadata: TransactionMetadata

    path: Path

    snapshot: dict[str, Any] = field(
        default_factory=dict
    )


class TransactionError(Exception):
    pass


class TransactionNotFound(
    TransactionError
):
    pass


class TransactionRegistry:

    """
    Enterprise Thread Safe Transaction Registry
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._transactions: dict[
            str,
            TransactionRecord,
        ] = {}

    def add(
        self,
        transaction: TransactionRecord,
    ) -> None:

        with self._lock:

            self._transactions[
                transaction.metadata.transaction_id
            ] = transaction

    def get(
        self,
        transaction_id: str,
    ) -> TransactionRecord:

        with self._lock:

            try:

                return self._transactions[
                    transaction_id
                ]

            except KeyError as exc:

                raise TransactionNotFound(
                    transaction_id
                ) from exc

    def remove(
        self,
        transaction_id: str,
    ) -> None:

        with self._lock:

            self._transactions.pop(
                transaction_id
            )

    def all(
        self,
    ) -> list[TransactionRecord]:

        with self._lock:

            return list(
                self._transactions.values()
            )

    def clear(
        self,
    ) -> None:

        with self._lock:

            self._transactions.clear()


class TransactionManager:

    """
    StudioOS Enterprise Transaction Manager

    Features:

    - Atomic Operations
    - Commit / Rollback
    - Snapshot Support
    - Transaction History
    - Runtime Integration
    - Event Bus Integration
    - Plugin Hooks

    Enterprise Upgrade Ready
    """

    TRANSACTION_FILE = "transaction.json"

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

        self._registry = TransactionRegistry()

        self._root = (
            self._workspace.root /
            "transactions"
        )

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_existing_transactions()

# ============================================================
# File: studio/transaction_manager.py
# Part: 2
# Enterprise Framework v1
# ============================================================

    @staticmethod
    def _utc() -> str:

        return datetime.now(
            UTC
        ).isoformat()

    @staticmethod
    def _transaction_id() -> str:

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

    def _load_existing_transactions(
        self,
    ) -> None:

        for transaction_file in self._root.rglob(
            self.TRANSACTION_FILE
        ):

            try:

                data = json.loads(
                    transaction_file.read_text(
                        encoding="utf-8",
                    )
                )

                record = TransactionRecord(
                    metadata=TransactionMetadata(
                        transaction_id=data[
                            "transaction_id"
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
                        status=TransactionStatus(
                            data[
                                "status"
                            ]
                        ),
                        operations=data.get(
                            "operations",
                            0,
                        ),
                        error=data.get(
                            "error"
                        ),
                        custom=dict(
                            data.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    path=transaction_file.parent,
                    snapshot=dict(
                        data.get(
                            "snapshot",
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
        transaction: TransactionRecord,
    ) -> None:

        transaction.metadata.updated_at = (
            self._utc()
        )

        payload = {
            "transaction_id":
                transaction.metadata.transaction_id,
            "name":
                transaction.metadata.name,
            "created_at":
                transaction.metadata.created_at,
            "updated_at":
                transaction.metadata.updated_at,
            "status":
                transaction.metadata.status,
            "operations":
                transaction.metadata.operations,
            "error":
                transaction.metadata.error,
            "custom":
                transaction.metadata.custom,
            "snapshot":
                transaction.snapshot,
        }

        transaction.path.write_text(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def create_transaction(
        self,
        *,
        name: str,
        snapshot: Mapping[
            str,
            Any,
        ] | None = None,
        custom: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> TransactionRecord:

        with self._lock:

            transaction_id = (
                self._transaction_id()
            )

            path = (
                self._root /
                transaction_id
            )

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

            record = TransactionRecord(
                metadata=TransactionMetadata(
                    transaction_id=transaction_id,
                    name=name,
                    created_at=self._utc(),
                    updated_at=self._utc(),
                    status=(
                        TransactionStatus.CREATED
                    ),
                    operations=0,
                    custom=dict(
                        custom or {}
                    ),
                ),
                path=(
                    path /
                    self.TRANSACTION_FILE
                ),
                snapshot=dict(
                    snapshot or {}
                ),
            )

            self._save(
                record
            )

            self._registry.add(
                record
            )

            self._emit(
                "transaction.created",
                transaction_id=transaction_id,
            )

            return record

    def begin(
        self,
        transaction_id: str,
    ) -> TransactionRecord:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            transaction.metadata.status = (
                TransactionStatus.RUNNING
            )

            self._save(
                transaction
            )

            self._emit(
                "transaction.started",
                transaction_id=transaction_id,
            )

            return transaction
        
# ============================================================
# File: studio/transaction_manager.py
# Part: 3
# Enterprise Framework v1
# ============================================================

    def execute(
        self,
        transaction_id: str,
        operation: Callable[
            [],
            Any,
        ],
    ) -> Any:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            if (
                transaction.metadata.status
                is not TransactionStatus.RUNNING
            ):

                raise TransactionError(
                    "Transaction is not running"
                )

            try:

                result = operation()

                transaction.metadata.operations += 1

                self._save(
                    transaction
                )

                self._emit(
                    "transaction.operation.executed",
                    transaction_id=transaction_id,
                )

                return result

            except Exception as exc:

                transaction.metadata.error = (
                    str(exc)
                )

                transaction.metadata.status = (
                    TransactionStatus.FAILED
                )

                self._save(
                    transaction
                )

                self._emit(
                    "transaction.failed",
                    transaction_id=transaction_id,
                    error=str(exc),
                )

                raise

    def commit(
        self,
        transaction_id: str,
    ) -> TransactionRecord:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            if (
                transaction.metadata.status
                is TransactionStatus.FAILED
            ):

                raise TransactionError(
                    "Failed transaction cannot commit"
                )

            transaction.metadata.status = (
                TransactionStatus.COMMITTED
            )

            self._save(
                transaction
            )

            self._emit(
                "transaction.committed",
                transaction_id=transaction_id,
            )

            return transaction

    def rollback(
        self,
        transaction_id: str,
        restore: Callable[
            [dict[str, Any]],
            None,
        ],
    ) -> TransactionRecord:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            restore(
                transaction.snapshot
            )

            transaction.metadata.status = (
                TransactionStatus.ROLLED_BACK
            )

            self._save(
                transaction
            )

            self._emit(
                "transaction.rollback",
                transaction_id=transaction_id,
            )

            return transaction

    def get_transaction(
        self,
        transaction_id: str,
    ) -> TransactionRecord:

        return self._registry.get(
            transaction_id
        )

    def list_transactions(
        self,
    ) -> list[TransactionRecord]:

        return sorted(
            self._registry.all(),
            key=lambda item:
                item.metadata.created_at,
        )

    def delete_transaction(
        self,
        transaction_id: str,
    ) -> None:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            if transaction.path.parent.exists():

                import shutil

                shutil.rmtree(
                    transaction.path.parent
                )

            self._registry.remove(
                transaction_id
            )

            self._emit(
                "transaction.deleted",
                transaction_id=transaction_id,
            )

    def update_snapshot(
        self,
        transaction_id: str,
        snapshot: Mapping[
            str,
            Any,
        ],
    ) -> TransactionRecord:

        with self._lock:

            transaction = (
                self._registry.get(
                    transaction_id
                )
            )

            transaction.snapshot = dict(
                snapshot
            )

            self._save(
                transaction
            )

            self._emit(
                "transaction.snapshot.updated",
                transaction_id=transaction_id,
            )

            return transaction
        
# ============================================================
# File: studio/transaction_manager.py
# Part: 4
# Enterprise Framework v1
# ============================================================

    def export_registry(
        self,
        destination: Path,
    ) -> Path:

        with self._lock:

            payload = [
                {
                    "metadata":
                        asdict(
                            transaction.metadata
                        ),
                    "snapshot":
                        transaction.snapshot,
                }
                for transaction
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

                metadata = item[
                    "metadata"
                ]

                transaction_id = metadata[
                    "transaction_id"
                ]

                transaction_path = (
                    self._root /
                    transaction_id
                )

                if not transaction_path.exists():

                    transaction_path.mkdir(
                        parents=True,
                        exist_ok=True,
                    )

                record = TransactionRecord(
                    metadata=TransactionMetadata(
                        transaction_id=transaction_id,
                        name=metadata[
                            "name"
                        ],
                        created_at=metadata[
                            "created_at"
                        ],
                        updated_at=metadata[
                            "updated_at"
                        ],
                        status=TransactionStatus(
                            metadata[
                                "status"
                            ]
                        ),
                        operations=metadata.get(
                            "operations",
                            0,
                        ),
                        error=metadata.get(
                            "error"
                        ),
                        custom=dict(
                            metadata.get(
                                "custom",
                                {},
                            )
                        ),
                    ),
                    path=(
                        transaction_path /
                        self.TRANSACTION_FILE
                    ),
                    snapshot=dict(
                        item.get(
                            "snapshot",
                            {},
                        )
                    ),
                )

                self._save(
                    record
                )

                self._registry.add(
                    record
                )

                imported += 1

            self._emit(
                "transaction.registry.imported",
                count=imported,
            )

            return imported

    def statistics(
        self,
    ) -> dict[str, Any]:

        transactions = (
            self._registry.all()
        )

        status_count: dict[str, int] = {}

        operations = 0

        for transaction in transactions:

            status = (
                transaction.metadata.status.value
            )

            status_count[status] = (
                status_count.get(
                    status,
                    0,
                )
                + 1
            )

            operations += (
                transaction.metadata.operations
            )

        return {
            "workspace_id":
                self._workspace.workspace_id,
            "transaction_count":
                len(transactions),
            "operation_count":
                operations,
            "statuses":
                status_count,
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

        failed = [
            transaction.metadata.transaction_id
            for transaction
            in self._registry.all()
            if (
                transaction.metadata.status
                is TransactionStatus.FAILED
            )
        ]

        return {
            "healthy":
                not failed,
            "failed_transactions":
                failed,
            "registered_transactions":
                len(
                    self._registry.all()
                ),
            "timestamp":
                time.time(),
        }
    
    # ============================================================
# File: studio/transaction_manager.py
# Part: 5
# Enterprise Framework v1
# ============================================================

    def synchronize(
        self,
    ) -> None:

        with self._lock:

            for transaction in (
                self._registry.all()
            ):

                self._save(
                    transaction
                )

            if self._shared_state is not None:

                self._shared_state.set(
                    "studio.transaction_count",
                    len(
                        self._registry.all()
                    ),
                )

            self._emit(
                "transaction_manager.synchronized",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

    def recover_pending(
        self,
    ) -> list[str]:

        recovered: list[str] = []

        with self._lock:

            for transaction in (
                self._registry.all()
            ):

                if (
                    transaction.metadata.status
                    is TransactionStatus.RUNNING
                ):

                    transaction.metadata.status = (
                        TransactionStatus.ROLLED_BACK
                    )

                    transaction.metadata.error = (
                        "Recovered after interrupted execution"
                    )

                    self._save(
                        transaction
                    )

                    recovered.append(
                        transaction.metadata.transaction_id
                    )

                    self._emit(
                        "transaction.recovered",
                        transaction_id=(
                            transaction.metadata.transaction_id
                        ),
                    )

        return recovered

    def rollback_all_failed(
        self,
        restore: Callable[
            [dict[str, Any]],
            None,
        ],
    ) -> list[str]:

        rolled_back: list[str] = []

        with self._lock:

            for transaction in (
                self._registry.all()
            ):

                if (
                    transaction.metadata.status
                    is TransactionStatus.FAILED
                ):

                    restore(
                        transaction.snapshot
                    )

                    transaction.metadata.status = (
                        TransactionStatus.ROLLED_BACK
                    )

                    self._save(
                        transaction
                    )

                    rolled_back.append(
                        transaction.metadata.transaction_id
                    )

                    self._emit(
                        "transaction.failed.rollback",
                        transaction_id=(
                            transaction.metadata.transaction_id
                        ),
                    )

        return rolled_back

    def cleanup(
        self,
        *,
        keep_committed: bool = True,
    ) -> int:

        removed = 0

        with self._lock:

            transactions = (
                self._registry.all()
            )

            for transaction in transactions:

                removable = (
                    transaction.metadata.status
                    in {
                        TransactionStatus.ROLLED_BACK,
                        TransactionStatus.FAILED,
                    }
                )

                if (
                    keep_committed
                    and
                    transaction.metadata.status
                    is TransactionStatus.COMMITTED
                ):

                    removable = False

                if removable:

                    self.delete_transaction(
                        transaction.metadata.transaction_id
                    )

                    removed += 1

        return removed

    def shutdown(
        self,
    ) -> None:

        with self._lock:

            self.synchronize()

            self._emit(
                "transaction_manager.shutdown",
                workspace=(
                    self._workspace.workspace_id
                ),
            )

            self._registry.clear()
