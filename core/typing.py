# core/typing.py

from __future__ import annotations

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generic,
    Iterator,
    Mapping,
    MutableMapping,
    Protocol,
    Sequence,
    Type,
    TypeVar,
)


# ==========================================================
# Generic Variables
# ==========================================================


T = TypeVar(
    "T"
)

K = TypeVar(
    "K"
)

V = TypeVar(
    "V"
)

R = TypeVar(
    "R"
)

E = TypeVar(
    "E",
)


# ==========================================================
# Primitive Aliases
# ==========================================================


JSONPrimitive = (
    str
    | int
    | float
    | bool
    | None
)


JSONType = (
    JSONPrimitive
    | list["JSONType"]
    | dict[str, "JSONType"]
)


Metadata = dict[
    str,
    Any,
]


Context = dict[
    str,
    Any,
]


Parameters = dict[
    str,
    Any,
]


Headers = dict[
    str,
    str,
]


Tags = list[
    str
]


# ==========================================================
# Callable Types
# ==========================================================


SyncCallable = Callable[
    ...,
    T,
]


AsyncCallable = Callable[
    ...,
    Awaitable[T],
]


CoroutineCallable = Callable[
    ...,
    Coroutine[
        Any,
        Any,
        T,
    ],
]


Callback = Callable[
    ...,
    Any,
]


Handler = Callable[
    ...,
    Any,
]


# ==========================================================
# Collection Types
# ==========================================================


StringMap = MutableMapping[
    str,
    str,
]


ObjectMap = MutableMapping[
    str,
    Any,
]


ReadOnlyMap = Mapping[
    str,
    Any,
]


ItemSequence = Sequence[
    T
]


ItemIterator = Iterator[
    T
]


# ==========================================================
# Class Types
# ==========================================================


ClassType = Type[
    T
]


Factory = Callable[
    [],
    T,
]


Builder = Callable[
    [
        Parameters
    ],
    T,
]

# ==========================================================
# Identifier Foundation
# ==========================================================


class SupportsID(Protocol):
    """
    Contract for identifiable objects.
    """

    id: str


# ==========================================================
# Base Identifier Types
# ==========================================================


NewType = TypeVar(
    "NewType"
)


class Identifier(Generic[T]):
    """
    Generic strongly typed identifier.
    """

    def __init__(
        self,
        value: str,
    ):
        self.value = value


    def __str__(
        self,
    ) -> str:
        return self.value


    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.value})"
        )


# ==========================================================
# Entity Identifiers
# ==========================================================


class WorkspaceID(
    Identifier["WorkspaceID"]
):
    """
    Workspace identifier.
    """

    pass


class ProjectID(
    Identifier["ProjectID"]
):
    """
    Project identifier.
    """

    pass


class SessionID(
    Identifier["SessionID"]
):
    """
    Session identifier.
    """

    pass


class TaskID(
    Identifier["TaskID"]
):
    """
    Task identifier.
    """

    pass


class AgentID(
    Identifier["AgentID"]
):
    """
    Agent identifier.
    """

    pass


class EventID(
    Identifier["EventID"]
):
    """
    Event identifier.
    """

    pass


class PluginID(
    Identifier["PluginID"]
):
    """
    Plugin identifier.
    """

    pass


class ProviderID(
    Identifier["ProviderID"]
):
    """
    Provider identifier.
    """

    pass


# ==========================================================
# Resource References
# ==========================================================


class ResourceType(str):
    """
    Generic resource category.
    """

    pass


class ResourceReference(
    Generic[T]
):
    """
    Reference to framework resource.
    """

    def __init__(
        self,
        resource_id: Identifier[T],
        resource_type: ResourceType,
    ):

        self.resource_id = resource_id

        self.resource_type = resource_type


# ==========================================================
# Entity Key
# ==========================================================


class EntityKey:
    """
    Unique entity lookup key.
    """

    def __init__(
        self,
        namespace: str,
        name: str,
    ):

        self.namespace = namespace

        self.name = name


    def __str__(
        self,
    ) -> str:

        return (
            f"{self.namespace}:"
            f"{self.name}"
        )
    
# ==========================================================
# Error Information Types
# ==========================================================


class ErrorInfo:
    """
    Structured error information.
    """

    def __init__(
        self,
        code: str,
        message: str,
        details: Metadata | None = None,
    ):

        self.code = code

        self.message = message

        self.details = details or {}


# ==========================================================
# Result Base Contract
# ==========================================================


class SupportsResult(Protocol[T]):
    """
    Result compatible object.
    """

    success: bool

    value: T | None

    error: ErrorInfo | None


# ==========================================================
# Generic Result Type
# ==========================================================


class Result(
    Generic[T]
):
    """
    Universal operation result.

    Used by:
    - Runtime
    - Agents
    - Providers
    - Workspace
    """

    def __init__(
        self,
        success: bool,
        value: T | None = None,
        error: ErrorInfo | None = None,
    ):

        self.success = success

        self.value = value

        self.error = error


    @classmethod
    def ok(
        cls,
        value: T | None = None,
    ) -> "Result[T]":

        return cls(
            success=True,
            value=value,
        )


    @classmethod
    def fail(
        cls,
        code: str,
        message: str,
        details: Metadata | None = None,
    ) -> "Result[T]":

        return cls(
            success=False,
            error=ErrorInfo(
                code,
                message,
                details,
            ),
        )


    def unwrap(
        self,
    ) -> T:

        if not self.success:

            raise RuntimeError(
                self.error.message
                if self.error
                else "Unknown error"
            )

        return self.value


# ==========================================================
# Specialized Results
# ==========================================================


class Success(
    Result[T]
):
    """
    Successful operation result.
    """

    def __init__(
        self,
        value: T | None = None,
    ):

        super().__init__(
            True,
            value=value,
        )


class Failure(
    Result[T]
):
    """
    Failed operation result.
    """

    def __init__(
        self,
        error: ErrorInfo,
    ):

        super().__init__(
            False,
            error=error,
        )


# ==========================================================
# Async Result Types
# ==========================================================


AsyncResult = Awaitable[
    Result[T]
]


AsyncCallbackResult = Callable[
    ...,
    AsyncResult[T],
]


# ==========================================================
# Operation Contracts
# ==========================================================


class Operation(Generic[T]):
    """
    Operation execution contract.
    """

    name: str


    def execute(
        self,
        context: Context | None = None,
    ) -> Result[T]:
        ...

# ==========================================================
# Execution Context Types
# ==========================================================


class ExecutionContext:
    """
    Shared runtime execution context.

    Passed between:
    - Runtime
    - Agents
    - Tasks
    - Workflows
    """

    def __init__(
        self,
        execution_id: str,
        metadata: Metadata | None = None,
    ):

        self.execution_id = execution_id

        self.metadata = metadata or {}


# ==========================================================
# Task Execution Types
# ==========================================================


class TaskCallable(
    Protocol[T]
):
    """
    Contract for executable tasks.
    """

    def __call__(
        self,
        context: ExecutionContext,
    ) -> Result[T]:
        ...


class AsyncTaskCallable(
    Protocol[T]
):
    """
    Async task execution contract.
    """

    async def __call__(
        self,
        context: ExecutionContext,
    ) -> Result[T]:
        ...


# ==========================================================
# Runtime Callable Types
# ==========================================================


RuntimeCallable = Callable[
    [
        ExecutionContext
    ],
    Result[Any],
]


AsyncRuntimeCallable = Callable[
    [
        ExecutionContext
    ],
    Awaitable[
        Result[Any]
    ],
]


# ==========================================================
# Worker Types
# ==========================================================


class WorkerProtocol(
    Protocol
):
    """
    Runtime worker contract.
    """

    id: str


    def start(
        self,
    ) -> None:
        ...


    def stop(
        self,
    ) -> None:
        ...


    def execute(
        self,
        task: TaskCallable[Any],
        context: ExecutionContext,
    ) -> Result[Any]:
        ...


# ==========================================================
# Scheduler Contracts
# ==========================================================


class ScheduleEntry:
    """
    Scheduler task definition.
    """

    def __init__(
        self,
        task_id: str,
        schedule: str,
        callback: RuntimeCallable,
    ):

        self.task_id = task_id

        self.schedule = schedule

        self.callback = callback


class SchedulerProtocol(
    Protocol
):
    """
    Scheduler interface.
    """

    def register(
        self,
        entry: ScheduleEntry,
    ) -> None:
        ...


    def remove(
        self,
        task_id: str,
    ) -> None:
        ...


    def start(
        self,
    ) -> None:
        ...


    def stop(
        self,
    ) -> None:
        ...


# ==========================================================
# Lifecycle Callback Types
# ==========================================================


LifecycleCallback = Callable[
    [],
    None,
]


AsyncLifecycleCallback = Callable[
    [],
    Awaitable[
        None
    ],
]

# ==========================================================
# Event Base Types
# ==========================================================


class EventBase(
    Protocol
):
    """
    Base event contract.
    """

    id: EventID

    name: str

    timestamp: float

    payload: Mapping[
        str,
        Any,
    ]


# ==========================================================
# Event Envelope
# ==========================================================


class EventEnvelope(
    Generic[T]
):
    """
    Event transport wrapper.
    """

    def __init__(
        self,
        event: T,
        source: str,
        metadata: Metadata | None = None,
    ):

        self.event = event

        self.source = source

        self.metadata = metadata or {}


# ==========================================================
# Event Handler Contracts
# ==========================================================


class EventHandler(
    Protocol[T]
):
    """
    Event handler interface.
    """

    def handle(
        self,
        event: T,
    ) -> Result[Any]:
        ...


class AsyncEventHandler(
    Protocol[T]
):
    """
    Async event handler interface.
    """

    async def handle(
        self,
        event: T,
    ) -> Result[Any]:
        ...


# ==========================================================
# Publisher / Subscriber Contracts
# ==========================================================


class Publisher(
    Protocol
):
    """
    Event publisher contract.
    """

    def publish(
        self,
        event: EventBase,
    ) -> Result[bool]:
        ...


class Subscriber(
    Protocol
):
    """
    Event subscriber contract.
    """

    def subscribe(
        self,
        event_type: Type[Any],
        handler: EventHandler[Any],
    ) -> Result[bool]:
        ...


    def unsubscribe(
        self,
        event_type: Type[Any],
    ) -> Result[bool]:
        ...


# ==========================================================
# Messaging Types
# ==========================================================


class MessageEnvelope(
    Generic[T]
):
    """
    Generic communication envelope.
    """

    def __init__(
        self,
        message_id: str,
        payload: T,
        sender: str,
        receiver: str | None = None,
    ):

        self.message_id = message_id

        self.payload = payload

        self.sender = sender

        self.receiver = receiver


# ==========================================================
# Command Contracts
# ==========================================================


class Command(
    Protocol
):
    """
    Command execution contract.
    """

    name: str


    parameters: Parameters


class CommandHandler(
    Protocol[T]
):
    """
    Command handler contract.
    """

    def execute(
        self,
        command: T,
    ) -> Result[Any]:
        ...

# ==========================================================
# Agent Capability Types
# ==========================================================


class AgentCapability(
    Protocol
):
    """
    Agent ability contract.
    """

    name: str

    description: str


    def execute(
        self,
        input_data: Any,
        context: Context | None = None,
    ) -> Result[Any]:
        ...


# ==========================================================
# Agent Contracts
# ==========================================================


class AgentProtocol(
    Protocol
):
    """
    Core AI agent contract.
    """

    id: AgentID

    name: str


    capabilities: Sequence[
        AgentCapability
    ]


    def initialize(
        self,
    ) -> Result[bool]:
        ...


    def execute(
        self,
        task: Any,
        context: ExecutionContext,
    ) -> Result[Any]:
        ...


    def shutdown(
        self,
    ) -> Result[bool]:
        ...


# ==========================================================
# Agent Communication
# ==========================================================


class AgentMessage:
    """
    Message exchanged between agents.
    """

    def __init__(
        self,
        sender: AgentID,
        receiver: AgentID,
        content: Any,
    ):

        self.sender = sender

        self.receiver = receiver

        self.content = content


# ==========================================================
# Workflow Contracts
# ==========================================================


class WorkflowStep(
    Protocol
):
    """
    Workflow execution step.
    """

    name: str


    def run(
        self,
        context: ExecutionContext,
    ) -> Result[Any]:
        ...


class WorkflowProtocol(
    Protocol
):
    """
    Workflow engine contract.
    """

    id: str

    name: str


    steps: Sequence[
        WorkflowStep
    ]


    def execute(
        self,
        context: ExecutionContext,
    ) -> Result[Any]:
        ...


# ==========================================================
# Planner / Executor Contracts
# ==========================================================


class PlannerProtocol(
    Protocol
):
    """
    Planning agent contract.
    """

    def plan(
        self,
        goal: str,
        context: Context | None = None,
    ) -> Result[list[Any]]:
        ...


class ExecutorProtocol(
    Protocol
):
    """
    Execution agent contract.
    """

    def execute_plan(
        self,
        plan: Sequence[Any],
        context: ExecutionContext,
    ) -> Result[Any]:
        ...


# ==========================================================
# AI Model Request / Response Types
# ==========================================================


class ModelRequest:
    """
    AI model input.
    """

    def __init__(
        self,
        prompt: str,
        parameters: Parameters | None = None,
        context: Context | None = None,
    ):

        self.prompt = prompt

        self.parameters = parameters or {}

        self.context = context or {}


class ModelResponse:
    """
    AI model output.
    """

    def __init__(
        self,
        content: str,
        metadata: Metadata | None = None,
    ):

        self.content = content

        self.metadata = metadata or {}

# ==========================================================
# Memory Types
# ==========================================================


class MemoryEntry:
    """
    Generic memory record.
    """

    def __init__(
        self,
        key: str,
        value: Any,
        metadata: Metadata | None = None,
    ):

        self.key = key

        self.value = value

        self.metadata = metadata or {}


class MemoryQuery:
    """
    Memory search request.
    """

    def __init__(
        self,
        query: str,
        limit: int = 10,
        filters: Metadata | None = None,
    ):

        self.query = query

        self.limit = limit

        self.filters = filters or {}


# ==========================================================
# Memory Contracts
# ==========================================================


class MemoryProtocol(
    Protocol
):
    """
    Memory subsystem contract.
    """

    def store(
        self,
        entry: MemoryEntry,
    ) -> Result[bool]:
        ...


    def retrieve(
        self,
        key: str,
    ) -> Result[MemoryEntry]:
        ...


    def search(
        self,
        query: MemoryQuery,
    ) -> Result[list[MemoryEntry]]:
        ...


    def delete(
        self,
        key: str,
    ) -> Result[bool]:
        ...


# ==========================================================
# Storage Contracts
# ==========================================================


class StorageItem:
    """
    Storage object.
    """

    def __init__(
        self,
        key: str,
        data: Any,
    ):

        self.key = key

        self.data = data


class StorageProtocol(
    Protocol
):
    """
    Persistent storage interface.
    """

    def save(
        self,
        item: StorageItem,
    ) -> Result[bool]:
        ...


    def load(
        self,
        key: str,
    ) -> Result[StorageItem]:
        ...


    def remove(
        self,
        key: str,
    ) -> Result[bool]:
        ...


    def exists(
        self,
        key: str,
    ) -> bool:
        ...


# ==========================================================
# Workspace Contracts
# ==========================================================


class WorkspaceMetadata:
    """
    Workspace information.
    """

    def __init__(
        self,
        name: str,
        path: str,
        metadata: Metadata | None = None,
    ):

        self.name = name

        self.path = path

        self.metadata = metadata or {}


class WorkspaceProtocol(
    Protocol
):
    """
    Enterprise workspace contract.
    """

    id: WorkspaceID

    metadata: WorkspaceMetadata


    def create(
        self,
    ) -> Result[bool]:
        ...


    def open(
        self,
    ) -> Result[bool]:
        ...


    def close(
        self,
    ) -> Result[bool]:
        ...


    def delete(
        self,
    ) -> Result[bool]:
        ...


# ==========================================================
# Project Contracts
# ==========================================================


class ProjectProtocol(
    Protocol
):
    """
    Project management contract.
    """

    id: ProjectID

    name: str


    def initialize(
        self,
    ) -> Result[bool]:
        ...


    def save(
        self,
    ) -> Result[bool]:
        ...


# ==========================================================
# Snapshot / Recovery Types
# ==========================================================


class Snapshot:
    """
    State snapshot.
    """

    def __init__(
        self,
        snapshot_id: str,
        state: Mapping[str, Any],
    ):

        self.snapshot_id = snapshot_id

        self.state = state


class RecoveryPoint:
    """
    Recovery checkpoint.
    """

    def __init__(
        self,
        name: str,
        snapshot: Snapshot,
    ):

        self.name = name

        self.snapshot = snapshot

# ==========================================================
# Plugin Types
# ==========================================================


class PluginMetadata:
    """
    Plugin information.
    """

    def __init__(
        self,
        name: str,
        version: str,
        description: str = "",
        author: str = "",
    ):

        self.name = name

        self.version = version

        self.description = description

        self.author = author


class PluginContext:
    """
    Context passed to plugins.
    """

    def __init__(
        self,
        config: Metadata | None = None,
        services: Metadata | None = None,
    ):

        self.config = config or {}

        self.services = services or {}


# ==========================================================
# Plugin Contract
# ==========================================================


class PluginProtocol(
    Protocol
):
    """
    Plugin lifecycle contract.
    """

    metadata: PluginMetadata


    def install(
        self,
        context: PluginContext,
    ) -> Result[bool]:
        ...


    def enable(
        self,
    ) -> Result[bool]:
        ...


    def disable(
        self,
    ) -> Result[bool]:
        ...


    def uninstall(
        self,
    ) -> Result[bool]:
        ...


# ==========================================================
# Provider Types
# ==========================================================


class ProviderMetadata:
    """
    AI provider information.
    """

    def __init__(
        self,
        name: str,
        version: str,
        capabilities: Sequence[str],
    ):

        self.name = name

        self.version = version

        self.capabilities = capabilities


class ProviderRequest:
    """
    Provider input request.
    """

    def __init__(
        self,
        model: str,
        prompt: str,
        parameters: Parameters | None = None,
    ):

        self.model = model

        self.prompt = prompt

        self.parameters = parameters or {}


class ProviderResponse:
    """
    Provider generated response.
    """

    def __init__(
        self,
        content: str,
        usage: Metadata | None = None,
    ):

        self.content = content

        self.usage = usage or {}


# ==========================================================
# Provider Contract
# ==========================================================


class ProviderProtocol(
    Protocol
):
    """
    AI provider interface.
    """

    metadata: ProviderMetadata


    def generate(
        self,
        request: ProviderRequest,
    ) -> Result[ProviderResponse]:
        ...


    def health_check(
        self,
    ) -> Result[bool]:
        ...


# ==========================================================
# Integration Types
# ==========================================================


class IntegrationConfig:
    """
    External integration settings.
    """

    def __init__(
        self,
        name: str,
        endpoint: str | None = None,
        metadata: Metadata | None = None,
    ):

        self.name = name

        self.endpoint = endpoint

        self.metadata = metadata or {}


class IntegrationProtocol(
    Protocol
):
    """
    External service integration.
    """

    name: str


    def connect(
        self,
    ) -> Result[bool]:
        ...


    def disconnect(
        self,
    ) -> Result[bool]:
        ...


    def send(
        self,
        data: Any,
    ) -> Result[Any]:
        ...


# ==========================================================
# Hook Contracts
# ==========================================================


class HookProtocol(
    Protocol
):
    """
    Generic lifecycle hook.
    """

    name: str


    def execute(
        self,
        context: Context,
    ) -> Result[Any]:
        ...

# ==========================================================
# Security Identity Types
# ==========================================================


class UserIdentity:
    """
    User/service identity.
    """

    def __init__(
        self,
        user_id: str,
        name: str,
        metadata: Metadata | None = None,
    ):

        self.user_id = user_id

        self.name = name

        self.metadata = metadata or {}


class SecurityToken:
    """
    Authentication token.
    """

    def __init__(
        self,
        value: str,
        expires_at: float | None = None,
    ):

        self.value = value

        self.expires_at = expires_at


# ==========================================================
# Permission Contracts
# ==========================================================


class Permission:
    """
    Access permission definition.
    """

    def __init__(
        self,
        resource: str,
        action: str,
    ):

        self.resource = resource

        self.action = action


class SecurityContext:
    """
    Security execution context.
    """

    def __init__(
        self,
        identity: UserIdentity | None = None,
        permissions: Sequence[Permission] | None = None,
    ):

        self.identity = identity

        self.permissions = permissions or []


class AuthorizationProtocol(
    Protocol
):
    """
    Authorization service contract.
    """

    def check(
        self,
        context: SecurityContext,
        permission: Permission,
    ) -> bool:
        ...


# ==========================================================
# Audit Types
# ==========================================================


class AuditRecord:
    """
    Security audit event.
    """

    def __init__(
        self,
        action: str,
        actor: UserIdentity | None = None,
        metadata: Metadata | None = None,
    ):

        self.action = action

        self.actor = actor

        self.metadata = metadata or {}


class AuditProtocol(
    Protocol
):
    """
    Audit system contract.
    """

    def record(
        self,
        event: AuditRecord,
    ) -> Result[bool]:
        ...


# ==========================================================
# Metrics Types
# ==========================================================


class MetricValue:
    """
    Metric data point.
    """

    def __init__(
        self,
        name: str,
        value: float,
        tags: Tags | None = None,
    ):

        self.name = name

        self.value = value

        self.tags = tags or []


class MetricsProtocol(
    Protocol
):
    """
    Metrics collector contract.
    """

    def record(
        self,
        metric: MetricValue,
    ) -> Result[bool]:
        ...


    def get(
        self,
        name: str,
    ) -> Result[MetricValue]:
        ...


# ==========================================================
# Health Monitoring Types
# ==========================================================


class HealthStatus(str):
    """
    Component health state.
    """

    pass


class HealthReport:
    """
    Health check response.
    """

    def __init__(
        self,
        component: str,
        status: HealthStatus,
        message: str = "",
    ):

        self.component = component

        self.status = status

        self.message = message


class HealthCheckProtocol(
    Protocol
):
    """
    Health monitoring contract.
    """

    def check_health(
        self,
    ) -> HealthReport:
        ...

# ==========================================================
# Public Type Registry
# ==========================================================


PUBLIC_TYPES = {

    # Generic
    "Metadata": Metadata,
    "Context": Context,
    "Parameters": Parameters,

    # Identifiers
    "WorkspaceID": WorkspaceID,
    "ProjectID": ProjectID,
    "SessionID": SessionID,
    "TaskID": TaskID,
    "AgentID": AgentID,
    "EventID": EventID,
    "PluginID": PluginID,
    "ProviderID": ProviderID,

    # Result
    "Result": Result,
    "Success": Success,
    "Failure": Failure,
    "ErrorInfo": ErrorInfo,

    # Runtime
    "ExecutionContext": ExecutionContext,
    "ScheduleEntry": ScheduleEntry,

    # Events
    "EventEnvelope": EventEnvelope,
    "MessageEnvelope": MessageEnvelope,

    # Agent / Workflow
    "AgentProtocol": AgentProtocol,
    "WorkflowProtocol": WorkflowProtocol,
    "PlannerProtocol": PlannerProtocol,
    "ExecutorProtocol": ExecutorProtocol,

    # Memory
    "MemoryEntry": MemoryEntry,
    "MemoryProtocol": MemoryProtocol,

    # Workspace
    "WorkspaceProtocol": WorkspaceProtocol,
    "ProjectProtocol": ProjectProtocol,

    # Providers
    "ProviderProtocol": ProviderProtocol,
    "ProviderRequest": ProviderRequest,
    "ProviderResponse": ProviderResponse,

    # Plugins
    "PluginProtocol": PluginProtocol,
    "PluginMetadata": PluginMetadata,

    # Security
    "SecurityContext": SecurityContext,
    "Permission": Permission,

    # Observability
    "MetricValue": MetricValue,
    "HealthReport": HealthReport,
}


# ==========================================================
# Export API
# ==========================================================


__all__ = [

    # Generic Types
    "T",
    "K",
    "V",
    "R",
    "E",

    "JSONType",
    "Metadata",
    "Context",
    "Parameters",

    # Callables
    "SyncCallable",
    "AsyncCallable",
    "Callback",
    "Handler",

    # Identifiers
    "WorkspaceID",
    "ProjectID",
    "SessionID",
    "TaskID",
    "AgentID",
    "EventID",
    "PluginID",
    "ProviderID",

    # Results
    "Result",
    "Success",
    "Failure",
    "ErrorInfo",

    # Runtime
    "ExecutionContext",
    "SchedulerProtocol",
    "WorkerProtocol",

    # Events
    "EventEnvelope",
    "EventHandler",
    "Publisher",
    "Subscriber",

    # Agents
    "AgentProtocol",
    "AgentCapability",

    # Workflow
    "WorkflowProtocol",
    "WorkflowStep",

    # Memory
    "MemoryProtocol",

    # Storage
    "StorageProtocol",

    # Workspace
    "WorkspaceProtocol",
    "ProjectProtocol",

    # Plugins
    "PluginProtocol",

    # Providers
    "ProviderProtocol",
    "ProviderRequest",
    "ProviderResponse",

    # Security
    "SecurityContext",
    "AuthorizationProtocol",

    # Observability
    "MetricsProtocol",
    "HealthCheckProtocol",

    # Registry
    "PUBLIC_TYPES",
]