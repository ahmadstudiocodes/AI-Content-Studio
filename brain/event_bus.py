"""
Arman StudioOS

brain/event_bus.py

Enterprise Event Bus v1.0
Sprint 05

PART 1
"""


from __future__ import annotations

import time
import uuid
import threading
import traceback
from abc import ABC
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Deque,
)

from brain.retry_manager import RetryManager

from brain.hook_manager import (
    hook_manager,
    BEFORE,
    AFTER,
    ERROR,
)

# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_HISTORY = 1000
DEFAULT_RETRY = 3


# ============================================================
# ENUMS
# ============================================================

class EventPriority(Enum):

    LOW = 0

    NORMAL = 1

    HIGH = 2

    CRITICAL = 3


class EventState(Enum):

    CREATED = "created"

    QUEUED = "queued"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class DispatchMode(Enum):

    SYNC = "sync"

    ASYNC = "async"


# ============================================================
# EXCEPTIONS
# ============================================================

class EventBusError(Exception):
    pass


class DispatchError(EventBusError):
    pass


class SubscriptionError(EventBusError):
    pass


# ============================================================
# DATA MODELS
# ============================================================

@dataclass(slots=True)
class Event:

    name: str

    payload: Dict[str, Any]

    priority: EventPriority = EventPriority.NORMAL

    source: str = "system"

    timestamp: float = field(
        default_factory=time.time
    )

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    state: EventState = EventState.CREATED


@dataclass(slots=True)
class EventResult:

    success: bool = True

    errors: List[str] = field(
        default_factory=list
    )

    handlers: int = 0

    latency: float = 0.0


@dataclass(slots=True)
class EventContext:

    event: Event

    handled: bool = False

    cancelled: bool = False

    trace: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    result: EventResult = field(
        default_factory=EventResult
    )

    def cancel(self):

        self.cancelled = True

        self.event.state = EventState.CANCELLED

    def add_trace(
        self,
        value: str
    ):

        self.trace.append(value)

    def add_error(
        self,
        value: str
    ):

        self.errors.append(value)

        self.result.errors.append(value)

        self.result.success = False


@dataclass(slots=True)
class Subscription:

    handler: Callable

    once: bool = False

    enabled: bool = True

    priority: int = 0

    name: str = ""


@dataclass(slots=True)
class EventStatistics:

    total_events: int = 0

    total_handlers: int = 0

    total_errors: int = 0

    total_latency: float = 0.0

    average_latency: float = 0.0


# ============================================================
# MATCHERS
# ============================================================

class EventMatcher:

    def match(
        self,
        pattern: str,
        event: str
    ) -> bool:

        if pattern == event:
            return True

        if pattern == "*":
            return True

        if pattern.endswith(".*"):

            return event.startswith(
                pattern[:-1]
            )

        return False


# ============================================================
# MIDDLEWARE
# ============================================================

class Middleware(ABC):

    def before(
        self,
        context: EventContext
    ) -> EventContext:

        return context

    def after(
        self,
        context: EventContext
    ) -> EventContext:

        return context


class MiddlewarePipeline:

    def __init__(self):

        self._items = []

    def add(
        self,
        middleware: Middleware
    ):

        self._items.append(
            middleware
        )

    def remove(
        self,
        middleware: Middleware
    ):

        if middleware in self._items:

            self._items.remove(
                middleware
            )

    def before(
        self,
        context: EventContext
    ):

        for middleware in self._items:

            context = middleware.before(
                context
            )

            if context.cancelled:

                return context

        return context

    def after(
        self,
        context: EventContext
    ):

        for middleware in reversed(
            self._items
        ):

            middleware.after(
                context
            )


# ============================================================
# QUEUES
# ============================================================

class EventQueue:

    def __init__(self):

        self._queue: Deque[
            EventContext
        ] = deque()

        self._lock = threading.RLock()

    def push(
        self,
        context: EventContext
    ):

        with self._lock:

            context.event.state = (
                EventState.QUEUED
            )

            self._queue.append(
                context
            )

    def pop(
        self
    ) -> Optional[EventContext]:

        with self._lock:

            if not self._queue:

                return None

            return self._queue.popleft()

    def clear(self):

        with self._lock:

            self._queue.clear()

    def size(self):

        return len(
            self._queue
        )

    def empty(self):

        return len(
            self._queue
        ) == 0


class DeadLetterQueue:

    def __init__(self):

        self.items = []

    def add(
        self,
        context: EventContext
    ):

        self.items.append(
            context
        )


# ============================================================
# DISPATCHER
# ============================================================

class Dispatcher:

    def __init__(
        self,
        bus
    ):

        self.bus = bus

    def dispatch(
        self,
        context: EventContext
    ):

        started = time.perf_counter()

        context.event.state = (
            EventState.RUNNING
        )

        handlers = self.bus._resolve_handlers(
            context.event.name
        )

        try:

            hook_manager.execute(
                BEFORE,
                context
            )

            context = self.bus._pipeline.before(
                context
            )

        except Exception as exc:

            context.event.state = EventState.FAILED

            context.add_error(str(exc))

            context.add_trace("middleware_failed")

            hook_manager.execute(
                ERROR,
                context,
                exc
            )
            
            self.bus._dead_letter.add(
                context
            )

            return

        if context.cancelled:

            return

        called = 0

        for subscription in handlers:

            if not subscription.enabled:

                continue

            try:

                self.bus._retry.execute(

                    subscription.handler,

                    context

                )

                called += 1

                context.handled = True

                context.add_trace(
                    subscription.name
                )

                if subscription.once:

                    self.bus.unsubscribe(

                        context.event.name,

                        subscription.handler

                    )

            except Exception as exc:

                context.add_error(
                    str(exc)
                )

                context.add_trace(
                    traceback.format_exc()
                )

                self.bus._dead_letter.add(
                    context
                )

        self.bus._pipeline.after(
            context
        )

        hook_manager.execute(
                AFTER,
                context
        )

        context.event.state = (
            EventState.COMPLETED
            if context.result.success
            else EventState.FAILED
        )

        latency = (

            time.perf_counter()

            - started

        )

        self.bus._statistics.total_events += 1

        self.bus._statistics.total_handlers += called

        self.bus._statistics.total_errors += len(
            context.errors
        )

        self.bus._statistics.total_latency += latency

        self.bus._statistics.average_latency = (

            self.bus._statistics.total_latency

            /

            self.bus._statistics.total_events

        )

        context.result.handlers = called

        context.result.latency = latency

        self.bus._history.append(
            context
        )


# ============================================================
# EVENT BUS
# ============================================================

class EventBus:

    def __init__(self):

        self._subscriptions = defaultdict(
            list
        )

        self._history = deque(
            maxlen=DEFAULT_HISTORY
        )

        self._queue = EventQueue()

        self._pipeline = MiddlewarePipeline()

        self._retry = RetryManager()

        self._dead_letter = (
            DeadLetterQueue()
        )

        self._statistics = (
            EventStatistics()
        )

        self._matcher = EventMatcher()

        self._dispatcher = Dispatcher(
            self
        )

        self._lock = threading.RLock()

    # ====================================================

    def subscribe(

        self,

        event: str,

        handler: Callable,

        *,

        once=False,

        priority=0

    ):

        subscription = Subscription(

            handler=handler,

            once=once,

            priority=priority,

            enabled=True,

            name=getattr(

                handler,

                "__name__",

                "anonymous"

            )

        )

        with self._lock:

            self._subscriptions[
                event
            ].append(
                subscription
            )

            self._subscriptions[
                event
            ].sort(

                key=lambda x: x.priority,

                reverse=True

            )

        return subscription

    # ====================================================

    def subscribe_once(

        self,

        event,

        handler,

        *,

        priority=0

    ):

        return self.subscribe(

            event,

            handler,

            once=True,

            priority=priority

        )

    # ====================================================

    def unsubscribe(

        self,

        event,

        handler

    ):

        with self._lock:

            self._subscriptions[event] = [

                sub

                for sub in self._subscriptions.get(

                    event,

                    []

                )

                if sub.handler != handler

            ]

    # ====================================================

    def publish(

        self,

        event,

        payload=None,

        *,

        priority=EventPriority.NORMAL,

        source="system"

    ):

        if payload is None:

            payload = {}

        context = EventContext(

            Event(

                name=event,

                payload=payload,

                priority=priority,

                source=source

            )

        )

        self._queue.push(
            context
        )

        self.dispatch()

    # ====================================================

    def dispatch(

        self

    ):

        while not self._queue.empty():

            context = self._queue.pop()

            if context is None:

                break

            self._dispatcher.dispatch(
                context
            )

    # ====================================================
    # Middleware
    # ====================================================

    def add_middleware(
        self,
        middleware: Middleware
    ):

        self._pipeline.add(
            middleware
        )

    def remove_middleware(
        self,
        middleware: Middleware
    ):

        self._pipeline.remove(
            middleware
        )

    # ====================================================
    # Resolver
    # ====================================================

    def _resolve_handlers(
        self,
        event_name: str
    ):

        handlers = []

        handlers.extend(

            self._subscriptions.get(

                event_name,

                []

            )

        )

        for pattern, items in self._subscriptions.items():

            if pattern == event_name:

                continue

            if self._matcher.match(

                pattern,

                event_name

            ):

                handlers.extend(
                    items
                )

        handlers.sort(

            key=lambda item: item.priority,

            reverse=True

        )

        return handlers

    # ====================================================
    # History
    # ====================================================

    def history(self):

        return list(
            self._history
        )

    def clear_history(self):

        self._history.clear()

    # ====================================================
    # Dead Letter Queue
    # ====================================================

    @property
    def dead_letter(self):

        return list(
            self._dead_letter.items
        )

    def clear_dead_letter(self):

        self._dead_letter.items.clear()

    # ====================================================
    # Metrics
    # ====================================================

    @property
    def metrics(self):

        return self._statistics

    def statistics(self):

        return {

            "events":
                self._statistics.total_events,

            "handlers":
                self._statistics.total_handlers,

            "errors":
                self._statistics.total_errors,

            "latency":
                round(

                    self._statistics.average_latency,

                    6

                ),

            "queue":
                self._queue.size(),

            "history":
                len(self._history),

            "dead_letter":
                len(self._dead_letter.items),

            "subscriptions":
                len(self._subscriptions)

        }

    # ====================================================
    # Snapshot
    # ====================================================

    def snapshot(self):

        with self._lock:

            return {

                "subscriptions": {

                    event: [

                        {

                            "handler": sub.name,

                            "priority": sub.priority,

                            "once": sub.once,

                            "enabled": sub.enabled

                        }

                        for sub in items

                    ]

                    for event, items

                    in self._subscriptions.items()

                },

                "metrics": self.statistics(),

                "history": len(
                    self._history
                ),

                "queue": self._queue.size(),

                "dead_letter": len(
                    self._dead_letter.items
                )

            }

    # ====================================================
    # Plugins
    # ====================================================

    def install(
        self,
        plugin
    ):

        if hasattr(
            plugin,
            "register"
        ):

            plugin.register(
                self
            )

    # ====================================================
    # Helpers
    # ====================================================

    def has_subscribers(
        self,
        event: str
    ):

        return (

            len(

                self._resolve_handlers(
                    event
                )

            )

            > 0

        )

    def registered_events(self):

        return sorted(

            self._subscriptions.keys()

        )

    def subscribers(
        self,
        event=None
    ):

        if event is None:

            return {

                key: [

                    sub.name

                    for sub in value

                ]

                for key, value

                in self._subscriptions.items()

            }

        return [

            sub.name

            for sub

            in self._subscriptions.get(

                event,

                []

            )

        ]

    # ====================================================
    # Reset
    # ====================================================

    def reset(self):

        with self._lock:

            self._subscriptions.clear()

            self._history.clear()

            self._queue.clear()

            self._dead_letter.items.clear()

            self._statistics = EventStatistics()

    # ====================================================
    # Shutdown
    # ====================================================

    def shutdown(self):

        self.reset()

    # ====================================================
    # Debug
    # ====================================================

    def __len__(self):

        return len(
            self._history
        )

    def __repr__(self):

        return (

            f"<EventBus "

            f"events={self._statistics.total_events} "

            f"handlers={self._statistics.total_handlers} "

            f"errors={self._statistics.total_errors}>"

        )


# ============================================================
# Singleton
# ============================================================

event_bus = EventBus()