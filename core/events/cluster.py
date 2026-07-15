# core/events.py
# Part 91
# EventBus Distributed Architecture and Cluster Coordination Layer


from __future__ import annotations
from .core import BaseEvent
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, Optional

from .middleware import (
    EventMiddleware,
)

# ============================================================
# Cluster Node State
# ============================================================


class EventClusterNodeState(str, Enum):
    """
    Distributed node lifecycle.
    """

    OFFLINE = "offline"

    JOINING = "joining"

    ONLINE = "online"

    DEGRADED = "degraded"

    LEAVING = "leaving"



# ============================================================
# Cluster Role
# ============================================================


class EventClusterNodeRole(str, Enum):
    """
    Cluster node responsibilities.
    """

    LEADER = "leader"

    WORKER = "worker"

    REPLICA = "replica"



# ============================================================
# Cluster Node
# ============================================================


@dataclass(slots=True)
class EventClusterNode:
    """
    Distributed EventBus node.
    """

    node_id: str

    hostname: str

    role:     EventClusterNodeRole

    state:      EventClusterNodeState

    last_seen: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Cluster Configuration
# ============================================================


@dataclass(slots=True)
class EventClusterConfiguration:
    """
    Distributed cluster settings.
    """

    cluster_name: str = (
        "arman-event-cluster"
    )

    replication_factor: int = 3

    heartbeat_interval: int = 10

    election_timeout: int = 30



# ============================================================
# Node Registry
# ============================================================


class EventClusterRegistry:
    """
    Stores cluster nodes.
    """

    def __init__(
        self,
    ) -> None:

        self.nodes: Dict[
            str,
            EventClusterNode
        ] = {}

        self.lock = threading.RLock()



    def register(
        self,
        node:
            EventClusterNode,
    ) -> None:

        with self.lock:

            self.nodes[
                node.node_id
            ] = node



    def remove(
        self,
        node_id:
            str,
    ) -> None:

        with self.lock:

            self.nodes.pop(
                node_id,
                None
            )



    def online_nodes(
        self,
    ) -> list[
        EventClusterNode
    ]:

        return [

            node
            for node
            in self.nodes.values()

            if node.state
            ==
            EventClusterNodeState.ONLINE

        ]



# ============================================================
# Leader Election
# ============================================================


class EventLeaderElection:
    """
    Controls cluster leadership.
    """

    def __init__(
        self,
        registry:
            EventClusterRegistry,
    ) -> None:

        self.registry = registry

        self.leader_id = None



    def elect(
        self,
    ) -> Optional[str]:

        nodes = (
            self.registry.online_nodes()
        )


        if not nodes:

            return None


        leader = sorted(
            nodes,
            key=lambda x:
                x.node_id
        )[0]


        leader.role = (
            EventClusterNodeRole.LEADER
        )


        self.leader_id = (
            leader.node_id
        )


        return self.leader_id



# ============================================================
# Cluster Heartbeat
# ============================================================


class EventHeartbeatManager:
    """
    Maintains node availability.
    """

    def __init__(
        self,
        registry:
            EventClusterRegistry,
    ) -> None:

        self.registry = registry



    def heartbeat(
        self,
        node_id:
            str,
    ) -> bool:

        node = (
            self.registry.nodes.get(
                node_id
            )
        )


        if not node:

            return False


        node.last_seen = (
            datetime.now(UTC)
        )

        node.state = (
            EventClusterNodeState.ONLINE
        )


        return True



# ============================================================
# Distributed Event Router
# ============================================================


class EventDistributedRouter:
    """
    Routes events between nodes.
    """

    def __init__(
        self,
        registry:
            EventClusterRegistry,
    ) -> None:

        self.registry = registry



    def route(
        self,
        event:
            BaseEvent,
    ) -> Optional[str]:

        nodes = (
            self.registry.online_nodes()
        )


        if not nodes:

            return None


        target = nodes[
            hash(
                event.event_id
            )
            %
            len(nodes)
        ]


        return target.node_id



# ============================================================
# Cluster Coordinator
# ============================================================


class EventClusterCoordinator:
    """
    Complete distributed controller.

    Features:
    - Node discovery
    - Leader election
    - Routing
    - Heartbeats
    """

    def __init__(
        self,
        config:
            Optional[
                EventClusterConfiguration
            ] = None,
    ) -> None:

        self.config = (
            config
            or
            EventClusterConfiguration()
        )

        self.registry = (
            EventClusterRegistry()
        )

        self.election = (
            EventLeaderElection(
                self.registry
            )
        )

        self.heartbeat = (
            EventHeartbeatManager(
                self.registry
            )
        )

        self.router = (
            EventDistributedRouter(
                self.registry
            )
        )



    def status(
        self,
    ) -> Dict[str, Any]:

        return {

            "cluster":
                self.config.cluster_name,

            "nodes":
                len(
                    self.registry.nodes
                ),

            "leader":
                self.election.leader_id,

        }



# ============================================================
# Cluster Middleware
# ============================================================


class EventClusterMiddleware(
    EventMiddleware
):
    """
    Distributed cluster middleware.
    """

    def __init__(
        self,
        coordinator:
            EventClusterCoordinator,
    ) -> None:

        super().__init__(
            "cluster_coordination"
        )

        self.coordinator = coordinator



# ============================================================
# Global Cluster Objects
# ============================================================


event_cluster_coordinator = (
    EventClusterCoordinator()
)


event_cluster_middleware = (
    EventClusterMiddleware(
        event_cluster_coordinator
    )
)