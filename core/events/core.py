# core/events.py
# Part 1

from __future__ import annotations

import json
import time
import uuid
import threading

from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import (
    Any,
    Dict,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Type,
    TypeVar,
    Callable,
)


# ============================================================
# Type Definitions
# ============================================================

EventPayload = MutableMapping[str, Any]

EventMetadataMap = MutableMapping[str, Any]

T = TypeVar("T")


# ============================================================
# Constants
# ============================================================

EVENT_VERSION = "1.0"

DEFAULT_EVENT_SOURCE = "arman"

UTC = timezone.utc


# ============================================================
# Event Enums
# ============================================================


class EventPriority(IntEnum):
    """
    Event execution priority.
    Lower value means higher priority.
    """

    CRITICAL = 0
    HIGH = 10
    NORMAL = 50
    LOW = 90
    BACKGROUND = 100


class EventStatus(str, Enum):
    """
    Current lifecycle state of an event.
    """

    CREATED = "created"

    QUEUED = "queued"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class EventPhase(str, Enum):
    """
    Event execution phase.
    """

    BEFORE = "before"

    MAIN = "main"

    AFTER = "after"


class EventCategory(str, Enum):
    """
    Global event categories.
    """

    SYSTEM = "system"

    WORKSPACE = "workspace"

    SESSION = "session"

    PROJECT = "project"

    ASSET = "asset"

    RUNTIME = "runtime"

    PLUGIN = "plugin"

    AGENT = "agent"

    TRANSACTION = "transaction"

    SECURITY = "security"

    DIAGNOSTIC = "diagnostic"

    CUSTOM = "custom"


# ============================================================
# Event Metadata
# ============================================================


@dataclass(slots=True)
class EventMetadata:
    """
    Additional information attached to events.
    """

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    source: str = DEFAULT_EVENT_SOURCE

    category: EventCategory = EventCategory.SYSTEM

    version: str = EVENT_VERSION

    tags: set[str] = field(
        default_factory=set
    )

    attributes: Dict[str, Any] = field(
        default_factory=dict
    )

    trace_id: str = field(
        default_factory=lambda: uuid.uuid4().hex
    )

    correlation_id: Optional[str] = None


# ============================================================
# Event Context
# ============================================================


@dataclass(slots=True)
class EventContext:
    """
    Runtime context passed during event processing.
    """

    workspace_id: Optional[str] = None

    session_id: Optional[str] = None

    user_id: Optional[str] = None

    runtime_id: Optional[str] = None

    request_id: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def update(
        self,
        values: Mapping[str, Any],
    ) -> None:

        self.metadata.update(values)

# core/events.py
# Part 1 — Continued
# EventHeader, BaseEvent, Serialization Support


# ============================================================
# Event Headers
# ============================================================


@dataclass(slots=True)
class EventHeaders:
    """
    Transport-level event headers.

    Used for routing, tracing and communication
    between internal StudioOS components.
    """

    event_id: str = field(
        default_factory=lambda: uuid.uuid4().hex
    )

    event_type: str = ""

    created_timestamp: float = field(
        default_factory=time.time
    )

    priority: EventPriority = EventPriority.NORMAL

    phase: EventPhase = EventPhase.MAIN

    status: EventStatus = EventStatus.CREATED

    retry_count: int = 0

    max_retries: int = 0

    parent_event_id: Optional[str] = None


# ============================================================
# Base Event
# ============================================================


@dataclass(slots=True)
class BaseEvent:
    """
    Base event model used across Arman StudioOS.

    Every internal event should inherit from this class.
    """

    name: str

    payload: EventPayload = field(
        default_factory=dict
    )

    context: EventContext = field(
        default_factory=EventContext
    )

    metadata: EventMetadata = field(
        default_factory=EventMetadata
    )

    headers: EventHeaders = field(
        default_factory=EventHeaders
    )


    def __post_init__(self) -> None:

        if not self.name:

            raise ValueError(
                "Event name cannot be empty"
            )

        if not isinstance(
            self.payload,
            dict,
        ):

            raise TypeError(
                "Event payload must be a dictionary"
            )

        self.headers.event_type = self.name


    @property
    def id(self) -> str:
        """
        Returns unique event identifier.
        """

        return self.headers.event_id


    @property
    def priority(self) -> EventPriority:
        """
        Returns event priority.
        """

        return self.headers.priority


    @property
    def status(self) -> EventStatus:
        """
        Returns current event status.
        """

        return self.headers.status


    def set_status(
        self,
        status: EventStatus,
    ) -> None:
        """
        Update lifecycle status.
        """

        self.headers.status = status


    def add_tag(
        self,
        tag: str,
    ) -> None:
        """
        Add metadata tag.
        """

        self.metadata.tags.add(tag)


    def has_tag(
        self,
        tag: str,
    ) -> bool:
        """
        Check metadata tag.
        """

        return tag in self.metadata.tags


# ============================================================
# Event Conversion
# ============================================================


class EventSerializer:
    """
    Serialize and deserialize events.

    Used by:
    - Event Bus
    - Persistence Layer
    - Debugging
    - Distributed communication
    """

    @staticmethod
    def to_dict(
        event: BaseEvent,
    ) -> Dict[str, Any]:

        return {
            "name": event.name,
            "payload": event.payload,
            "context": asdict(
                event.context
            ),
            "metadata": asdict(
                event.metadata
            ),
            "headers": {
                **asdict(
                    event.headers
                ),
                "priority":
                    event.headers.priority.name,
                "phase":
                    event.headers.phase.value,
                "status":
                    event.headers.status.value,
            },
        }


    @staticmethod
    def to_json(
        event: BaseEvent,
    ) -> str:

        return json.dumps(
            EventSerializer.to_dict(event),
            default=str,
            ensure_ascii=False,
        )


    @staticmethod
    def from_dict(
        data: Mapping[str, Any],
        event_class: Type[T] = BaseEvent,
    ) -> T:

        headers_data = data.get(
            "headers",
            {},
        )

        metadata_data = data.get(
            "metadata",
            {},
        )

        context_data = data.get(
            "context",
            {},
        )


        event = event_class(
            name=data["name"],
            payload=dict(
                data.get(
                    "payload",
                    {},
                )
            ),
            context=EventContext(
                **context_data
            ),
            metadata=EventMetadata(
                **metadata_data
            ),
            headers=EventHeaders(
                **{
                    key: value
                    for key, value
                    in headers_data.items()
                    if key in EventHeaders.__dataclass_fields__
                }
            ),
        )


        return event


    @staticmethod
    def from_json(
        value: str,
        event_class: Type[T] = BaseEvent,
    ) -> T:

        data = json.loads(value)

        return EventSerializer.from_dict(
            data,
            event_class,
        )
    
# core/events.py
# Part 1 — Continued
# Event Factory, Registry and Validation


# ============================================================
# Event Factory
# ============================================================


class EventFactory:
    """
    Central factory for creating StudioOS events.

    Provides a unified creation point so future
    runtime, plugin and distributed systems can
    create events consistently.
    """

    @staticmethod
    def create(
        name: str,
        payload: Optional[Mapping[str, Any]] = None,
        *,
        context: Optional[EventContext] = None,
        category: EventCategory = EventCategory.SYSTEM,
        priority: EventPriority = EventPriority.NORMAL,
        source: str = DEFAULT_EVENT_SOURCE,
        tags: Optional[Iterable[str]] = None,
    ) -> BaseEvent:
        """
        Create a new BaseEvent instance.
        """

        metadata = EventMetadata(
            source=source,
            category=category,
        )

        if tags:

            metadata.tags.update(
                tags
            )


        headers = EventHeaders(
            priority=priority,
        )


        return BaseEvent(
            name=name,
            payload=dict(
                payload or {}
            ),
            context=context or EventContext(),
            metadata=metadata,
            headers=headers,
        )


# ============================================================
# Event Registry
# ============================================================


class EventRegistry:
    """
    Registry of known event types.

    Used by:
    - Plugin system
    - Runtime discovery
    - Serialization
    - Validation
    """

    def __init__(self) -> None:

        self._events: Dict[
            str,
            Type[BaseEvent]
        ] = {}

        self._lock = threading.RLock()


    def register(
        self,
        name: str,
        event_type: Type[BaseEvent],
    ) -> None:
        """
        Register an event class.
        """

        if not issubclass(
            event_type,
            BaseEvent,
        ):

            raise TypeError(
                "Event type must inherit from BaseEvent"
            )


        with self._lock:

            self._events[name] = event_type



    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove event registration.
        """

        with self._lock:

            self._events.pop(
                name,
                None,
            )



    def resolve(
        self,
        name: str,
    ) -> Optional[Type[BaseEvent]]:
        """
        Resolve event class.
        """

        with self._lock:

            return self._events.get(
                name
            )



    def contains(
        self,
        name: str,
    ) -> bool:

        with self._lock:

            return name in self._events



    def list_events(
        self,
    ) -> list[str]:

        with self._lock:

            return list(
                self._events.keys()
            )


# ============================================================
# Event Validator
# ============================================================


class EventValidator:
    """
    Validates events before dispatch.

    Keeps invalid events away from
    Runtime and EventBus layers.
    """

    REQUIRED_FIELDS = {
        "name",
        "payload",
        "headers",
        "metadata",
    }


    @classmethod
    def validate(
        cls,
        event: BaseEvent,
    ) -> bool:
        """
        Validate event structure.
        """

        if not isinstance(
            event,
            BaseEvent,
        ):

            raise TypeError(
                "Invalid event instance"
            )


        for field_name in cls.REQUIRED_FIELDS:

            if not hasattr(
                event,
                field_name,
            ):

                raise ValueError(
                    f"Missing event field: {field_name}"
                )


        if not event.name.strip():

            raise ValueError(
                "Event name cannot be empty"
            )


        if not isinstance(
            event.payload,
            dict,
        ):

            raise TypeError(
                "Payload must be dictionary"
            )


        return True


# ============================================================
# Global Event Registry Instance
# ============================================================


event_registry = EventRegistry()

# core/events.py
# Part 1 — Continued
# Specialized Events and Event Utilities


# ============================================================
# Specialized Event Types
# ============================================================


@dataclass(slots=True)
class CancelableEvent(BaseEvent):
    """
    Event that can be cancelled during processing.

    Used by:
    - Hooks
    - Permissions
    - Validation pipelines
    - Runtime interceptors
    """

    cancelled: bool = False

    cancel_reason: Optional[str] = None


    def cancel(
        self,
        reason: Optional[str] = None,
    ) -> None:
        """
        Cancel event execution.
        """

        self.cancelled = True

        self.cancel_reason = reason

        self.headers.status = (
            EventStatus.CANCELLED
        )



    def is_cancelled(
        self,
    ) -> bool:
        """
        Check cancellation state.
        """

        return self.cancelled



# ============================================================
# Result Event
# ============================================================


@dataclass(slots=True)
class ResultEvent(BaseEvent):
    """
    Event containing execution result.
    """

    success: bool = True

    result: Any = None

    error: Optional[str] = None


    def fail(
        self,
        message: str,
    ) -> None:
        """
        Mark result as failed.
        """

        self.success = False

        self.error = message

        self.headers.status = (
            EventStatus.FAILED
        )



# ============================================================
# Error Event
# ============================================================


@dataclass(slots=True)
class ErrorEvent(BaseEvent):
    """
    Event used for system errors
    and diagnostics reporting.
    """

    error_type: str = ""

    message: str = ""

    traceback: Optional[str] = None

    recoverable: bool = False



# ============================================================
# Event Utilities
# ============================================================


class EventUtils:
    """
    Helper methods for event operations.
    """

    @staticmethod
    def clone(
        event: BaseEvent,
    ) -> BaseEvent:
        """
        Create a copy of an event
        with a new identity.
        """

        return BaseEvent(
            name=event.name,
            payload=dict(
                event.payload
            ),
            context=EventContext(
                workspace_id=
                    event.context.workspace_id,
                session_id=
                    event.context.session_id,
                user_id=
                    event.context.user_id,
                runtime_id=
                    event.context.runtime_id,
                request_id=
                    event.context.request_id,
                metadata=dict(
                    event.context.metadata
                ),
            ),
            metadata=EventMetadata(
                source=
                    event.metadata.source,
                category=
                    event.metadata.category,
                version=
                    event.metadata.version,
                tags=set(
                    event.metadata.tags
                ),
                attributes=dict(
                    event.metadata.attributes
                ),
                correlation_id=
                    event.metadata.correlation_id,
            ),
            headers=EventHeaders(
                priority=
                    event.headers.priority,
                phase=
                    event.headers.phase,
                max_retries=
                    event.headers.max_retries,
                parent_event_id=
                    event.headers.event_id,
            ),
        )


    @staticmethod
    def elapsed(
        event: BaseEvent,
    ) -> float:
        """
        Return time elapsed since creation.
        """

        return (
            time.time()
            -
            event.headers.created_timestamp
        )



    @staticmethod
    def mark_processing(
        event: BaseEvent,
    ) -> None:
        """
        Set event state to processing.
        """

        event.headers.status = (
            EventStatus.PROCESSING
        )



    @staticmethod
    def mark_completed(
        event: BaseEvent,
    ) -> None:
        """
        Set event state to completed.
        """

        event.headers.status = (
            EventStatus.COMPLETED
        )



# ============================================================
# Default Event Types Registration
# ============================================================


event_registry.register(
    "base",
    BaseEvent,
)

event_registry.register(
    "cancelable",
    CancelableEvent,
)

event_registry.register(
    "result",
    ResultEvent,
)

event_registry.register(
    "error",
    ErrorEvent,
)

# core/events.py
# Part 2
# Event Routing, Matching and Runtime Support


# ============================================================
# Event Matcher
# ============================================================


class EventMatcher:
    """
    Provides event matching utilities.

    Used by:
    - Observer system
    - Event Bus
    - Plugin filters
    - Runtime hooks
    """

    @staticmethod
    def match_name(
        event: BaseEvent,
        pattern: str,
    ) -> bool:
        """
        Match event name against wildcard pattern.
        """

        import fnmatch

        return fnmatch.fnmatch(
            event.name,
            pattern,
        )


    @staticmethod
    def match_category(
        event: BaseEvent,
        category: EventCategory,
    ) -> bool:
        """
        Match event category.
        """

        return (
            event.metadata.category
            ==
            category
        )


    @staticmethod
    def match_source(
        event: BaseEvent,
        source: str,
    ) -> bool:
        """
        Match event source.
        """

        return (
            event.metadata.source
            ==
            source
        )


    @staticmethod
    def match_tags(
        event: BaseEvent,
        tags: Iterable[str],
    ) -> bool:
        """
        Check whether event contains tags.
        """

        required = set(tags)

        return required.issubset(
            event.metadata.tags
        )



# ============================================================
# Event Envelope
# ============================================================


@dataclass(slots=True)
class EventEnvelope:
    """
    Wrapper around events when transported
    between internal systems.

    Used for:
    - EventBus
    - Queues
    - Runtime messaging
    """

    event: BaseEvent

    destination: Optional[str] = None

    created_at: float = field(
        default_factory=time.time
    )

    delivered: bool = False

    delivery_attempts: int = 0


    def mark_delivered(
        self,
    ) -> None:
        """
        Mark successful delivery.
        """

        self.delivered = True



# ============================================================
# Event Batch
# ============================================================


@dataclass(slots=True)
class EventBatch:
    """
    Group of events processed together.
    """

    events: list[BaseEvent] = field(
        default_factory=list
    )

    batch_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    created_at: float = field(
        default_factory=time.time
    )


    def add(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Add event to batch.
        """

        EventValidator.validate(
            event
        )

        self.events.append(
            event
        )


    def size(
        self,
    ) -> int:

        return len(
            self.events
        )



# ============================================================
# Event Lifecycle Manager
# ============================================================


class EventLifecycle:
    """
    Manages event state transitions.
    """

    VALID_TRANSITIONS = {

        EventStatus.CREATED: {
            EventStatus.QUEUED,
            EventStatus.CANCELLED,
        },

        EventStatus.QUEUED: {
            EventStatus.PROCESSING,
            EventStatus.CANCELLED,
        },

        EventStatus.PROCESSING: {
            EventStatus.COMPLETED,
            EventStatus.FAILED,
            EventStatus.CANCELLED,
        },

        EventStatus.COMPLETED: set(),

        EventStatus.FAILED: {
            EventStatus.QUEUED,
        },

        EventStatus.CANCELLED: set(),
    }


    @classmethod
    def transition(
        cls,
        event: BaseEvent,
        new_status: EventStatus,
    ) -> None:
        """
        Perform validated lifecycle transition.
        """

        current = event.headers.status

        allowed = cls.VALID_TRANSITIONS.get(
            current,
            set(),
        )

        if new_status not in allowed:

            raise ValueError(
                f"Invalid event transition "
                f"{current.value} -> {new_status.value}"
            )


        event.headers.status = new_status



    @classmethod
    def can_transition(
        cls,
        current: EventStatus,
        target: EventStatus,
    ) -> bool:

        return target in cls.VALID_TRANSITIONS.get(
            current,
            set(),
        )
    
# core/events.py
# Part 2 — Continued
# Event Execution Context and Listener Support


# ============================================================
# Event Execution Result
# ============================================================


@dataclass(slots=True)
class EventExecutionResult:
    """
    Result returned after event processing.
    """

    event_id: str

    success: bool = True

    value: Any = None

    error: Optional[Exception] = None

    execution_time: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


    @classmethod
    def success_result(
        cls,
        event: BaseEvent,
        value: Any = None,
        execution_time: float = 0.0,
    ) -> "EventExecutionResult":
        """
        Create successful execution result.
        """

        return cls(
            event_id=event.id,
            success=True,
            value=value,
            execution_time=execution_time,
        )


    @classmethod
    def failure_result(
        cls,
        event: BaseEvent,
        error: Exception,
        execution_time: float = 0.0,
    ) -> "EventExecutionResult":
        """
        Create failed execution result.
        """

        return cls(
            event_id=event.id,
            success=False,
            error=error,
            execution_time=execution_time,
        )



# ============================================================
# Event Listener Protocol
# ============================================================


class EventListener:
    """
    Base listener abstraction.

    Components such as:
    - Workspace Observer
    - Runtime Hooks
    - Plugins
    - Agents

    can implement this interface.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self.name = name

        self.enabled = True



    def enable(
        self,
    ) -> None:
        """
        Enable listener.
        """

        self.enabled = True



    def disable(
        self,
    ) -> None:
        """
        Disable listener.
        """

        self.enabled = False



    def accepts(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Determine whether listener
        accepts an event.

        Override in subclasses.
        """

        return True



    def handle(
        self,
        event: BaseEvent,
    ) -> Optional[Any]:
        """
        Process event.

        Override in subclasses.
        """

        raise NotImplementedError(
            "Listener must implement handle()"
        )



# ============================================================
# Event Subscription
# ============================================================


@dataclass(slots=True)
class EventSubscription:
    """
    Represents an event listener subscription.
    """

    event_pattern: str

    listener: EventListener

    priority: EventPriority = (
        EventPriority.NORMAL
    )

    active: bool = True


    def matches(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Check subscription match.
        """

        if not self.active:

            return False


        return EventMatcher.match_name(
            event,
            self.event_pattern,
        )



    def cancel(
        self,
    ) -> None:
        """
        Disable subscription.
        """

        self.active = False



# ============================================================
# Event Dispatcher Helper
# ============================================================


class EventDispatcher:
    """
    Lightweight internal dispatcher.

    This class is not the final EventBus.
    It provides basic dispatching support
    for Observer and Hook systems.
    """

    def __init__(
        self,
    ) -> None:

        self._subscriptions: list[
            EventSubscription
        ] = []


    def subscribe(
        self,
        subscription: EventSubscription,
    ) -> None:
        """
        Add subscription.
        """

        self._subscriptions.append(
            subscription
        )

        self._subscriptions.sort(
            key=lambda item:
                item.priority.value
        )



    def unsubscribe(
        self,
        subscription: EventSubscription,
    ) -> None:
        """
        Remove subscription.
        """

        if subscription in self._subscriptions:

            self._subscriptions.remove(
                subscription
            )



    def dispatch(
        self,
        event: BaseEvent,
    ) -> list[Any]:
        """
        Dispatch event to listeners.
        """

        results: list[Any] = []


        for subscription in list(
            self._subscriptions
        ):

            if not subscription.matches(
                event
            ):

                continue


            if not subscription.listener.enabled:

                continue


            if not subscription.listener.accepts(
                event
            ):

                continue


            result = subscription.listener.handle(
                event
            )

            results.append(
                result
            )


        return results
    
# core/events.py
# Part 2 — Continued
# Event Metrics, Tracing and Debug Support


# ============================================================
# Event Trace Record
# ============================================================


@dataclass(slots=True)
class EventTraceRecord:
    """
    Stores execution trace information.

    Used by:
    - Diagnostics
    - Performance monitoring
    - Debugging
    - Runtime analysis
    """

    event_id: str

    event_name: str

    started_at: float = field(
        default_factory=time.time
    )

    finished_at: Optional[float] = None

    handler: Optional[str] = None

    status: EventStatus = EventStatus.CREATED

    details: Dict[str, Any] = field(
        default_factory=dict
    )


    def finish(
        self,
        status: EventStatus = EventStatus.COMPLETED,
    ) -> None:
        """
        Complete trace record.
        """

        self.finished_at = time.time()

        self.status = status



    @property
    def duration(
        self,
    ) -> float:
        """
        Return execution duration.
        """

        end = (
            self.finished_at
            or
            time.time()
        )

        return (
            end
            -
            self.started_at
        )



# ============================================================
# Event Tracer
# ============================================================


class EventTracer:
    """
    Lightweight in-memory event tracer.

    Designed to later integrate with:
    - Metrics system
    - Observability layer
    - Logging backend
    """

    def __init__(
        self,
        max_records: int = 10000,
    ) -> None:

        self.max_records = max_records

        self._records: list[
            EventTraceRecord
        ] = []

        self._lock = threading.RLock()



    def start(
        self,
        event: BaseEvent,
        handler: Optional[str] = None,
    ) -> EventTraceRecord:
        """
        Start tracing event execution.
        """

        record = EventTraceRecord(
            event_id=event.id,
            event_name=event.name,
            handler=handler,
        )


        with self._lock:

            self._records.append(
                record
            )

            self._trim()


        return record



    def complete(
        self,
        record: EventTraceRecord,
        status: EventStatus =
            EventStatus.COMPLETED,
    ) -> None:
        """
        Finish trace.
        """

        record.finish(
            status
        )



    def _trim(
        self,
    ) -> None:
        """
        Keep memory usage controlled.
        """

        overflow = (
            len(self._records)
            -
            self.max_records
        )


        if overflow > 0:

            del self._records[
                :overflow
            ]



    def get_records(
        self,
    ) -> list[EventTraceRecord]:
        """
        Return trace history.
        """

        with self._lock:

            return list(
                self._records
            )



# ============================================================
# Event Statistics
# ============================================================


@dataclass(slots=True)
class EventStatistics:
    """
    Runtime statistics for events.
    """

    total_events: int = 0

    completed_events: int = 0

    failed_events: int = 0

    cancelled_events: int = 0

    total_execution_time: float = 0.0


    def record(
        self,
        result: EventExecutionResult,
    ) -> None:
        """
        Update statistics.
        """

        self.total_events += 1

        self.total_execution_time += (
            result.execution_time
        )


        if result.success:

            self.completed_events += 1

        else:

            self.failed_events += 1



    @property
    def average_execution_time(
        self,
    ) -> float:
        """
        Calculate average execution time.
        """

        if self.total_events == 0:

            return 0.0


        return (
            self.total_execution_time
            /
            self.total_events
        )



# ============================================================
# Global Tracer Instance
# ============================================================


event_tracer = EventTracer()

event_statistics = EventStatistics()

# core/events.py
# Part 2 — Continued
# Event Manager and Public API Support


# ============================================================
# Event Manager
# ============================================================


class EventManager:
    """
    High-level event lifecycle manager.

    Coordinates:
    - Validation
    - Tracing
    - Dispatching
    - Statistics
    """

    def __init__(
        self,
        dispatcher: Optional[
            EventDispatcher
        ] = None,
    ) -> None:

        self.dispatcher = (
            dispatcher
            or
            EventDispatcher()
        )

        self.tracer = event_tracer

        self.statistics = event_statistics



    def emit(
        self,
        event: BaseEvent,
    ) -> list[Any]:
        """
        Validate and dispatch event.
        """

        EventValidator.validate(
            event
        )


        EventLifecycle.transition(
            event,
            EventStatus.QUEUED,
        )


        trace = self.tracer.start(
            event
        )


        start = time.perf_counter()


        try:

            EventLifecycle.transition(
                event,
                EventStatus.PROCESSING,
            )


            results = self.dispatcher.dispatch(
                event
            )


            EventLifecycle.transition(
                event,
                EventStatus.COMPLETED,
            )


            elapsed = (
                time.perf_counter()
                -
                start
            )


            execution = (
                EventExecutionResult.success_result(
                    event,
                    value=results,
                    execution_time=elapsed,
                )
            )


            self.statistics.record(
                execution
            )


            self.tracer.complete(
                trace,
                EventStatus.COMPLETED,
            )


            return results


        except Exception as exc:

            EventLifecycle.transition(
                event,
                EventStatus.FAILED,
            )


            elapsed = (
                time.perf_counter()
                -
                start
            )


            execution = (
                EventExecutionResult.failure_result(
                    event,
                    exc,
                    elapsed,
                )
            )


            self.statistics.record(
                execution
            )


            self.tracer.complete(
                trace,
                EventStatus.FAILED,
            )


            raise



# ============================================================
# Event Builder
# ============================================================


class EventBuilder:
    """
    Fluent builder for creating events.

    Example:

    event = (
        EventBuilder("workspace.open")
        .payload(id="123")
        .priority(EventPriority.HIGH)
        .build()
    )
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self._name = name

        self._payload: EventPayload = {}

        self._context = EventContext()

        self._category = (
            EventCategory.SYSTEM
        )

        self._priority = (
            EventPriority.NORMAL
        )

        self._tags: set[str] = set()



    def payload(
        self,
        **values: Any,
    ) -> "EventBuilder":

        self._payload.update(
            values
        )

        return self



    def context(
        self,
        context: EventContext,
    ) -> "EventBuilder":

        self._context = context

        return self



    def category(
        self,
        category: EventCategory,
    ) -> "EventBuilder":

        self._category = category

        return self



    def priority(
        self,
        priority: EventPriority,
    ) -> "EventBuilder":

        self._priority = priority

        return self



    def tag(
        self,
        value: str,
    ) -> "EventBuilder":

        self._tags.add(
            value
        )

        return self



    def build(
        self,
    ) -> BaseEvent:

        return EventFactory.create(
            name=self._name,
            payload=self._payload,
            context=self._context,
            category=self._category,
            priority=self._priority,
            tags=self._tags,
        )



# ============================================================
# Global Event Manager
# ============================================================


event_manager = EventManager()

# core/events.py
# Part 2 — Continued
# Async Compatibility, Event Hooks and Final Utilities


# ============================================================
# Async Event Support
# ============================================================


class AsyncEventListener(EventListener):
    """
    Base async-compatible event listener.

    Runtime systems can inherit this class
    when asynchronous execution is required.
    """

    async def handle_async(
        self,
        event: BaseEvent,
    ) -> Optional[Any]:
        """
        Async event handler.

        Override in subclasses.
        """

        raise NotImplementedError(
            "Async listener must implement handle_async()"
        )



# ============================================================
# Event Hook
# ============================================================


@dataclass(slots=True)
class EventHook:
    """
    Hook executed around event lifecycle.

    Used by:
    - Runtime hooks
    - Permission layer
    - Monitoring
    - Transaction system
    """

    name: str

    before: Optional[
        Callable[[BaseEvent], None]
    ] = None

    after: Optional[
        Callable[[BaseEvent], None]
    ] = None

    enabled: bool = True



    def execute_before(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Execute before callback.
        """

        if (
            self.enabled
            and
            self.before
        ):

            self.before(
                event
            )



    def execute_after(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Execute after callback.
        """

        if (
            self.enabled
            and
            self.after
        ):

            self.after(
                event
            )



# ============================================================
# Event Hook Manager
# ============================================================


class EventHookManager:
    """
    Manages event lifecycle hooks.
    """

    def __init__(
        self,
    ) -> None:

        self._hooks: list[
            EventHook
        ] = []

        self._lock = threading.RLock()



    def register(
        self,
        hook: EventHook,
    ) -> None:
        """
        Register a hook.
        """

        with self._lock:

            self._hooks.append(
                hook
            )



    def remove(
        self,
        hook: EventHook,
    ) -> None:
        """
        Remove hook.
        """

        with self._lock:

            if hook in self._hooks:

                self._hooks.remove(
                    hook
                )



    def before(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Execute before hooks.
        """

        for hook in list(
            self._hooks
        ):

            hook.execute_before(
                event
            )



    def after(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Execute after hooks.
        """

        for hook in list(
            self._hooks
        ):

            hook.execute_after(
                event
            )



# ============================================================
# Event ID Generator
# ============================================================


class EventIdGenerator:
    """
    Generates unique event identifiers.
    """

    @staticmethod
    def generate(
        prefix: str = "evt",
    ) -> str:
        """
        Create unique identifier.
        """

        return (
            f"{prefix}_"
            f"{uuid.uuid4().hex}"
        )



# ============================================================
# Event Debug Formatter
# ============================================================


class EventDebugFormatter:
    """
    Human-readable event formatting.
    """

    @staticmethod
    def format(
        event: BaseEvent,
    ) -> str:
        """
        Convert event to debug string.
        """

        return (
            f"Event("
            f"id={event.id}, "
            f"name={event.name}, "
            f"status={event.status.value}, "
            f"priority={event.priority.name}"
            f")"
        )



# ============================================================
# Global Hook Manager
# ============================================================


event_hook_manager = EventHookManager()

# core/events.py
# Part 2 — Continued
# Event Context Management, Filtering and Diagnostics


# ============================================================
# Event Filter
# ============================================================


@dataclass(slots=True)
class EventFilter:
    """
    Defines filtering rules for events.

    Used by:
    - Observer System
    - Plugin Manager
    - Runtime Monitoring
    """

    names: set[str] = field(
        default_factory=set
    )

    categories: set[EventCategory] = field(
        default_factory=set
    )

    priorities: set[EventPriority] = field(
        default_factory=set
    )

    sources: set[str] = field(
        default_factory=set
    )

    tags: set[str] = field(
        default_factory=set
    )


    def matches(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Check whether event matches filter.
        """

        if self.names:

            if event.name not in self.names:

                return False


        if self.categories:

            if (
                event.metadata.category
                not in self.categories
            ):

                return False


        if self.priorities:

            if (
                event.priority
                not in self.priorities
            ):

                return False


        if self.sources:

            if (
                event.metadata.source
                not in self.sources
            ):

                return False


        if self.tags:

            if not self.tags.issubset(
                event.metadata.tags
            ):

                return False


        return True



# ============================================================
# Event Context Manager
# ============================================================


class EventContextManager:
    """
    Provides helpers for managing
    event execution contexts.
    """

    @staticmethod
    def create(
        *,
        workspace_id: Optional[str] = None,
        session_id: Optional[str] = None,
        runtime_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> EventContext:
        """
        Create runtime context.
        """

        return EventContext(
            workspace_id=workspace_id,
            session_id=session_id,
            runtime_id=runtime_id,
            user_id=user_id,
        )


    @staticmethod
    def clone(
        context: EventContext,
    ) -> EventContext:
        """
        Clone context.
        """

        return EventContext(
            workspace_id=context.workspace_id,
            session_id=context.session_id,
            runtime_id=context.runtime_id,
            user_id=context.user_id,
            request_id=context.request_id,
            metadata=dict(
                context.metadata
            ),
        )



# ============================================================
# Event Diagnostics
# ============================================================


@dataclass(slots=True)
class EventDiagnostic:
    """
    Diagnostic information for an event.
    """

    event_id: str

    event_name: str

    status: EventStatus

    created_at: datetime

    messages: list[str] = field(
        default_factory=list
    )

    data: Dict[str, Any] = field(
        default_factory=dict
    )


    def add_message(
        self,
        message: str,
    ) -> None:

        self.messages.append(
            message
        )



class EventDiagnostics:
    """
    Collects diagnostic information.
    """

    def __init__(
        self,
    ) -> None:

        self._items: Dict[
            str,
            EventDiagnostic
        ] = {}

        self._lock = threading.RLock()



    def create(
        self,
        event: BaseEvent,
    ) -> EventDiagnostic:
        """
        Create diagnostic record.
        """

        diagnostic = EventDiagnostic(
            event_id=event.id,
            event_name=event.name,
            status=event.status,
            created_at=datetime.now(UTC),
        )


        with self._lock:

            self._items[event.id] = diagnostic


        return diagnostic



    def get(
        self,
        event_id: str,
    ) -> Optional[EventDiagnostic]:
        """
        Retrieve diagnostic.
        """

        with self._lock:

            return self._items.get(
                event_id
            )



    def remove(
        self,
        event_id: str,
    ) -> None:

        with self._lock:

            self._items.pop(
                event_id,
                None,
            )



# ============================================================
# Global Diagnostics Instance
# ============================================================


event_diagnostics = EventDiagnostics()

# core/events.py
# Part 3
# Event Persistence, Snapshot and Recovery Support


# ============================================================
# Event Snapshot
# ============================================================


@dataclass(slots=True)
class EventSnapshot:
    """
    Serializable snapshot of an event.

    Used by:
    - Recovery system
    - Persistence layer
    - Debug sessions
    """

    event_id: str

    event_name: str

    payload: Dict[str, Any]

    status: EventStatus

    created_at: float

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    headers: Dict[str, Any] = field(
        default_factory=dict
    )


    @classmethod
    def from_event(
        cls,
        event: BaseEvent,
    ) -> "EventSnapshot":
        """
        Create snapshot from event.
        """

        return cls(
            event_id=event.id,
            event_name=event.name,
            payload=dict(
                event.payload
            ),
            status=event.status,
            created_at=(
                event.headers.created_timestamp
            ),
            metadata=asdict(
                event.metadata
            ),
            headers=asdict(
                event.headers
            ),
        )



    def restore(
        self,
    ) -> BaseEvent:
        """
        Restore event from snapshot.
        """

        return BaseEvent(
            name=self.event_name,
            payload=dict(
                self.payload
            ),
            metadata=EventMetadata(
                **{
                    key: value
                    for key, value
                    in self.metadata.items()
                    if key
                    in EventMetadata.__dataclass_fields__
                }
            ),
            headers=EventHeaders(
                **{
                    key: value
                    for key, value
                    in self.headers.items()
                    if key
                    in EventHeaders.__dataclass_fields__
                }
            ),
        )



# ============================================================
# Event Store
# ============================================================


class EventStore:
    """
    In-memory event storage.

    Later can be replaced by:
    - SQLite
    - PostgreSQL
    - Redis
    - Distributed storage
    """

    def __init__(
        self,
        max_events: int = 50000,
    ) -> None:

        self.max_events = max_events

        self._events: Dict[
            str,
            EventSnapshot
        ] = {}

        self._lock = threading.RLock()



    def save(
        self,
        event: BaseEvent,
    ) -> EventSnapshot:
        """
        Store event snapshot.
        """

        snapshot = EventSnapshot.from_event(
            event
        )


        with self._lock:

            self._events[
                snapshot.event_id
            ] = snapshot


            self._cleanup()


        return snapshot



    def get(
        self,
        event_id: str,
    ) -> Optional[EventSnapshot]:
        """
        Retrieve snapshot.
        """

        with self._lock:

            return self._events.get(
                event_id
            )



    def delete(
        self,
        event_id: str,
    ) -> None:

        with self._lock:

            self._events.pop(
                event_id,
                None,
            )



    def list_all(
        self,
    ) -> list[EventSnapshot]:

        with self._lock:

            return list(
                self._events.values()
            )



    def _cleanup(
        self,
    ) -> None:

        overflow = (
            len(self._events)
            -
            self.max_events
        )


        if overflow <= 0:

            return


        keys = list(
            self._events.keys()
        )


        for key in keys[:overflow]:

            del self._events[key]



# ============================================================
# Event Recovery Manager
# ============================================================


class EventRecoveryManager:
    """
    Handles failed event recovery.

    Provides retry preparation for:
    - Runtime
    - Transactions
    - Workers
    """

    def __init__(
        self,
        store: EventStore,
    ) -> None:

        self.store = store



    def recover(
        self,
        event_id: str,
    ) -> Optional[BaseEvent]:
        """
        Restore event from storage.
        """

        snapshot = self.store.get(
            event_id
        )


        if snapshot is None:

            return None


        event = snapshot.restore()


        event.headers.status = (
            EventStatus.QUEUED
        )


        event.headers.retry_count += 1


        return event



# ============================================================
# Global Event Storage
# ============================================================


event_store = EventStore()

event_recovery = EventRecoveryManager(
    event_store
)

# core/events.py
# Part 3 — Continued
# Event Queue, Retry Policy and Dead Letter Support


# ============================================================
# Event Retry Policy
# ============================================================


@dataclass(slots=True)
class EventRetryPolicy:
    """
    Defines retry behavior for failed events.
    """

    max_attempts: int = 3

    delay_seconds: float = 1.0

    exponential_backoff: bool = True


    def can_retry(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Check retry availability.
        """

        return (
            event.headers.retry_count
            <
            self.max_attempts
        )



    def next_delay(
        self,
        event: BaseEvent,
    ) -> float:
        """
        Calculate next retry delay.
        """

        if not self.exponential_backoff:

            return self.delay_seconds


        return (
            self.delay_seconds
            *
            (
                2
                **
                event.headers.retry_count
            )
        )



# ============================================================
# Dead Letter Event
# ============================================================


@dataclass(slots=True)
class DeadLetterEvent:
    """
    Stores permanently failed events.
    """

    event: BaseEvent

    reason: str

    failed_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Dead Letter Queue
# ============================================================


class DeadLetterQueue:
    """
    Storage for unrecoverable events.
    """

    def __init__(
        self,
    ) -> None:

        self._items: list[
            DeadLetterEvent
        ] = []

        self._lock = threading.RLock()



    def push(
        self,
        event: BaseEvent,
        reason: str,
    ) -> None:
        """
        Add failed event.
        """

        item = DeadLetterEvent(
            event=event,
            reason=reason,
        )


        with self._lock:

            self._items.append(
                item
            )



    def list(
        self,
    ) -> list[DeadLetterEvent]:

        with self._lock:

            return list(
                self._items
            )



    def clear(
        self,
    ) -> None:

        with self._lock:

            self._items.clear()



# ============================================================
# Event Queue Item
# ============================================================


@dataclass(slots=True)
class EventQueueItem:
    """
    Internal queue representation.
    """

    event: BaseEvent

    inserted_at: float = field(
        default_factory=time.time
    )

    attempts: int = 0



# ============================================================
# Event Queue
# ============================================================


class EventQueue:
    """
    Thread-safe event queue.

    Used internally by runtime
    and asynchronous processors.
    """

    def __init__(
        self,
    ) -> None:

        self._items: list[
            EventQueueItem
        ] = []

        self._condition = (
            threading.Condition()
        )



    def push(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Insert event.
        """

        item = EventQueueItem(
            event=event
        )


        with self._condition:

            self._items.append(
                item
            )

            self._condition.notify()



    def pop(
        self,
        timeout: Optional[float] = None,
    ) -> Optional[EventQueueItem]:
        """
        Remove next event.
        """

        with self._condition:

            if not self._items:

                self._condition.wait(
                    timeout
                )


            if not self._items:

                return None


            return self._items.pop(
                0
            )



    def size(
        self,
    ) -> int:

        with self._condition:

            return len(
                self._items
            )



# ============================================================
# Global Queue Instances
# ============================================================


event_queue = EventQueue()

dead_letter_queue = DeadLetterQueue()

# core/events.py
# Part 3 — Continued
# Event Pipeline, Middleware and Processing Chain


# ============================================================
# Event Middleware
# ============================================================


class EventMiddleware:
    """
    Middleware base class.

    Middleware can intercept events before
    and after processing.

    Used by:
    - Security layer
    - Permission system
    - Logging
    - Transactions
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self.name = name

        self.enabled = True



    def before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:
        """
        Execute before event processing.

        Override in subclasses.
        """

        return event



    def after(
        self,
        event: BaseEvent,
        result: Any,
    ) -> Any:
        """
        Execute after event processing.

        Override in subclasses.
        """

        return result



    def error(
        self,
        event: BaseEvent,
        exception: Exception,
    ) -> None:
        """
        Execute when processing fails.
        """

        pass



# ============================================================
# Middleware Chain
# ============================================================


class EventMiddlewareChain:
    """
    Executes middleware in order.
    """

    def __init__(
        self,
    ) -> None:

        self._middlewares: list[
            EventMiddleware
        ] = []

        self._lock = threading.RLock()



    def add(
        self,
        middleware: EventMiddleware,
    ) -> None:
        """
        Register middleware.
        """

        with self._lock:

            self._middlewares.append(
                middleware
            )



    def remove(
        self,
        middleware: EventMiddleware,
    ) -> None:
        """
        Remove middleware.
        """

        with self._lock:

            if middleware in self._middlewares:

                self._middlewares.remove(
                    middleware
                )



    def process_before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:
        """
        Execute before pipeline.
        """

        current = event


        for middleware in list(
            self._middlewares
        ):

            if middleware.enabled:

                current = middleware.before(
                    current
                )


        return current



    def process_after(
        self,
        event: BaseEvent,
        result: Any,
    ) -> Any:
        """
        Execute after pipeline.
        """

        current = result


        for middleware in reversed(
            self._middlewares
        ):

            if middleware.enabled:

                current = middleware.after(
                    event,
                    current,
                )


        return current



    def process_error(
        self,
        event: BaseEvent,
        exception: Exception,
    ) -> None:

        for middleware in reversed(
            self._middlewares
        ):

            if middleware.enabled:

                middleware.error(
                    event,
                    exception,
                )



# ============================================================
# Event Pipeline
# ============================================================


class EventPipeline:
    """
    Complete event execution pipeline.

    Flow:

    Validate
        ↓
    Middleware Before
        ↓
    Hooks Before
        ↓
    Dispatch
        ↓
    Hooks After
        ↓
    Middleware After
        ↓
    Statistics
    """

    def __init__(
        self,
        manager: Optional[EventManager] = None,
    ) -> None:

        self.manager = (
            manager
            or
            event_manager
        )

        self.middleware = (
            EventMiddlewareChain()
        )



    def execute(
        self,
        event: BaseEvent,
    ) -> list[Any]:
        """
        Execute full pipeline.
        """

        EventValidator.validate(
            event
        )


        try:

            event = (
                self.middleware.process_before(
                    event
                )
            )


            event_hook_manager.before(
                event
            )


            result = (
                self.manager.emit(
                    event
                )
            )


            event_hook_manager.after(
                event
            )


            result = (
                self.middleware.process_after(
                    event,
                    result,
                )
            )


            return result



        except Exception as exc:

            self.middleware.process_error(
                event,
                exc,
            )

            raise



# ============================================================
# Global Pipeline Instance
# ============================================================


event_pipeline = EventPipeline()

# core/events.py
# Part 4
# Event Monitoring, Audit Trail and Runtime Integration


# ============================================================
# Event Audit Entry
# ============================================================


@dataclass(slots=True)
class EventAuditEntry:
    """
    Immutable-style audit record for events.

    Used for:
    - Security auditing
    - Compliance tracking
    - Debugging
    - User activity history
    """

    event_id: str

    event_name: str

    action: str

    actor: Optional[str] = None

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    details: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Event Audit Logger
# ============================================================


class EventAuditLogger:
    """
    Collects event audit history.
    """

    def __init__(
        self,
        max_entries: int = 100000,
    ) -> None:

        self.max_entries = max_entries

        self._entries: list[
            EventAuditEntry
        ] = []

        self._lock = threading.RLock()



    def record(
        self,
        event: BaseEvent,
        action: str,
        *,
        actor: Optional[str] = None,
        details: Optional[
            Mapping[str, Any]
        ] = None,
    ) -> EventAuditEntry:
        """
        Add audit record.
        """

        entry = EventAuditEntry(
            event_id=event.id,
            event_name=event.name,
            action=action,
            actor=actor,
            details=dict(
                details or {}
            ),
        )


        with self._lock:

            self._entries.append(
                entry
            )

            self._trim()


        return entry



    def _trim(
        self,
    ) -> None:

        overflow = (
            len(self._entries)
            -
            self.max_entries
        )

        if overflow > 0:

            del self._entries[
                :overflow
            ]



    def list_entries(
        self,
    ) -> list[EventAuditEntry]:

        with self._lock:

            return list(
                self._entries
            )



# ============================================================
# Event Monitor
# ============================================================


class EventMonitor:
    """
    Real-time event monitoring layer.

    Provides:
    - Counters
    - Error tracking
    - Performance information
    """

    def __init__(
        self,
    ) -> None:

        self._received = 0

        self._processed = 0

        self._failed = 0

        self._processing_times: list[
            float
        ] = []

        self._lock = threading.RLock()



    def received(
        self,
    ) -> None:

        with self._lock:

            self._received += 1



    def processed(
        self,
        duration: float,
    ) -> None:

        with self._lock:

            self._processed += 1

            self._processing_times.append(
                duration
            )



    def failed(
        self,
    ) -> None:

        with self._lock:

            self._failed += 1



    def snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Return monitoring snapshot.
        """

        with self._lock:

            average = 0.0

            if self._processing_times:

                average = (
                    sum(
                        self._processing_times
                    )
                    /
                    len(
                        self._processing_times
                    )
                )


            return {
                "received":
                    self._received,

                "processed":
                    self._processed,

                "failed":
                    self._failed,

                "average_time":
                    average,
            }



# ============================================================
# Runtime Event Bridge
# ============================================================


class RuntimeEventBridge:
    """
    Bridge between event system
    and runtime components.

    Future integration point for:
    - Runtime Engine
    - Scheduler
    - Workers
    """

    def __init__(
        self,
    ) -> None:

        self.enabled = True



    def publish(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Publish event into runtime pipeline.
        """

        if not self.enabled:

            return


        event_pipeline.execute(
            event
        )



    def shutdown(
        self,
    ) -> None:

        self.enabled = False



    def start(
        self,
    ) -> None:

        self.enabled = True



# ============================================================
# Global Monitoring Instances
# ============================================================


event_audit_logger = EventAuditLogger()

event_monitor = EventMonitor()

runtime_event_bridge = RuntimeEventBridge()

# core/events.py
# Part 4 — Continued
# Event Permissions, Security Checks and Access Control


# ============================================================
# Event Permission Action
# ============================================================


class EventPermissionAction(str, Enum):
    """
    Supported event security actions.
    """

    CREATE = "create"

    READ = "read"

    EXECUTE = "execute"

    MODIFY = "modify"

    DELETE = "delete"

    ADMIN = "admin"



# ============================================================
# Event Permission Rule
# ============================================================


@dataclass(slots=True)
class EventPermissionRule:
    """
    Defines permission requirements
    for an event.
    """

    event_pattern: str

    action: EventPermissionAction

    required_roles: set[str] = field(
        default_factory=set
    )

    required_attributes: Dict[
        str,
        Any
    ] = field(
        default_factory=dict
    )

    enabled: bool = True



    def matches(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Check event pattern match.
        """

        return EventMatcher.match_name(
            event,
            self.event_pattern,
        )



# ============================================================
# Event Security Context
# ============================================================


@dataclass(slots=True)
class EventSecurityContext:
    """
    Security information attached
    to event execution.
    """

    user_id: Optional[str] = None

    roles: set[str] = field(
        default_factory=set
    )

    permissions: set[str] = field(
        default_factory=set
    )

    attributes: Dict[str, Any] = field(
        default_factory=dict
    )



    def has_role(
        self,
        role: str,
    ) -> bool:

        return role in self.roles



    def has_permission(
        self,
        permission: str,
    ) -> bool:

        return (
            permission
            in
            self.permissions
        )



# ============================================================
# Event Permission Manager
# ============================================================


class EventPermissionManager:
    """
    Controls event execution permissions.
    """

    def __init__(
        self,
    ) -> None:

        self._rules: list[
            EventPermissionRule
        ] = []

        self._lock = threading.RLock()



    def add_rule(
        self,
        rule: EventPermissionRule,
    ) -> None:
        """
        Register permission rule.
        """

        with self._lock:

            self._rules.append(
                rule
            )



    def remove_rule(
        self,
        rule: EventPermissionRule,
    ) -> None:

        with self._lock:

            if rule in self._rules:

                self._rules.remove(
                    rule
                )



    def check(
        self,
        event: BaseEvent,
        security: EventSecurityContext,
    ) -> bool:
        """
        Verify event access.
        """

        for rule in list(
            self._rules
        ):

            if not rule.enabled:

                continue


            if not rule.matches(
                event
            ):

                continue


            if rule.required_roles:

                if not rule.required_roles.intersection(
                    security.roles
                ):

                    return False


            for key, value in (
                rule.required_attributes.items()
            ):

                if (
                    security.attributes.get(key)
                    !=
                    value
                ):

                    return False


        return True



# ============================================================
# Security Middleware
# ============================================================


class EventSecurityMiddleware(
    EventMiddleware
):
    """
    Middleware enforcing event permissions.
    """

    def __init__(
        self,
        permission_manager:
            EventPermissionManager,
    ) -> None:

        super().__init__(
            "security"
        )

        self.permission_manager = (
            permission_manager
        )

        self.context = (
            EventSecurityContext()
        )



    def before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:
        """
        Validate permission before execution.
        """

        allowed = (
            self.permission_manager.check(
                event,
                self.context,
            )
        )


        if not allowed:

            raise PermissionError(
                f"Event execution denied: "
                f"{event.name}"
            )


        return event



# ============================================================
# Global Permission Manager
# ============================================================


event_permission_manager = (
    EventPermissionManager()
)

# core/events.py
# Part 4 — Continued
# Event Transactions, Rollback and Consistency Management


# ============================================================
# Event Transaction State
# ============================================================


class EventTransactionState(str, Enum):
    """
    Transaction lifecycle states.
    """

    CREATED = "created"

    ACTIVE = "active"

    COMMITTED = "committed"

    ROLLED_BACK = "rolled_back"

    FAILED = "failed"



# ============================================================
# Event Transaction Operation
# ============================================================


@dataclass(slots=True)
class EventTransactionOperation:
    """
    Represents a reversible event operation.
    """

    name: str

    execute: Callable[[], Any]

    rollback: Optional[
        Callable[[], Any]
    ] = None

    executed: bool = False

    result: Any = None



    def run(
        self,
    ) -> Any:
        """
        Execute operation.
        """

        self.result = (
            self.execute()
        )

        self.executed = True

        return self.result



    def undo(
        self,
    ) -> None:
        """
        Rollback operation.
        """

        if (
            self.executed
            and
            self.rollback
        ):

            self.rollback()



# ============================================================
# Event Transaction
# ============================================================


@dataclass(slots=True)
class EventTransaction:
    """
    Groups multiple event operations
    into atomic execution.
    """

    transaction_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    state: EventTransactionState = (
        EventTransactionState.CREATED
    )

    operations: list[
        EventTransactionOperation
    ] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )


    def add(
        self,
        operation:
            EventTransactionOperation,
    ) -> None:
        """
        Add operation.
        """

        self.operations.append(
            operation
        )



    def begin(
        self,
    ) -> None:

        self.state = (
            EventTransactionState.ACTIVE
        )



    def commit(
        self,
    ) -> list[Any]:
        """
        Execute all operations.
        """

        self.begin()

        results = []


        try:

            for operation in (
                self.operations
            ):

                results.append(
                    operation.run()
                )


            self.state = (
                EventTransactionState.COMMITTED
            )


            return results



        except Exception:

            self.rollback()

            self.state = (
                EventTransactionState.FAILED
            )

            raise



    def rollback(
        self,
    ) -> None:
        """
        Reverse executed operations.
        """

        for operation in reversed(
            self.operations
        ):

            operation.undo()


        self.state = (
            EventTransactionState.ROLLED_BACK
        )



# ============================================================
# Transaction Manager
# ============================================================


class EventTransactionManager:
    """
    Manages active event transactions.
    """

    def __init__(
        self,
    ) -> None:

        self._transactions: Dict[
            str,
            EventTransaction
        ] = {}

        self._lock = threading.RLock()



    def create(
        self,
    ) -> EventTransaction:
        """
        Create transaction.
        """

        transaction = (
            EventTransaction()
        )


        with self._lock:

            self._transactions[
                transaction.transaction_id
            ] = transaction


        return transaction



    def get(
        self,
        transaction_id: str,
    ) -> Optional[EventTransaction]:

        with self._lock:

            return self._transactions.get(
                transaction_id
            )



    def remove(
        self,
        transaction_id: str,
    ) -> None:

        with self._lock:

            self._transactions.pop(
                transaction_id,
                None,
            )



# ============================================================
# Transaction Middleware
# ============================================================


class EventTransactionMiddleware(
    EventMiddleware
):
    """
    Adds transaction support around events.
    """

    def __init__(
        self,
        manager:
            EventTransactionManager,
    ) -> None:

        super().__init__(
            "transaction"
        )

        self.manager = manager



    def before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:

        event.context.metadata[
            "transaction_enabled"
        ] = True

        return event



# ============================================================
# Global Transaction Manager
# ============================================================


event_transaction_manager = (
    EventTransactionManager()
)

# core/events.py
# Part 5
# Event Thread Safety, Concurrency and Worker Support


# ============================================================
# Event Lock
# ============================================================


class EventLock:
    """
    Provides locking for event execution.

    Used for:
    - Shared state protection
    - Concurrent workers
    - Runtime synchronization
    """

    def __init__(
        self,
    ) -> None:

        self._lock = threading.RLock()

        self.owner: Optional[str] = None



    def acquire(
        self,
        owner: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Acquire event lock.
        """

        acquired = (
            self._lock.acquire(
                timeout=timeout
                if timeout is not None
                else -1
            )
        )


        if acquired:

            self.owner = owner


        return acquired



    def release(
        self,
    ) -> None:
        """
        Release lock.
        """

        self.owner = None

        self._lock.release()



    def locked(
        self,
    ) -> bool:

        return self._lock._is_owned()



# ============================================================
# Event Lock Manager
# ============================================================


class EventLockManager:
    """
    Manages multiple event locks.
    """

    def __init__(
        self,
    ) -> None:

        self._locks: Dict[
            str,
            EventLock
        ] = {}

        self._lock = threading.RLock()



    def get(
        self,
        key: str,
    ) -> EventLock:
        """
        Get or create lock.
        """

        with self._lock:

            if key not in self._locks:

                self._locks[key] = (
                    EventLock()
                )


            return self._locks[key]



    def remove(
        self,
        key: str,
    ) -> None:

        with self._lock:

            self._locks.pop(
                key,
                None,
            )



# ============================================================
# Event Worker
# ============================================================


class EventWorker:
    """
    Background worker for processing events.

    Designed for:
    - Runtime workers
    - Queue processors
    - Async expansion
    """

    def __init__(
        self,
        queue: EventQueue,
        pipeline: EventPipeline,
    ) -> None:

        self.queue = queue

        self.pipeline = pipeline

        self.running = False

        self.thread: Optional[
            threading.Thread
        ] = None



    def start(
        self,
    ) -> None:
        """
        Start worker thread.
        """

        if self.running:

            return


        self.running = True


        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self.thread.start()



    def stop(
        self,
    ) -> None:

        self.running = False



    def _run(
        self,
    ) -> None:
        """
        Worker loop.
        """

        while self.running:

            item = self.queue.pop(
                timeout=1.0
            )


            if item is None:

                continue


            try:

                self.pipeline.execute(
                    item.event
                )


            except Exception as exc:

                dead_letter_queue.push(
                    item.event,
                    str(exc),
                )



# ============================================================
# Event Scheduler
# ============================================================


@dataclass(slots=True)
class ScheduledEvent:
    """
    Event scheduled for future execution.
    """

    event: BaseEvent

    execute_at: float



class EventScheduler:
    """
    Simple event scheduler.

    Future integration:
    - Cron system
    - Task manager
    - Runtime scheduler
    """

    def __init__(
        self,
    ) -> None:

        self._events: list[
            ScheduledEvent
        ] = []

        self._lock = threading.RLock()



    def schedule(
        self,
        event: BaseEvent,
        delay: float,
    ) -> None:
        """
        Schedule event.
        """

        item = ScheduledEvent(
            event=event,
            execute_at=(
                time.time()
                +
                delay
            ),
        )


        with self._lock:

            self._events.append(
                item
            )



    def due(
        self,
    ) -> list[BaseEvent]:
        """
        Return ready events.
        """

        now = time.time()

        result = []


        with self._lock:

            remaining = []


            for item in self._events:

                if item.execute_at <= now:

                    result.append(
                        item.event
                    )

                else:

                    remaining.append(
                        item
                    )


            self._events = remaining


        return result



# ============================================================
# Global Concurrency Objects
# ============================================================


event_lock_manager = EventLockManager()

event_scheduler = EventScheduler()

# core/events.py
# Part 5 — Continued
# Event Serialization Advanced, Import/Export and Versioning


# ============================================================
# Event Version Manager
# ============================================================


@dataclass(slots=True)
class EventVersion:
    """
    Represents event schema version.
    """

    major: int = 1

    minor: int = 0

    patch: int = 0


    def __str__(
        self,
    ) -> str:

        return (
            f"{self.major}."
            f"{self.minor}."
            f"{self.patch}"
        )


    def compatible_with(
        self,
        other: "EventVersion",
    ) -> bool:
        """
        Check compatibility.
        """

        return (
            self.major
            ==
            other.major
        )



# ============================================================
# Event Migration
# ============================================================


class EventMigration:
    """
    Handles event schema migration.

    Used when old persisted events
    need to run on newer versions.
    """

    def __init__(
        self,
        from_version: EventVersion,
        to_version: EventVersion,
        migrate: Callable[
            [Dict[str, Any]],
            Dict[str, Any]
        ],
    ) -> None:

        self.from_version = (
            from_version
        )

        self.to_version = (
            to_version
        )

        self.migrate = migrate



# ============================================================
# Event Version Registry
# ============================================================


class EventVersionRegistry:
    """
    Stores event migrations.
    """

    def __init__(
        self,
    ) -> None:

        self._migrations: list[
            EventMigration
        ] = []

        self._lock = threading.RLock()



    def register(
        self,
        migration: EventMigration,
    ) -> None:

        with self._lock:

            self._migrations.append(
                migration
            )



    def migrate(
        self,
        data: Dict[str, Any],
        current: EventVersion,
        target: EventVersion,
    ) -> Dict[str, Any]:
        """
        Apply migrations.
        """

        result = data


        for migration in list(
            self._migrations
        ):

            if (
                migration.from_version.major
                ==
                current.major
                and
                migration.to_version.major
                ==
                target.major
            ):

                result = migration.migrate(
                    result
                )


        return result



# ============================================================
# Advanced Event Serializer
# ============================================================


class AdvancedEventSerializer:
    """
    Enterprise serializer.

    Adds:
    - Type information
    - Versioning
    - Metadata
    - Integrity fields
    """

    VERSION = EventVersion(
        1,
        0,
        0,
    )


    @classmethod
    def export(
        cls,
        event: BaseEvent,
    ) -> Dict[str, Any]:
        """
        Export complete event package.
        """

        return {
            "schema_version":
                str(cls.VERSION),

            "event_type":
                event.__class__.__name__,

            "event":
                EventSerializer.to_dict(
                    event
                ),

            "exported_at":
                datetime.now(
                    UTC
                ).isoformat(),
        }



    @classmethod
    def import_event(
        cls,
        package: Mapping[str, Any],
    ) -> BaseEvent:
        """
        Restore event package.
        """

        event_data = package.get(
            "event",
            {},
        )


        return EventSerializer.from_dict(
            event_data
        )



    @classmethod
    def dumps(
        cls,
        event: BaseEvent,
    ) -> str:
        """
        Export JSON string.
        """

        return json.dumps(
            cls.export(event),
            default=str,
            ensure_ascii=False,
        )



    @classmethod
    def loads(
        cls,
        value: str,
    ) -> BaseEvent:
        """
        Import from JSON.
        """

        package = json.loads(
            value
        )

        return cls.import_event(
            package
        )



# ============================================================
# Global Version Registry
# ============================================================


event_version_registry = (
    EventVersionRegistry()
)

# core/events.py
# Part 5 — Continued
# Event Configuration, Registration and Plugin Integration


# ============================================================
# Event Configuration
# ============================================================


@dataclass(slots=True)
class EventConfiguration:
    """
    Global event system configuration.
    """

    enabled: bool = True

    max_queue_size: int = 50000

    enable_tracing: bool = True

    enable_audit: bool = True

    enable_metrics: bool = True

    enable_recovery: bool = True

    worker_count: int = 1

    retry_policy: EventRetryPolicy = field(
        default_factory=EventRetryPolicy
    )



# ============================================================
# Event Config Manager
# ============================================================


class EventConfigManager:
    """
    Runtime configuration manager.
    """

    def __init__(
        self,
        config: Optional[
            EventConfiguration
        ] = None,
    ) -> None:

        self._config = (
            config
            or
            EventConfiguration()
        )

        self._lock = threading.RLock()



    def get(
        self,
    ) -> EventConfiguration:

        with self._lock:

            return self._config



    def update(
        self,
        **values: Any,
    ) -> None:
        """
        Update configuration.
        """

        with self._lock:

            for key, value in values.items():

                if hasattr(
                    self._config,
                    key,
                ):

                    setattr(
                        self._config,
                        key,
                        value,
                    )



# ============================================================
# Event Type Information
# ============================================================


@dataclass(slots=True)
class EventTypeInfo:
    """
    Metadata about registered events.
    """

    name: str

    event_class: Type[BaseEvent]

    version: str = EVENT_VERSION

    description: str = ""

    plugin: Optional[str] = None

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Enterprise Event Registry
# ============================================================


class EnterpriseEventRegistry:
    """
    Extended registry supporting plugins
    and runtime discovery.
    """

    def __init__(
        self,
    ) -> None:

        self._types: Dict[
            str,
            EventTypeInfo
        ] = {}

        self._lock = threading.RLock()



    def register(
        self,
        name: str,
        event_class: Type[BaseEvent],
        *,
        description: str = "",
        plugin: Optional[str] = None,
    ) -> None:
        """
        Register event type.
        """

        if not issubclass(
            event_class,
            BaseEvent,
        ):

            raise TypeError(
                "Invalid event class"
            )


        info = EventTypeInfo(
            name=name,
            event_class=event_class,
            description=description,
            plugin=plugin,
        )


        with self._lock:

            self._types[name] = info



    def resolve(
        self,
        name: str,
    ) -> Optional[EventTypeInfo]:

        with self._lock:

            return self._types.get(
                name
            )



    def unregister(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._types.pop(
                name,
                None,
            )



    def all(
        self,
    ) -> list[EventTypeInfo]:

        with self._lock:

            return list(
                self._types.values()
            )



# ============================================================
# Plugin Event Provider
# ============================================================


class EventPluginProvider:
    """
    Interface for plugins exposing events.
    """

    def register_events(
        self,
        registry:
            EnterpriseEventRegistry,
    ) -> None:
        """
        Plugins override this method.
        """

        raise NotImplementedError(
            "Plugin must register events"
        )



# ============================================================
# Global Event Configuration Objects
# ============================================================


event_config_manager = (
    EventConfigManager()
)


enterprise_event_registry = (
    EnterpriseEventRegistry()
)

# core/events.py
# Part 6
# Event System Initialization, Shutdown and Health Monitoring


# ============================================================
# Event Health Status
# ============================================================


class EventHealthStatus(str, Enum):
    """
    Event system health states.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNAVAILABLE = "unavailable"



# ============================================================
# Event Health Report
# ============================================================


@dataclass(slots=True)
class EventHealthReport:
    """
    Health information of event subsystem.
    """

    status: EventHealthStatus

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    checks: Dict[str, Any] = field(
        default_factory=dict
    )

    warnings: list[str] = field(
        default_factory=list
    )



# ============================================================
# Event Health Monitor
# ============================================================


class EventHealthMonitor:
    """
    Performs health checks.

    Checks:
    - Queue
    - Registry
    - Workers
    - Storage
    - Configuration
    """

    def check(
        self,
    ) -> EventHealthReport:
        """
        Run health checks.
        """

        checks = {}

        warnings = []


        try:

            checks["queue"] = {
                "size":
                    event_queue.size(),
                "status":
                    "ok",
            }


        except Exception as exc:

            checks["queue"] = {
                "status":
                    "error",
                "error":
                    str(exc),
            }

            warnings.append(
                "Queue unavailable"
            )



        try:

            checks["registry"] = {
                "events":
                    len(
                        enterprise_event_registry.all()
                    ),
                "status":
                    "ok",
            }


        except Exception as exc:

            checks["registry"] = {
                "status":
                    "error",
                "error":
                    str(exc),
            }

            warnings.append(
                "Registry unavailable"
            )



        try:

            checks["store"] = {
                "events":
                    len(
                        event_store.list_all()
                    ),
                "status":
                    "ok",
            }


        except Exception as exc:

            checks["store"] = {
                "status":
                    "error",
                "error":
                    str(exc),
            }

            warnings.append(
                "Event store unavailable"
            )


        status = (
            EventHealthStatus.HEALTHY
            if not warnings
            else
            EventHealthStatus.DEGRADED
        )


        return EventHealthReport(
            status=status,
            checks=checks,
            warnings=warnings,
        )



# ============================================================
# Event System Lifecycle
# ============================================================


class EventSystem:
    """
    Main lifecycle controller.

    Responsible for:
    - Startup
    - Shutdown
    - Runtime state
    """

    def __init__(
        self,
    ) -> None:

        self.initialized = False

        self.running = False

        self.worker: Optional[
            EventWorker
        ] = None



    def initialize(
        self,
    ) -> None:
        """
        Initialize event system.
        """

        if self.initialized:

            return


        self.initialized = True



    def start(
        self,
    ) -> None:
        """
        Start background processing.
        """

        if not self.initialized:

            self.initialize()


        if self.running:

            return


        self.worker = EventWorker(
            event_queue,
            event_pipeline,
        )


        self.worker.start()

        self.running = True



    def shutdown(
        self,
    ) -> None:
        """
        Stop event system.
        """

        if self.worker:

            self.worker.stop()


        self.running = False



    def health(
        self,
    ) -> EventHealthReport:

        return event_health_monitor.check()



# ============================================================
# Event System Instance
# ============================================================


event_health_monitor = (
    EventHealthMonitor()
)


event_system = EventSystem()

# core/events.py
# Part 6 — Continued
# Event Logging, Notification and External Integration


# ============================================================
# Event Log Level
# ============================================================


class EventLogLevel(str, Enum):
    """
    Logging severity levels.
    """

    DEBUG = "debug"

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"



# ============================================================
# Event Log Entry
# ============================================================


@dataclass(slots=True)
class EventLogEntry:
    """
    Structured event log record.
    """

    event_id: str

    event_name: str

    level: EventLogLevel

    message: str

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    data: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Event Logger
# ============================================================


class EventLogger:
    """
    Structured event logger.

    Supports:
    - Debugging
    - Monitoring
    - Diagnostics
    """

    def __init__(
        self,
        max_entries: int = 50000,
    ) -> None:

        self.max_entries = max_entries

        self._logs: list[
            EventLogEntry
        ] = []

        self._lock = threading.RLock()



    def write(
        self,
        event: BaseEvent,
        level: EventLogLevel,
        message: str,
        **data: Any,
    ) -> EventLogEntry:
        """
        Write log entry.
        """

        entry = EventLogEntry(
            event_id=event.id,
            event_name=event.name,
            level=level,
            message=message,
            data=data,
        )


        with self._lock:

            self._logs.append(
                entry
            )

            overflow = (
                len(self._logs)
                -
                self.max_entries
            )


            if overflow > 0:

                del self._logs[
                    :overflow
                ]


        return entry



    def query(
        self,
        level: Optional[
            EventLogLevel
        ] = None,
    ) -> list[EventLogEntry]:
        """
        Query logs.
        """

        with self._lock:

            if level is None:

                return list(
                    self._logs
                )


            return [
                item
                for item
                in self._logs
                if item.level == level
            ]



# ============================================================
# Event Notification
# ============================================================


@dataclass(slots=True)
class EventNotification:
    """
    Notification generated by events.
    """

    title: str

    message: str

    event_id: Optional[str] = None

    severity: EventLogLevel = (
        EventLogLevel.INFO
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Notification Manager
# ============================================================


class EventNotificationManager:
    """
    Manages event notifications.

    Future integration:
    - UI
    - Telegram
    - Email
    - Dashboard
    """

    def __init__(
        self,
    ) -> None:

        self._notifications: list[
            EventNotification
        ] = []

        self._lock = threading.RLock()



    def send(
        self,
        notification:
            EventNotification,
    ) -> None:

        with self._lock:

            self._notifications.append(
                notification
            )



    def all(
        self,
    ) -> list[EventNotification]:

        with self._lock:

            return list(
                self._notifications
            )



    def clear(
        self,
    ) -> None:

        with self._lock:

            self._notifications.clear()



# ============================================================
# External Event Adapter
# ============================================================


class ExternalEventAdapter:
    """
    Base adapter for external systems.

    Examples:
    - Telegram
    - WebSocket
    - REST API
    - Message brokers
    """

    name: str = "external"


    def send(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Send event externally.
        """

        raise NotImplementedError(
            "Adapter must implement send()"
        )



# ============================================================
# External Adapter Registry
# ============================================================


class ExternalAdapterRegistry:
    """
    Stores external adapters.
    """

    def __init__(
        self,
    ) -> None:

        self._adapters: Dict[
            str,
            ExternalEventAdapter
        ] = {}



    def register(
        self,
        adapter: ExternalEventAdapter,
    ) -> None:

        self._adapters[
            adapter.name
        ] = adapter



    def get(
        self,
        name: str,
    ) -> Optional[
        ExternalEventAdapter
    ]:

        return self._adapters.get(
            name
        )



# ============================================================
# Global Logging Objects
# ============================================================


event_logger = EventLogger()

event_notification_manager = (
    EventNotificationManager()
)

external_adapter_registry = (
    ExternalAdapterRegistry()
)

# core/events.py
# Part 6 — Continued
# Event API, Command Support and Message Routing


# ============================================================
# Event Message Type
# ============================================================


class EventMessageType(str, Enum):
    """
    Communication message types.
    """

    EVENT = "event"

    COMMAND = "command"

    QUERY = "query"

    RESPONSE = "response"

    NOTIFICATION = "notification"



# ============================================================
# Event Message
# ============================================================


@dataclass(slots=True)
class EventMessage:
    """
    Generic transport message.

    Used for communication between:
    - Runtime
    - Agents
    - Plugins
    - Services
    """

    message_type: EventMessageType

    name: str

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    message_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    reply_to: Optional[str] = None

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



    def to_event(
        self,
    ) -> BaseEvent:
        """
        Convert message into event.
        """

        return EventFactory.create(
            name=self.name,
            payload=self.payload,
            category=EventCategory.RUNTIME,
        )



# ============================================================
# Command Event
# ============================================================


@dataclass(slots=True)
class CommandEvent(BaseEvent):
    """
    Represents executable commands.
    """

    command_name: str = ""

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Query Event
# ============================================================


@dataclass(slots=True)
class QueryEvent(BaseEvent):
    """
    Represents read-only requests.
    """

    query_name: str = ""

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Response Event
# ============================================================


@dataclass(slots=True)
class ResponseEvent(BaseEvent):
    """
    Response generated by commands
    or queries.
    """

    request_id: Optional[str] = None

    success: bool = True

    data: Any = None



# ============================================================
# Message Router
# ============================================================


class EventMessageRouter:
    """
    Routes messages into event system.
    """

    def __init__(
        self,
    ) -> None:

        self._routes: Dict[
            EventMessageType,
            Callable[
                [EventMessage],
                Any
            ]
        ] = {}



    def register(
        self,
        message_type: EventMessageType,
        handler: Callable[
            [EventMessage],
            Any
        ],
    ) -> None:
        """
        Register message handler.
        """

        self._routes[
            message_type
        ] = handler



    def route(
        self,
        message: EventMessage,
    ) -> Any:
        """
        Route message.
        """

        handler = self._routes.get(
            message.message_type
        )


        if handler is None:

            raise ValueError(
                f"No route for "
                f"{message.message_type}"
            )


        return handler(
            message
        )



# ============================================================
# Default Message Handlers
# ============================================================


def handle_event_message(
    message: EventMessage,
) -> Any:
    """
    Process normal events.
    """

    return event_manager.emit(
        message.to_event()
    )



def handle_command_message(
    message: EventMessage,
) -> Any:
    """
    Process commands.
    """

    event = CommandEvent(
        name=message.name,
        command_name=message.name,
        parameters=message.payload,
        payload=message.payload,
    )

    return event_manager.emit(
        event
    )



# ============================================================
# Global Router
# ============================================================


event_message_router = (
    EventMessageRouter()
)


event_message_router.register(
    EventMessageType.EVENT,
    handle_event_message,
)


event_message_router.register(
    EventMessageType.COMMAND,
    handle_command_message,
)

# core/events.py
# Part 7
# Event Metrics Export, Performance Tracking and Profiling


# ============================================================
# Event Performance Record
# ============================================================


@dataclass(slots=True)
class EventPerformanceRecord:
    """
    Detailed performance information.
    """

    event_id: str

    event_name: str

    started_at: float

    finished_at: Optional[float] = None

    cpu_time: float = 0.0

    execution_time: float = 0.0

    memory_usage: Optional[int] = None

    handler: Optional[str] = None



    def finish(
        self,
    ) -> None:
        """
        Complete performance record.
        """

        self.finished_at = time.time()

        self.execution_time = (
            self.finished_at
            -
            self.started_at
        )



# ============================================================
# Event Profiler
# ============================================================


class EventProfiler:
    """
    Profiles event execution.

    Used for:
    - Performance optimization
    - Bottleneck detection
    - Enterprise monitoring
    """

    def __init__(
        self,
        max_records: int = 10000,
    ) -> None:

        self.max_records = max_records

        self._records: list[
            EventPerformanceRecord
        ] = []

        self._active: Dict[
            str,
            EventPerformanceRecord
        ] = {}

        self._lock = threading.RLock()



    def start(
        self,
        event: BaseEvent,
        handler: Optional[str] = None,
    ) -> EventPerformanceRecord:
        """
        Start profiling.
        """

        record = EventPerformanceRecord(
            event_id=event.id,
            event_name=event.name,
            started_at=time.time(),
            handler=handler,
        )


        with self._lock:

            self._active[
                event.id
            ] = record


        return record



    def stop(
        self,
        event_id: str,
    ) -> Optional[
        EventPerformanceRecord
    ]:
        """
        Stop profiling.
        """

        with self._lock:

            record = self._active.pop(
                event_id,
                None,
            )


        if record:

            record.finish()


            with self._lock:

                self._records.append(
                    record
                )


                overflow = (
                    len(self._records)
                    -
                    self.max_records
                )


                if overflow > 0:

                    del self._records[
                        :overflow
                    ]


        return record



    def records(
        self,
    ) -> list[EventPerformanceRecord]:

        with self._lock:

            return list(
                self._records
            )



# ============================================================
# Performance Aggregator
# ============================================================


class EventPerformanceAggregator:
    """
    Aggregates performance statistics.
    """

    def summarize(
        self,
        records:
            Iterable[EventPerformanceRecord],
    ) -> Dict[str, Any]:
        """
        Generate summary.
        """

        records = list(
            records
        )


        if not records:

            return {
                "count": 0,
                "average": 0.0,
                "maximum": 0.0,
                "minimum": 0.0,
            }


        times = [
            item.execution_time
            for item
            in records
        ]


        return {
            "count":
                len(times),

            "average":
                sum(times)
                /
                len(times),

            "maximum":
                max(times),

            "minimum":
                min(times),
        }



# ============================================================
# Metrics Exporter
# ============================================================


class EventMetricsExporter:
    """
    Converts metrics into external format.

    Future:
    - Prometheus
    - Grafana
    - Dashboard API
    """

    def export(
        self,
    ) -> Dict[str, Any]:
        """
        Export current metrics.
        """

        return {
            "events":
                event_monitor.snapshot(),

            "statistics": {
                "total":
                    event_statistics.total_events,

                "completed":
                    event_statistics.completed_events,

                "failed":
                    event_statistics.failed_events,

                "average_time":
                    event_statistics.average_execution_time,
            },

            "queue": {
                "size":
                    event_queue.size(),
            },
        }



# ============================================================
# Global Performance Objects
# ============================================================


event_profiler = EventProfiler()

event_performance_aggregator = (
    EventPerformanceAggregator()
)

event_metrics_exporter = (
    EventMetricsExporter()
)

# core/events.py
# Part 7 — Continued
# Event Dependency Graph, Ordering and Priority Execution


# ============================================================
# Event Dependency
# ============================================================


@dataclass(slots=True)
class EventDependency:
    """
    Defines dependency between events.

    Example:
    workspace.open
        requires
    workspace.create
    """

    event_name: str

    depends_on: set[str] = field(
        default_factory=set
    )

    optional: bool = False



# ============================================================
# Event Dependency Manager
# ============================================================


class EventDependencyManager:
    """
    Resolves event dependencies.

    Used by:
    - Workflow engine
    - Runtime scheduler
    - Plugin loading
    """

    def __init__(
        self,
    ) -> None:

        self._dependencies: Dict[
            str,
            EventDependency
        ] = {}

        self._lock = threading.RLock()



    def register(
        self,
        dependency: EventDependency,
    ) -> None:
        """
        Register dependency.
        """

        with self._lock:

            self._dependencies[
                dependency.event_name
            ] = dependency



    def resolve(
        self,
        event_name: str,
    ) -> set[str]:
        """
        Get required dependencies.
        """

        with self._lock:

            dependency = (
                self._dependencies.get(
                    event_name
                )
            )


        if dependency is None:

            return set()


        return set(
            dependency.depends_on
        )



    def validate(
        self,
        completed_events: set[str],
        event_name: str,
    ) -> bool:
        """
        Check dependency satisfaction.
        """

        required = self.resolve(
            event_name
        )

        return required.issubset(
            completed_events
        )



# ============================================================
# Priority Event Executor
# ============================================================


class PriorityEventExecutor:
    """
    Executes events according to priority.

    Critical events execute first.
    """

    def __init__(
        self,
        pipeline: EventPipeline,
    ) -> None:

        self.pipeline = pipeline

        self._queue: list[
            tuple[
                int,
                float,
                BaseEvent
            ]
        ] = []

        self._lock = threading.RLock()



    def submit(
        self,
        event: BaseEvent,
    ) -> None:
        """
        Add event by priority.
        """

        with self._lock:

            self._queue.append(
                (
                    event.priority.value,
                    time.time(),
                    event,
                )
            )

            self._queue.sort(
                key=lambda item:
                    (
                        item[0],
                        item[1],
                    )
            )



    def execute_next(
        self,
    ) -> Optional[list[Any]]:
        """
        Execute highest priority event.
        """

        with self._lock:

            if not self._queue:

                return None


            _, _, event = (
                self._queue.pop(0)
            )


        return self.pipeline.execute(
            event
        )



    def size(
        self,
    ) -> int:

        with self._lock:

            return len(
                self._queue
            )



# ============================================================
# Event Workflow Step
# ============================================================


@dataclass(slots=True)
class EventWorkflowStep:
    """
    A step in event workflow.
    """

    name: str

    event: BaseEvent

    completed: bool = False

    result: Any = None



# ============================================================
# Event Workflow
# ============================================================


class EventWorkflow:
    """
    Executes multiple events as workflow.
    """

    def __init__(
        self,
        pipeline: EventPipeline,
    ) -> None:

        self.pipeline = pipeline

        self.steps: list[
            EventWorkflowStep
        ] = []



    def add(
        self,
        step: EventWorkflowStep,
    ) -> None:

        self.steps.append(
            step
        )



    def execute(
        self,
    ) -> list[Any]:
        """
        Execute workflow steps.
        """

        results = []


        for step in self.steps:

            result = (
                self.pipeline.execute(
                    step.event
                )
            )


            step.completed = True

            step.result = result

            results.append(
                result
            )


        return results



# ============================================================
# Global Dependency Objects
# ============================================================


event_dependency_manager = (
    EventDependencyManager()
)


priority_event_executor = (
    PriorityEventExecutor(
        event_pipeline
    )
)

# core/events.py
# Part 7 — Continued
# Event Tracing, Correlation and Distributed Execution Support


# ============================================================
# Event Trace Span
# ============================================================


@dataclass(slots=True)
class EventTraceSpan:
    """
    Represents a single trace segment.

    Used for:
    - Debugging
    - Distributed tracing
    - Runtime analysis
    """

    span_id: str

    event_id: str

    name: str

    start_time: float

    end_time: Optional[float] = None

    parent_id: Optional[str] = None

    attributes: Dict[str, Any] = field(
        default_factory=dict
    )


    def finish(
        self,
    ) -> None:
        """
        Close trace span.
        """

        self.end_time = time.time()



    @property
    def duration(
        self,
    ) -> float:

        if self.end_time is None:

            return 0.0


        return (
            self.end_time
            -
            self.start_time
        )



# ============================================================
# Event Trace Context
# ============================================================


@dataclass(slots=True)
class EventTraceContext:
    """
    Trace context shared between
    related events.
    """

    trace_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    parent_span_id: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Event Tracer
# ============================================================


class EventTracer:
    """
    Enterprise tracing engine.
    """

    def __init__(
        self,
        max_spans: int = 100000,
    ) -> None:

        self.max_spans = max_spans

        self._spans: list[
            EventTraceSpan
        ] = []

        self._active: Dict[
            str,
            EventTraceSpan
        ] = {}

        self._lock = threading.RLock()



    def start(
        self,
        event: BaseEvent,
        name: Optional[str] = None,
        context:
            Optional[EventTraceContext] = None,
    ) -> EventTraceSpan:
        """
        Start trace span.
        """

        span = EventTraceSpan(
            span_id=uuid.uuid4().hex,
            event_id=event.id,
            name=name or event.name,
            start_time=time.time(),
            parent_id=(
                context.parent_span_id
                if context
                else None
            ),
        )


        with self._lock:

            self._active[
                span.span_id
            ] = span


        return span



    def finish(
        self,
        span_id: str,
    ) -> Optional[EventTraceSpan]:
        """
        Finish trace span.
        """

        with self._lock:

            span = self._active.pop(
                span_id,
                None,
            )


        if span:

            span.finish()


            with self._lock:

                self._spans.append(
                    span
                )


                overflow = (
                    len(self._spans)
                    -
                    self.max_spans
                )


                if overflow > 0:

                    del self._spans[
                        :overflow
                    ]


        return span



    def list(
        self,
    ) -> list[EventTraceSpan]:

        with self._lock:

            return list(
                self._spans
            )



# ============================================================
# Correlation Manager
# ============================================================


class EventCorrelationManager:
    """
    Connects related events.

    Example:
    User Request
        |
        ├── Workspace Event
        ├── Runtime Event
        └── Plugin Event
    """

    def __init__(
        self,
    ) -> None:

        self._relations: Dict[
            str,
            set[str]
        ] = {}

        self._lock = threading.RLock()



    def link(
        self,
        parent_event_id: str,
        child_event_id: str,
    ) -> None:
        """
        Link two events.
        """

        with self._lock:

            self._relations.setdefault(
                parent_event_id,
                set(),
            ).add(
                child_event_id
            )



    def children(
        self,
        event_id: str,
    ) -> set[str]:

        with self._lock:

            return set(
                self._relations.get(
                    event_id,
                    set(),
                )
            )



# ============================================================
# Distributed Event Envelope
# ============================================================


@dataclass(slots=True)
class DistributedEventEnvelope:
    """
    Transport wrapper for events
    between services.
    """

    event: BaseEvent

    node_id: str

    trace_id: str

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Global Trace Objects
# ============================================================


event_tracer = EventTracer()

event_correlation_manager = (
    EventCorrelationManager()
)

# core/events.py
# Part 8
# Event Plugin System, Dynamic Loading and Extension Architecture


# ============================================================
# Event Plugin Metadata
# ============================================================


@dataclass(slots=True)
class EventPluginMetadata:
    """
    Plugin information for event extensions.
    """

    name: str

    version: str

    author: Optional[str] = None

    description: str = ""

    enabled: bool = True

    dependencies: list[str] = field(
        default_factory=list
    )



# ============================================================
# Event Plugin Interface
# ============================================================


class EventPlugin:
    """
    Base class for event plugins.

    Plugins can provide:
    - New events
    - Middleware
    - Hooks
    - Adapters
    - Handlers
    """

    metadata: EventPluginMetadata


    def initialize(
        self,
        system: EventSystem,
    ) -> None:
        """
        Called during plugin startup.
        """

        pass



    def register(
        self,
        registry:
            EnterpriseEventRegistry,
    ) -> None:
        """
        Register plugin events.
        """

        pass



    def shutdown(
        self,
    ) -> None:
        """
        Cleanup plugin resources.
        """

        pass



# ============================================================
# Plugin Runtime State
# ============================================================


class EventPluginState(str, Enum):
    """
    Plugin lifecycle states.
    """

    LOADED = "loaded"

    ACTIVE = "active"

    DISABLED = "disabled"

    FAILED = "failed"



# ============================================================
# Loaded Plugin Record
# ============================================================


@dataclass(slots=True)
class LoadedEventPlugin:
    """
    Runtime plugin record.
    """

    plugin: EventPlugin

    state: EventPluginState = (
        EventPluginState.LOADED
    )

    loaded_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    error: Optional[str] = None



# ============================================================
# Event Plugin Manager
# ============================================================


class EventPluginManager:
    """
    Controls event plugins.
    """

    def __init__(
        self,
    ) -> None:

        self._plugins: Dict[
            str,
            LoadedEventPlugin
        ] = {}

        self._lock = threading.RLock()



    def load(
        self,
        plugin: EventPlugin,
    ) -> None:
        """
        Load plugin.
        """

        name = (
            plugin.metadata.name
        )


        record = LoadedEventPlugin(
            plugin=plugin
        )


        with self._lock:

            self._plugins[
                name
            ] = record



        try:

            plugin.initialize(
                event_system
            )


            plugin.register(
                enterprise_event_registry
            )


            record.state = (
                EventPluginState.ACTIVE
            )


        except Exception as exc:

            record.state = (
                EventPluginState.FAILED
            )

            record.error = str(
                exc
            )



    def unload(
        self,
        name: str,
    ) -> None:
        """
        Remove plugin.
        """

        with self._lock:

            record = (
                self._plugins.pop(
                    name,
                    None,
                )
            )


        if record:

            record.plugin.shutdown()



    def get(
        self,
        name: str,
    ) -> Optional[
        LoadedEventPlugin
    ]:

        with self._lock:

            return self._plugins.get(
                name
            )



    def all(
        self,
    ) -> list[LoadedEventPlugin]:

        with self._lock:

            return list(
                self._plugins.values()
            )



# ============================================================
# Plugin Discovery Interface
# ============================================================


class EventPluginDiscovery:
    """
    Discovers plugins dynamically.

    Future support:
    - Python packages
    - External modules
    - Plugin marketplace
    """

    def discover(
        self,
    ) -> list[EventPlugin]:
        """
        Return available plugins.
        """

        return []



# ============================================================
# Global Plugin Manager
# ============================================================


event_plugin_manager = (
    EventPluginManager()
)

event_plugin_discovery = (
    EventPluginDiscovery()
)

# core/events.py
# Part 8 — Continued
# Event API Gateway, Remote Dispatch and Service Communication


# ============================================================
# Remote Event Request
# ============================================================


@dataclass(slots=True)
class RemoteEventRequest:
    """
    Represents an external event request.

    Used by:
    - REST API
    - WebSocket
    - External services
    """

    event_name: str

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    source: Optional[str] = None

    request_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Remote Event Response
# ============================================================


@dataclass(slots=True)
class RemoteEventResponse:
    """
    Response returned after dispatch.
    """

    request_id: str

    success: bool

    data: Any = None

    error: Optional[str] = None

    completed_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Event API Gateway
# ============================================================


class EventAPIGateway:
    """
    Entry point for external systems.

    Provides:
    - Validation
    - Authentication hook
    - Event creation
    - Dispatch
    """

    def __init__(
        self,
        pipeline:
            EventPipeline,
    ) -> None:

        self.pipeline = pipeline



    def dispatch(
        self,
        request:
            RemoteEventRequest,
    ) -> RemoteEventResponse:
        """
        Convert request into event.
        """

        try:

            event = EventFactory.create(
                name=request.event_name,
                payload=request.payload,
                category=(
                    EventCategory.SYSTEM
                ),
            )


            result = (
                self.pipeline.execute(
                    event
                )
            )


            return RemoteEventResponse(
                request_id=request.request_id,
                success=True,
                data=result,
            )



        except Exception as exc:

            return RemoteEventResponse(
                request_id=request.request_id,
                success=False,
                error=str(exc),
            )



# ============================================================
# Event Service Endpoint
# ============================================================


class EventServiceEndpoint:
    """
    Internal service communication layer.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self.name = name

        self.enabled = True



    def receive(
        self,
        message: EventMessage,
    ) -> Any:
        """
        Receive service message.
        """

        if not self.enabled:

            raise RuntimeError(
                "Endpoint disabled"
            )


        return event_message_router.route(
            message
        )



    def enable(
        self,
    ) -> None:

        self.enabled = True



    def disable(
        self,
    ) -> None:

        self.enabled = False



# ============================================================
# Event Service Registry
# ============================================================


class EventServiceRegistry:
    """
    Stores internal services.
    """

    def __init__(
        self,
    ) -> None:

        self._services: Dict[
            str,
            EventServiceEndpoint
        ] = {}

        self._lock = threading.RLock()



    def register(
        self,
        service:
            EventServiceEndpoint,
    ) -> None:

        with self._lock:

            self._services[
                service.name
            ] = service



    def get(
        self,
        name: str,
    ) -> Optional[
        EventServiceEndpoint
    ]:

        with self._lock:

            return self._services.get(
                name
            )



    def remove(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._services.pop(
                name,
                None,
            )



# ============================================================
# Event Gateway Middleware
# ============================================================


class EventGatewayMiddleware(
    EventMiddleware
):
    """
    Adds gateway metadata.
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            "gateway"
        )



    def before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:

        event.metadata.tags.add(
            "external"
        )

        return event



# ============================================================
# Global Gateway Objects
# ============================================================


event_api_gateway = EventAPIGateway(
    event_pipeline
)


event_service_registry = (
    EventServiceRegistry()
)

# core/events.py
# Part 8 — Continued
# Event Backup, Persistence Export and Recovery Snapshots


# ============================================================
# Event Backup Record
# ============================================================


@dataclass(slots=True)
class EventBackupRecord:
    """
    Represents a stored backup point.
    """

    backup_id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    event_count: int = 0

    location: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Event Backup Manager
# ============================================================


class EventBackupManager:
    """
    Handles event system backups.

    Provides:
    - Snapshot creation
    - Export
    - Restore preparation
    """

    def __init__(
        self,
        store: EventStore,
    ) -> None:

        self.store = store

        self._backups: Dict[
            str,
            EventBackupRecord
        ] = {}

        self._lock = threading.RLock()



    def create_backup(
        self,
        location:
            Optional[str] = None,
    ) -> EventBackupRecord:
        """
        Create backup record.
        """

        snapshots = (
            self.store.list_all()
        )


        record = EventBackupRecord(
            event_count=len(
                snapshots
            ),
            location=location,
            metadata={
                "created":
                    datetime.now(
                        UTC
                    ).isoformat()
            },
        )


        with self._lock:

            self._backups[
                record.backup_id
            ] = record


        return record



    def list_backups(
        self,
    ) -> list[EventBackupRecord]:

        with self._lock:

            return list(
                self._backups.values()
            )



# ============================================================
# Event Snapshot Manager
# ============================================================


class EventSnapshotManager:
    """
    Creates complete system snapshots.

    Includes:
    - Events
    - Diagnostics
    - Metrics
    - Configuration
    """

    def create(
        self,
    ) -> Dict[str, Any]:
        """
        Generate snapshot package.
        """

        return {
            "timestamp":
                datetime.now(
                    UTC
                ).isoformat(),

            "events":
                [
                    asdict(item)
                    for item
                    in event_store.list_all()
                ],

            "metrics":
                event_metrics_exporter.export(),

            "health":
                asdict(
                    event_health_monitor.check()
                ),

            "configuration":
                asdict(
                    event_config_manager.get()
                ),
        }



    def export_json(
        self,
    ) -> str:
        """
        Export snapshot JSON.
        """

        return json.dumps(
            self.create(),
            default=str,
            ensure_ascii=False,
        )



# ============================================================
# Recovery Point
# ============================================================


@dataclass(slots=True)
class EventRecoveryPoint:
    """
    Point-in-time recovery marker.
    """

    id: str = field(
        default_factory=lambda:
            uuid.uuid4().hex
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    event_ids: list[str] = field(
        default_factory=list
    )



# ============================================================
# Recovery Point Manager
# ============================================================


class EventRecoveryPointManager:
    """
    Manages recovery checkpoints.
    """

    def __init__(
        self,
    ) -> None:

        self._points: Dict[
            str,
            EventRecoveryPoint
        ] = {}

        self._lock = threading.RLock()



    def create(
        self,
    ) -> EventRecoveryPoint:
        """
        Create checkpoint.
        """

        point = EventRecoveryPoint(
            event_ids=[
                item.event_id
                for item
                in event_store.list_all()
            ]
        )


        with self._lock:

            self._points[
                point.id
            ] = point


        return point



    def get(
        self,
        point_id: str,
    ) -> Optional[
        EventRecoveryPoint
    ]:

        with self._lock:

            return self._points.get(
                point_id
            )



# ============================================================
# Global Backup Objects
# ============================================================


event_backup_manager = (
    EventBackupManager(
        event_store
    )
)


event_snapshot_manager = (
    EventSnapshotManager()
)


event_recovery_point_manager = (
    EventRecoveryPointManager()
)

# core/events.py
# Part 9
# Event Rules Engine, Automation and Conditional Execution


# ============================================================
# Event Rule Action
# ============================================================


class EventRuleAction(str, Enum):
    """
    Actions performed by rules.
    """

    ALLOW = "allow"

    BLOCK = "block"

    MODIFY = "modify"

    REDIRECT = "redirect"

    TRIGGER = "trigger"



# ============================================================
# Event Condition
# ============================================================


@dataclass(slots=True)
class EventCondition:
    """
    Condition used by rule engine.
    """

    field: str

    operator: str

    value: Any



    def evaluate(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Evaluate condition.
        """

        current = (
            event.payload.get(
                self.field
            )
        )


        if self.operator == "equals":

            return (
                current
                ==
                self.value
            )


        if self.operator == "contains":

            return (
                self.value
                in
                current
                if current
                else False
            )


        if self.operator == "exists":

            return current is not None


        if self.operator == "greater":

            return (
                current
                >
                self.value
            )


        if self.operator == "less":

            return (
                current
                <
                self.value
            )


        return False



# ============================================================
# Event Rule
# ============================================================


@dataclass(slots=True)
class EventRule:
    """
    Automation rule definition.
    """

    name: str

    event_pattern: str

    conditions: list[
        EventCondition
    ] = field(
        default_factory=list
    )

    action: EventRuleAction = (
        EventRuleAction.ALLOW
    )

    enabled: bool = True

    priority: int = 0



    def matches(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Check rule matching.
        """

        if not self.enabled:

            return False


        if not EventMatcher.match_name(
            event,
            self.event_pattern,
        ):

            return False


        for condition in (
            self.conditions
        ):

            if not condition.evaluate(
                event
            ):

                return False


        return True



# ============================================================
# Event Rule Engine
# ============================================================


class EventRuleEngine:
    """
    Executes event automation rules.

    Used by:
    - Workflow
    - Runtime automation
    - Plugins
    """

    def __init__(
        self,
    ) -> None:

        self._rules: list[
            EventRule
        ] = []

        self._lock = threading.RLock()



    def register(
        self,
        rule: EventRule,
    ) -> None:
        """
        Add automation rule.
        """

        with self._lock:

            self._rules.append(
                rule
            )


            self._rules.sort(
                key=lambda item:
                    item.priority,
                reverse=True,
            )



    def remove(
        self,
        name: str,
    ) -> None:

        with self._lock:

            self._rules = [
                rule
                for rule
                in self._rules
                if rule.name != name
            ]



    def evaluate(
        self,
        event: BaseEvent,
    ) -> list[EventRule]:
        """
        Return matching rules.
        """

        result = []


        with self._lock:

            rules = list(
                self._rules
            )


        for rule in rules:

            if rule.matches(
                event
            ):

                result.append(
                    rule
                )


        return result



# ============================================================
# Rule Middleware
# ============================================================


class EventRuleMiddleware(
    EventMiddleware
):
    """
    Applies rule engine before execution.
    """

    def __init__(
        self,
        engine:
            EventRuleEngine,
    ) -> None:

        super().__init__(
            "rules"
        )

        self.engine = engine



    def before(
        self,
        event: BaseEvent,
    ) -> BaseEvent:

        rules = (
            self.engine.evaluate(
                event
            )
        )


        for rule in rules:

            if (
                rule.action
                ==
                EventRuleAction.BLOCK
            ):

                raise RuntimeError(
                    f"Blocked by rule: "
                    f"{rule.name}"
                )


            if (
                rule.action
                ==
                EventRuleAction.MODIFY
            ):

                event.metadata.tags.add(
                    "modified_by_rule"
                )


        return event



# ============================================================
# Global Rule Engine
# ============================================================


event_rule_engine = (
    EventRuleEngine()
)

# core/events.py
# Part 9 — Continued
# Event Data Validation, Schemas and Type Safety


# ============================================================
# Event Schema Field
# ============================================================


@dataclass(slots=True)
class EventSchemaField:
    """
    Defines a payload field schema.
    """

    name: str

    field_type: Type

    required: bool = True

    default: Any = None

    description: str = ""



# ============================================================
# Event Schema
# ============================================================


@dataclass(slots=True)
class EventSchema:
    """
    Defines structure of event payload.
    """

    name: str

    fields: list[
        EventSchemaField
    ] = field(
        default_factory=list
    )

    version: str = "1.0"



    def validate(
        self,
        payload: Dict[str, Any],
    ) -> bool:
        """
        Validate payload.
        """

        for field_info in self.fields:

            if (
                field_info.name
                not in payload
            ):

                if field_info.required:

                    raise ValueError(
                        f"Missing field: "
                        f"{field_info.name}"
                    )

                continue


            value = payload[
                field_info.name
            ]


            if not isinstance(
                value,
                field_info.field_type,
            ):

                raise TypeError(
                    f"Invalid type for "
                    f"{field_info.name}"
                )


        return True



# ============================================================
# Event Schema Registry
# ============================================================


class EventSchemaRegistry:
    """
    Stores event schemas.
    """

    def __init__(
        self,
    ) -> None:

        self._schemas: Dict[
            str,
            EventSchema
        ] = {}

        self._lock = threading.RLock()



    def register(
        self,
        schema: EventSchema,
    ) -> None:

        with self._lock:

            self._schemas[
                schema.name
            ] = schema



    def get(
        self,
        name: str,
    ) -> Optional[
        EventSchema
    ]:

        with self._lock:

            return self._schemas.get(
                name
            )



    def validate(
        self,
        event: BaseEvent,
    ) -> bool:
        """
        Validate event payload.
        """

        schema = self.get(
            event.name
        )


        if schema is None:

            return True


        return schema.validate(
            event.payload
        )



# ============================================================
# Typed Event Factory
# ============================================================


class TypedEventFactory:
    """
    Creates validated events.
    """

    def __init__(
        self,
        schemas:
            EventSchemaRegistry,
    ) -> None:

        self.schemas = schemas



    def create(
        self,
        name: str,
        payload: Dict[str, Any],
    ) -> BaseEvent:
        """
        Create validated event.
        """

        event = EventFactory.create(
            name=name,
            payload=payload,
        )


        self.schemas.validate(
            event
        )


        return event



# ============================================================
# Schema Migration Support
# ============================================================


@dataclass(slots=True)
class SchemaMigration:
    """
    Migrates payload between versions.
    """

    source_version: str

    target_version: str

    migrate: Callable[
        [Dict[str, Any]],
        Dict[str, Any]
    ]



class SchemaMigrationManager:
    """
    Handles schema upgrades.
    """

    def __init__(
        self,
    ) -> None:

        self._migrations: list[
            SchemaMigration
        ] = []



    def register(
        self,
        migration:
            SchemaMigration,
    ) -> None:

        self._migrations.append(
            migration
        )



    def migrate(
        self,
        payload: Dict[str, Any],
        source: str,
        target: str,
    ) -> Dict[str, Any]:

        result = payload


        for migration in (
            self._migrations
        ):

            if (
                migration.source_version
                ==
                source
                and
                migration.target_version
                ==
                target
            ):

                result = (
                    migration.migrate(
                        result
                    )
                )


        return result



# ============================================================
# Global Schema Objects
# ============================================================


event_schema_registry = (
    EventSchemaRegistry()
)


typed_event_factory = (
    TypedEventFactory(
        event_schema_registry
    )
)


schema_migration_manager = (
    SchemaMigrationManager()
)

# core/events.py
# Part 10
# Event Shared State Synchronization and Runtime Coordination


# ============================================================
# Event State Change
# ============================================================


@dataclass(slots=True)
class EventStateChange:
    """
    Represents a state mutation caused by event.
    """

    key: str

    old_value: Any

    new_value: Any

    event_id: str

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Shared State Adapter
# ============================================================


class EventStateAdapter:
    """
    Interface between event system
    and shared state manager.

    Integration point for:
    - core/shared_state.py
    - Workspace state
    - Runtime state
    """

    def get(
        self,
        key: str,
    ) -> Any:
        """
        Read state value.
        """

        raise NotImplementedError



    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Update state value.
        """

        raise NotImplementedError



# ============================================================
# In Memory State Adapter
# ============================================================


class MemoryStateAdapter(
    EventStateAdapter
):
    """
    Default internal state storage.
    """

    def __init__(
        self,
    ) -> None:

        self._state: Dict[
            str,
            Any
        ] = {}

        self._lock = threading.RLock()



    def get(
        self,
        key: str,
    ) -> Any:

        with self._lock:

            return self._state.get(
                key
            )



    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        with self._lock:

            self._state[key] = value



# ============================================================
# State Synchronizer
# ============================================================


class EventStateSynchronizer:
    """
    Synchronizes event changes
    with shared state.
    """

    def __init__(
        self,
        adapter:
            EventStateAdapter,
    ) -> None:

        self.adapter = adapter

        self._changes: list[
            EventStateChange
        ] = []

        self._lock = threading.RLock()



    def apply(
        self,
        event: BaseEvent,
        key: str,
        value: Any,
    ) -> EventStateChange:
        """
        Apply state change.
        """

        old = self.adapter.get(
            key
        )


        self.adapter.set(
            key,
            value,
        )


        change = EventStateChange(
            key=key,
            old_value=old,
            new_value=value,
            event_id=event.id,
        )


        with self._lock:

            self._changes.append(
                change
            )


        return change



    def history(
        self,
    ) -> list[EventStateChange]:

        with self._lock:

            return list(
                self._changes
            )



# ============================================================
# Runtime Event Context
# ============================================================


@dataclass(slots=True)
class RuntimeEventContext:
    """
    Runtime execution metadata.
    """

    runtime_id: str

    workspace_id: Optional[str] = None

    session_id: Optional[str] = None

    worker_id: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Runtime Coordinator
# ============================================================


class RuntimeEventCoordinator:
    """
    Connects runtime lifecycle
    with event engine.
    """

    def __init__(
        self,
    ) -> None:

        self.contexts: Dict[
            str,
            RuntimeEventContext
        ] = {}

        self._lock = threading.RLock()



    def register(
        self,
        context:
            RuntimeEventContext,
    ) -> None:

        with self._lock:

            self.contexts[
                context.runtime_id
            ] = context



    def remove(
        self,
        runtime_id: str,
    ) -> None:

        with self._lock:

            self.contexts.pop(
                runtime_id,
                None,
            )



    def get(
        self,
        runtime_id: str,
    ) -> Optional[
        RuntimeEventContext
    ]:

        with self._lock:

            return self.contexts.get(
                runtime_id
            )



# ============================================================
# Global State Integration
# ============================================================


event_state_adapter = (
    MemoryStateAdapter()
)


event_state_synchronizer = (
    EventStateSynchronizer(
        event_state_adapter
    )
)


runtime_event_coordinator = (
    RuntimeEventCoordinator()
)

# core/events.py
# Part 10 — Continued
# Workspace Integration, Resource Tracking and Event Binding


# ============================================================
# Workspace Event Binding
# ============================================================


@dataclass(slots=True)
class WorkspaceEventBinding:
    """
    Connects workspace lifecycle events
    with event system.
    """

    workspace_id: str

    enabled: bool = True

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================
# Workspace Event Manager
# ============================================================


class WorkspaceEventManager:
    """
    Manages workspace related events.

    Integration with:
    - workspace.py
    - project manager
    - asset registry
    """

    def __init__(
        self,
    ) -> None:

        self._bindings: Dict[
            str,
            WorkspaceEventBinding
        ] = {}

        self._lock = threading.RLock()



    def bind(
        self,
        workspace_id: str,
    ) -> WorkspaceEventBinding:
        """
        Create workspace binding.
        """

        binding = WorkspaceEventBinding(
            workspace_id=workspace_id
        )


        with self._lock:

            self._bindings[
                workspace_id
            ] = binding


        return binding



    def unbind(
        self,
        workspace_id: str,
    ) -> None:

        with self._lock:

            self._bindings.pop(
                workspace_id,
                None,
            )



    def exists(
        self,
        workspace_id: str,
    ) -> bool:

        with self._lock:

            return (
                workspace_id
                in
                self._bindings
            )



# ============================================================
# Resource Event Tracking
# ============================================================


@dataclass(slots=True)
class ResourceEventRecord:
    """
    Tracks resource activity.
    """

    resource_id: str

    resource_type: str

    action: str

    event_id: str

    timestamp: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Resource Event Tracker
# ============================================================


class ResourceEventTracker:
    """
    Tracks:
    - Files
    - Assets
    - Projects
    - Models
    """

    def __init__(
        self,
    ) -> None:

        self._records: list[
            ResourceEventRecord
        ] = []

        self._lock = threading.RLock()



    def record(
        self,
        resource_id: str,
        resource_type: str,
        action: str,
        event: BaseEvent,
    ) -> ResourceEventRecord:
        """
        Store resource action.
        """

        record = ResourceEventRecord(
            resource_id=resource_id,
            resource_type=resource_type,
            action=action,
            event_id=event.id,
        )


        with self._lock:

            self._records.append(
                record
            )


        return record



    def get_history(
        self,
        resource_id: str,
    ) -> list[ResourceEventRecord]:

        with self._lock:

            return [
                item
                for item
                in self._records
                if item.resource_id
                ==
                resource_id
            ]



# ============================================================
# File Watch Event
# ============================================================


@dataclass(slots=True)
class FileChangeEvent:
    """
    Represents file system change.
    """

    path: str

    action: str

    modified_time: float

    size: int



# ============================================================
# File Watcher Bridge
# ============================================================


class EventFileWatcherBridge:
    """
    Connects filesystem changes
    to event engine.

    Future integration:
    - watchdog library
    - auto reload
    - cache invalidation
    """

    def __init__(
        self,
    ) -> None:

        self.enabled = True



    def publish_change(
        self,
        change: FileChangeEvent,
    ) -> BaseEvent:
        """
        Convert file change into event.
        """

        event = EventFactory.create(
            name="file.changed",
            payload={
                "path":
                    change.path,

                "action":
                    change.action,

                "size":
                    change.size,
            },
            category=(
                EventCategory.SYSTEM
            ),
        )


        if self.enabled:

            event_queue.push(
                event
            )


        return event



# ============================================================
# Global Workspace / Resource Objects
# ============================================================


workspace_event_manager = (
    WorkspaceEventManager()
)


resource_event_tracker = (
    ResourceEventTracker()
)


event_file_watcher_bridge = (
    EventFileWatcherBridge()
)

