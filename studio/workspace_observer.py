# ==========================================================
# Part 39
# Workspace Observer Core
# File:
#     studio/workspace_observer.py
# ==========================================================


from __future__ import annotations


import threading

from dataclasses import (
    dataclass,
    field,
)

from datetime import (
    UTC,
    datetime,
)

from typing import (
    Any,
    Callable,
    Dict,
    List,
)


from .workspace import (
    Workspace,
    WorkspaceStatus,
    workspace_registry,
)

# ==========================================================
# EventBus Integration
# ==========================================================

try:

    from brain.event_bus import event_bus

except Exception:

    event_bus = None

# ==========================================================
# Observation Event
# ==========================================================


@dataclass(slots=True)
class WorkspaceObservation:
    """
    Workspace observation event.
    """

    event: str

    workspace_id: str

    workspace_name: str

    status: str

    created_at: str = field(
        default_factory=lambda:
        datetime.now(
            UTC
        ).isoformat()
    )

    payload: Dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )



# ==========================================================
# Observer Callback
# ==========================================================


WorkspaceObserverCallback = Callable[
    [
        WorkspaceObservation
    ],
    None,
]



# ==========================================================
# Workspace Observer
# ==========================================================


class WorkspaceObserver:
    """
    Enterprise Workspace Observer.

    Responsibilities:

        - Observe workspace lifecycle
        - Track workspace state
        - Notify subscribers
        - Store observation history
    """


    def __init__(
        self,
        workspace: Workspace,
    ) -> None:


        self.workspace = workspace


        self._lock = (
            threading.RLock()
        )


        self._listeners: List[
            WorkspaceObserverCallback
        ] = []


        self._history: List[
            WorkspaceObservation
        ] = []



    # ======================================================
    # Subscribe
    # ======================================================


    def subscribe(
        self,
        callback: WorkspaceObserverCallback,
    ) -> None:


        with self._lock:

            if callback not in self._listeners:

                self._listeners.append(
                    callback
                )



    # ======================================================
    # Unsubscribe
    # ======================================================


    def unsubscribe(
        self,
        callback: WorkspaceObserverCallback,
    ) -> None:


        with self._lock:

            if callback in self._listeners:

                self._listeners.remove(
                    callback
                )



    # ======================================================
    # Emit
    # ======================================================


    def emit(
        self,
        event: str,
        **payload: Any,
    ) -> WorkspaceObservation:


        observation = WorkspaceObservation(

            event=event,

            workspace_id=self.workspace.id,

            workspace_name=self.workspace.name,

            status=self.workspace.status.value,

            payload=payload,

        )


        with self._lock:


            self._history.append(
                observation
            )


            listeners = list(
                self._listeners
            )



        for listener in listeners:

            try:

                listener(
                    observation
                )

            except Exception:

                pass



        return observation



    # ======================================================
    # Lifecycle Observations
    # ======================================================


    def observe_open(
        self,
    ) -> WorkspaceObservation:

        return self.emit(
            "workspace.opened"
        )


    def observe_close(
        self,
    ) -> WorkspaceObservation:

        return self.emit(
            "workspace.closed"
        )


    def observe_save(
        self,
    ) -> WorkspaceObservation:

        return self.emit(
            "workspace.saved",
            saves=self.workspace.statistics.get(
                "saves",
                0,
            ),
        )


    def observe_archive(
        self,
    ) -> WorkspaceObservation:

        return self.emit(
            "workspace.archived"
        )



    # ======================================================
    # State Check
    # ======================================================


    def check_state(
        self,
    ) -> WorkspaceObservation:


        return self.emit(

            "workspace.state.checked",

            state=self.workspace.status.value,

            healthy=self.workspace.health.get(
                "healthy",
                True,
            ),

        )



    # ======================================================
    # History
    # ======================================================


    def history(
        self,
    ) -> List[
        WorkspaceObservation
    ]:

        with self._lock:

            return list(
                self._history
            )



# ==========================================================
# Registry Observer
# ==========================================================


class WorkspaceRegistryObserver:
    """
    Observe registered workspaces.
    """


    def __init__(
        self,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self._known: Dict[
            str,
            str,
        ] = {}



    def scan(
        self,
    ) -> List[
        WorkspaceObservation
    ]:


        changes = []


        with self._lock:


            for workspace in workspace_registry:


                previous = (
                    self._known.get(
                        workspace.id
                    )
                )


                current = (
                    workspace.status.value
                )


                if previous != current:


                    changes.append(

                        WorkspaceObservation(

                            event=
                                "workspace.status.changed",

                            workspace_id=
                                workspace.id,

                            workspace_name=
                                workspace.name,

                            status=
                                current,

                            payload={

                                "previous":
                                    previous,

                                "current":
                                    current,

                            },

                        )

                    )


                self._known[
                    workspace.id
                ] = current



        return changes



# ==========================================================
# Global Services
# ==========================================================


workspace_registry_observer = (
    WorkspaceRegistryObserver()
)



__all__ = [

    "WorkspaceObservation",

    "WorkspaceObserver",

    "WorkspaceRegistryObserver",

    "workspace_registry_observer",

]

# ==========================================================
# Part 40
# Workspace Monitoring Engine
# File:
#     studio/workspace_observer.py
# ==========================================================

# ==========================================================
# Workspace Observer Registry
# ==========================================================


class WorkspaceObserverRegistry:
    """
    Registry for workspace observers.
    """


    def __init__(
        self,
    ) -> None:

        self._observers = {}


    def register(
        self,
        observer: WorkspaceObserver,
    ) -> None:

        self._observers[
            observer.workspace.id
        ] = observer


    def unregister(
        self,
        workspace_id: str,
    ) -> None:

        self._observers.pop(
            workspace_id,
            None,
        )


    def get(
        self,
        workspace_id: str,
    ) -> WorkspaceObserver | None:

        return self._observers.get(
            workspace_id
        )


    def all(
        self,
    ):

        return list(
            self._observers.values()
        )



workspace_observer_registry = (
    WorkspaceObserverRegistry()
)

# ==========================================================
# Workspace Monitor Metrics
# ==========================================================


@dataclass(slots=True)
class WorkspaceMonitorMetrics:
    """
    Runtime metrics collected from workspace.
    """

    workspace_id: str

    status: str

    projects: int = 0

    assets: int = 0

    services: int = 0

    extensions: int = 0

    history_events: int = 0

    snapshots: int = 0

    saves: int = 0

    backups: int = 0

    healthy: bool = True

    collected_at: str = field(
        default_factory=lambda:
        datetime.now(
            UTC
        ).isoformat()
    )


# ==========================================================
# Workspace Monitor
# ==========================================================


class WorkspaceMonitor:
    """
    Enterprise Workspace Monitoring Engine.

    Responsibilities:

        - Collect metrics
        - Monitor health
        - Track activity
        - Detect issues
    """


    def __init__(
        self,
        workspace: Workspace,
    ) -> None:


        self.workspace = workspace


        self._lock = (
            threading.RLock()
        )


        self.metrics_history: List[
            WorkspaceMonitorMetrics
        ] = []



    # ======================================================
    # Collect Metrics
    # ======================================================


    def collect(
        self,
    ) -> WorkspaceMonitorMetrics:


        with self._lock:


            statistics = (
                self.workspace.statistics
            )


            metrics = WorkspaceMonitorMetrics(

                workspace_id=
                    self.workspace.id,

                status=
                    self.workspace.status.value,

                projects=
                    len(
                        self.workspace.projects
                    ),

                assets=
                    len(
                        self.workspace.assets
                    ),

                services=
                    len(
                        self.workspace.services
                    ),

                extensions=
                    len(
                        self.workspace.extensions
                    ),

                history_events=
                    len(
                        self.workspace.history
                    ),

                snapshots=
                    len(
                        self.workspace.snapshots
                    ),

                saves=
                    statistics.get(
                        "saves",
                        0,
                    ),

                backups=
                    statistics.get(
                        "backups",
                        0,
                    ),

                healthy=
                    self.workspace.health.get(
                        "healthy",
                        True,
                    ),

            )


            self.metrics_history.append(
                metrics
            )


            return metrics



    # ======================================================
    # Health Check
    # ======================================================


    def health_check(
        self,
    ) -> Dict[str, Any]:


        errors = []


        warnings = []


        try:


            if not self.workspace.root.exists():

                errors.append(
                    "workspace_root_missing"
                )


            if (
                self.workspace.status
                == WorkspaceStatus.BROKEN
            ):

                errors.append(
                    "workspace_broken"
                )


        except Exception as exc:


            errors.append(
                str(exc)
            )



        healthy = (
            len(errors) == 0
        )


        report = {

            "healthy":
                healthy,

            "workspace_id":
                self.workspace.id,

            "status":
                self.workspace.status.value,

            "errors":
                errors,

            "warnings":
                warnings,

            "checked_at":
                datetime.now(
                    UTC
                ).isoformat(),

        }


        self.workspace.health.update(
            report
        )


        return report



    # ======================================================
    # Activity
    # ======================================================


    def activity(
        self,
    ) -> Dict[str, Any]:


        return {

            "workspace":
                self.workspace.name,

            "status":
                self.workspace.status.value,

            "history":
                len(
                    self.workspace.history
                ),

            "snapshots":
                len(
                    self.workspace.snapshots
                ),

            "sessions":
                1
                if self.workspace.session.active
                else 0,

        }



    # ======================================================
    # Latest Metrics
    # ======================================================


    def latest(
        self,
    ) -> WorkspaceMonitorMetrics | None:


        if not self.metrics_history:

            return None


        return self.metrics_history[-1]



    # ======================================================
    # Clear History
    # ======================================================


    def clear(
        self,
    ) -> None:


        with self._lock:

            self.metrics_history.clear()



# ==========================================================
# Global Monitor Registry
# ==========================================================


class WorkspaceMonitorRegistry:
    """
    Keeps monitors for active workspaces.
    """


    def __init__(
        self,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self._monitors: Dict[
            str,
            WorkspaceMonitor,
        ] = {}



    def register(
        self,
        monitor: WorkspaceMonitor,
    ) -> None:


        with self._lock:

            self._monitors[
                monitor.workspace.id
            ] = monitor



    def unregister(
        self,
        workspace_id: str,
    ) -> None:


        with self._lock:

            self._monitors.pop(
                workspace_id,
                None,
            )



    def get(
        self,
        workspace_id: str,
    ) -> WorkspaceMonitor | None:


        return self._monitors.get(
            workspace_id
        )



    def all(
        self,
    ) -> List[
        WorkspaceMonitor
    ]:


        return list(
            self._monitors.values()
        )



# ==========================================================
# Global Instance
# ==========================================================


workspace_monitor_registry = (
    WorkspaceMonitorRegistry()
)

# ==========================================================
# Part 41
# Workspace Event Observer
# File:
#     studio/workspace_observer.py
# ==========================================================


# ==========================================================
# Event Bus Integration
# ==========================================================


class WorkspaceEventObserver:
    """
    Connects workspace events with EventBus.

    Responsibilities:

        - Subscribe to workspace events
        - Receive lifecycle notifications
        - Forward events to observers
        - Maintain event state
    """


    EVENTS = [

        "workspace.created",

        "workspace.opened",

        "workspace.saved",

        "workspace.closed",

        "workspace.archived",

        "workspace.deleted",

        "workspace.restored",

        "workspace.transaction_committed",

        "workspace.transaction_rolled_back",

    ]


    def __init__(
        self,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self.received: List[
            WorkspaceObservation
        ] = []


        self.enabled = True



    # ======================================================
    # Attach EventBus
    # ======================================================


    def attach(
        self,
    ) -> None:


        if event_bus is None:

            return


        for event_name in self.EVENTS:

            try:

                event_bus.subscribe(

                    event_name,

                    self.handle,

                )

            except Exception:

                pass



    # ======================================================
    # Handle Event
    # ======================================================


    def handle(
        self,
        event: Any,
        **payload: Any,
    ) -> None:


        if not self.enabled:

            return



        workspace = (
            payload.get(
                "workspace"
            )
        )


        if workspace is None:

            return



        observation = WorkspaceObservation(

            event=
                getattr(
                    event,
                    "name",
                    str(
                        event
                    ),
                ),

            workspace_id=
                workspace.id,

            workspace_name=
                workspace.name,

            status=
                workspace.status.value,

            payload=
                payload,

        )


        with self._lock:

            self.received.append(
                observation
            )



    # ======================================================
    # Enable / Disable
    # ======================================================


    def enable(
        self,
    ) -> None:

        self.enabled = True



    def disable(
        self,
    ) -> None:

        self.enabled = False



    # ======================================================
    # History
    # ======================================================


    def history(
        self,
    ) -> List[
        WorkspaceObservation
    ]:


        with self._lock:

            return list(
                self.received
            )



    # ======================================================
    # Clear
    # ======================================================


    def clear(
        self,
    ) -> None:


        with self._lock:

            self.received.clear()



# ==========================================================
# Event Observer Service
# ==========================================================


class WorkspaceEventService:
    """
    Unified event observation service.
    """


    def __init__(
        self,
    ) -> None:


        self.observer = (
            WorkspaceEventObserver()
        )


        self.started = False



    def start(
        self,
    ) -> None:


        if self.started:

            return


        self.observer.attach()


        self.started = True



    def stop(
        self,
    ) -> None:


        self.started = False


        self.observer.disable()



    def events(
        self,
    ) -> List[
        WorkspaceObservation
    ]:


        return self.observer.history()



# ==========================================================
# Global Event Observer
# ==========================================================


workspace_event_observer = (
    WorkspaceEventObserver()
)


workspace_event_service = (
    WorkspaceEventService()
)

# ==========================================================
# Part 42
# Enterprise Observer Service
# File:
#     studio/workspace_observer.py
# ==========================================================


# ==========================================================
# Workspace Observer Service
# ==========================================================


class WorkspaceObserverService:
    """
    Unified Enterprise Workspace Observer.

    Responsibilities:

        - Manage observers
        - Manage monitors
        - Connect EventBus
        - Provide runtime access
        - Expose diagnostics
    """


    def __init__(
        self,
    ) -> None:


        self._lock = (
            threading.RLock()
        )


        self.started = False



    # ======================================================
    # Start Service
    # ======================================================


    def start(
        self,
    ) -> None:


        with self._lock:


            if self.started:

                return


            workspace_event_service.start()


            self.started = True



    # ======================================================
    # Stop Service
    # ======================================================


    def stop(
        self,
    ) -> None:


        with self._lock:


            workspace_event_service.stop()


            self.started = False



    # ======================================================
    # Attach Workspace
    # ======================================================


    def attach(
        self,
        workspace: Workspace,
    ) -> WorkspaceObserver:


        observer = WorkspaceObserver(
            workspace
        )


        monitor = WorkspaceMonitor(
            workspace
        )


        workspace_observer_registry.register(
            observer
        )


        workspace_monitor_registry.register(
            monitor
        )


        return observer



    # ======================================================
    # Detach Workspace
    # ======================================================


    def detach(
        self,
        workspace_id: str,
    ) -> None:


        workspace_observer_registry.unregister(
            workspace_id
        )


        workspace_monitor_registry.unregister(
            workspace_id
        )



    # ======================================================
    # Observe Workspace
    # ======================================================


    def observe(
        self,
        workspace_id: str,
    ) -> Dict[str, Any]:


        observer = (
            workspace_observer_registry.get(
                workspace_id
            )
        )


        monitor = (
            workspace_monitor_registry.get(
                workspace_id
            )
        )


        if observer is None:

            return {

                "exists": False,

                "workspace_id":
                    workspace_id,

            }



        result = {

            "exists": True,

            "observer": {

                "events":
                    len(
                        observer.history()
                    ),

            },

        }



        if monitor:

            result[
                "monitor"
            ] = {

                "metrics":
                    monitor.collect(),

                "health":
                    monitor.health_check(),

            }



        return result



    # ======================================================
    # Observe All
    # ======================================================


    def observe_all(
        self,
    ) -> List[
        Dict[str, Any]
    ]:


        result = []


        for observer in (
            workspace_observer_registry.all()
        ):


            result.append(

                self.observe(

                    observer.workspace.id

                )

            )


        return result



    # ======================================================
    # Health
    # ======================================================


    def health(
        self,
    ) -> Dict[str, Any]:


        return {

            "service":

                "workspace_observer",


            "running":

                self.started,


            "observers":

                len(
                    workspace_observer_registry.all()
                ),


            "monitors":

                len(
                    workspace_monitor_registry.all()
                ),


            "events":

                len(
                    workspace_event_observer.history()
                ),

        }



# ==========================================================
# Global Enterprise Observer
# ==========================================================


workspace_observer_service = (
    WorkspaceObserverService()
)



# ==========================================================
# Auto Attach Existing Workspaces
# ==========================================================


def initialize_workspace_observers() -> None:
    """
    Attach observers to registered workspaces.
    """


    for workspace in workspace_registry:

        workspace_observer_service.attach(
            workspace
        )


    workspace_observer_service.start()



# ==========================================================
# Public API
# ==========================================================


__all__ += [

    "WorkspaceMonitorMetrics",

    "WorkspaceMonitor",

    "WorkspaceMonitorRegistry",

    "workspace_monitor_registry",

    "WorkspaceEventObserver",

    "WorkspaceEventService",

    "workspace_event_observer",

    "workspace_event_service",

    "WorkspaceObserverService",

    "workspace_observer_service",

    "initialize_workspace_observers",

]