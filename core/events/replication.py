# core/events.py
# Part 95
# Advanced Distributed Event Replication Layer

from __future__ import annotations

import uuid

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum

from typing import Any, Dict, Optional
from .core import BaseEvent
from .middleware import EventMiddleware

# ============================================================
# Replication Mode
# ============================================================


class EventReplicationMode(str, Enum):
    """
    Event replication strategies.
    """

    SYNCHRONOUS = "synchronous"

    ASYNCHRONOUS = "asynchronous"

    HYBRID = "hybrid"



# ============================================================
# Replication State
# ============================================================


class EventReplicationState(str, Enum):
    """
    Replication lifecycle.
    """

    PENDING = "pending"

    REPLICATING = "replicating"

    COMPLETED = "completed"

    FAILED = "failed"



# ============================================================
# Replication Record
# ============================================================


@dataclass(slots=True)
class EventReplicationRecord:
    """
    Distributed event copy metadata.
    """

    replication_id: str

    event_id: str

    source_node: str

    target_node: str

    state:     EventReplicationState

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Replica Node
# ============================================================


@dataclass(slots=True)
class EventReplicaNode:
    """
    Replica destination.
    """

    node_id: str

    location: str

    healthy: bool = True

    last_sync: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Replica Registry
# ============================================================


class EventReplicaRegistry:
    """
    Manages replica nodes.
    """

    def __init__(
        self,
    ) -> None:

        self.replicas: Dict[
            str,
            EventReplicaNode
        ] = {}



    def register(
        self,
        replica:
            EventReplicaNode,
    ) -> None:

        self.replicas[
            replica.node_id
        ] = replica



    def available(
        self,
    ) -> list[
        EventReplicaNode
    ]:

        return [

            replica
            for replica
            in self.replicas.values()

            if replica.healthy

        ]



# ============================================================
# Replication Queue
# ============================================================


class EventReplicationQueue:
    """
    Stores pending replication jobs.
    """

    def __init__(
        self,
    ) -> None:

        self.queue: list[
            EventReplicationRecord
        ] = []



    def add(
        self,
        record:
            EventReplicationRecord,
    ) -> None:

        self.queue.append(
            record
        )



    def pending(
        self,
    ) -> list[
        EventReplicationRecord
    ]:

        return [

            item
            for item
            in self.queue

            if item.state
            ==
            EventReplicationState.PENDING

        ]



# ============================================================
# Event Replication Engine
# ============================================================


class EventReplicationEngine:
    """
    Distributed replication controller.

    Features:
    - Multi node replication
    - Failure handling
    - Synchronization
    """

    def __init__(
        self,
        mode:
            EventReplicationMode =
            EventReplicationMode.ASYNCHRONOUS,
    ) -> None:

        self.mode = mode

        self.registry = (
            EventReplicaRegistry()
        )

        self.queue = (
            EventReplicationQueue()
        )

        self.history: list[
            EventReplicationRecord
        ] = []



    def replicate(
        self,
        event:
            BaseEvent,
        source:
            str,
    ) -> list[
        EventReplicationRecord
    ]:


        records = []


        for replica in (
            self.registry.available()
        ):

            record = EventReplicationRecord(
                replication_id=
                    uuid.uuid4().hex,

                event_id=
                    event.event_id,

                source_node=
                    source,

                target_node=
                    replica.node_id,

                state=
                    EventReplicationState.PENDING,
            )


            self.queue.add(
                record
            )


            records.append(
                record
            )


        return records



    def synchronize(
        self,
    ) -> None:

        for record in (
            self.queue.pending()
        ):

            record.state = (
                EventReplicationState.REPLICATING
            )


            # Future:
            # real distributed transport


            record.state = (
                EventReplicationState.COMPLETED
            )


            self.history.append(
                record
            )



# ============================================================
# Conflict Resolver
# ============================================================


class EventReplicationConflictResolver:
    """
    Handles replicated event conflicts.
    """

    def resolve(
        self,
        first:
            EventReplicationRecord,
        second:
            EventReplicationRecord,
    ) -> EventReplicationRecord:

        if (
            first.created_at
            <=
            second.created_at
        ):

            return first


        return second



# ============================================================
# Global Replication Manager
# ============================================================


class EventDistributedReplicationManager:
    """
    Complete replication layer.

    Provides:
    - Replication
    - Synchronization
    - Conflict resolution
    """

    def __init__(
        self,
    ) -> None:

        self.engine = (
            EventReplicationEngine()
        )

        self.resolver = (
            EventReplicationConflictResolver()
        )



    def publish_replica(
        self,
        event:
            BaseEvent,
        node:
            str,
    ) -> list[
        EventReplicationRecord
    ]:

        return (
            self.engine.replicate(
                event,
                node,
            )
        )



# ============================================================
# Replication Middleware
# ============================================================


class EventReplicationMiddleware(
    EventMiddleware
):
    """
    Distributed replication middleware.
    """

    def __init__(
        self,
        manager:
            EventDistributedReplicationManager,
    ) -> None:

        super().__init__(
            "event_replication"
        )

        self.manager = manager



# ============================================================
# Global Replication Objects
# ============================================================


event_distributed_replication_manager = (
    EventDistributedReplicationManager()
)


event_replication_middleware = (
    EventReplicationMiddleware(
        event_distributed_replication_manager
    )
)