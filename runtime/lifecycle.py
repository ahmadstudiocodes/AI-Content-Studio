from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, List


class RuntimeState(Enum):

    CREATED = "created"

    INITIALIZING = "initializing"

    RUNNING = "running"

    STOPPING = "stopping"

    STOPPED = "stopped"


_VALID_TRANSITIONS = {
    RuntimeState.CREATED: {
        RuntimeState.INITIALIZING,
    },
    RuntimeState.INITIALIZING: {
        RuntimeState.RUNNING,
    },
    RuntimeState.RUNNING: {
        RuntimeState.STOPPING,
    },
    RuntimeState.STOPPING: {
        RuntimeState.STOPPED,
    },
    RuntimeState.STOPPED: set(),
}


@dataclass(slots=True)
class RuntimeLifecycle:

    state: RuntimeState = (
        RuntimeState.CREATED
    )

    startup_hooks: List[Callable] = field(
        default_factory=list
    )

    shutdown_hooks: List[Callable] = field(
        default_factory=list
    )

    def _transition(
        self,
        new_state: RuntimeState,
    ) -> None:

        allowed = _VALID_TRANSITIONS[
            self.state
        ]

        if new_state not in allowed:

            raise RuntimeError(
                f"Invalid runtime transition: "
                f"{self.state.value} -> "
                f"{new_state.value}"
            )

        self.state = new_state

    def initialize(self):

        self._transition(
            RuntimeState.INITIALIZING
        )

        for hook in self.startup_hooks:

            hook()

        self._transition(
            RuntimeState.RUNNING
        )

    def shutdown(self):

        self._transition(
            RuntimeState.STOPPING
        )

        for hook in self.shutdown_hooks:

            hook()

        self._transition(
            RuntimeState.STOPPED
        )

    def register_startup(
        self,
        hook: Callable,
    ):

        self.startup_hooks.append(
            hook
        )

    def register_shutdown(
        self,
        hook: Callable,
    ):

        self.shutdown_hooks.append(
            hook
        )

    @property
    def is_running(
        self,
    ) -> bool:

        return (
            self.state
            is RuntimeState.RUNNING
        )

    @property
    def is_stopped(
        self,
    ) -> bool:

        return (
            self.state
            is RuntimeState.STOPPED
        )


runtime_lifecycle = RuntimeLifecycle()