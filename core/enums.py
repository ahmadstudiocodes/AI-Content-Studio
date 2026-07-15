# core/enums.py

from __future__ import annotations

from enum import Enum, IntEnum, StrEnum, auto
from typing import Any


class BaseEnum(Enum):
    """
    Base enum class for Arman StudioOS.

    Provides:
    - Safe string conversion
    - Serialization support
    - Comparison helpers
    """

    def __str__(self) -> str:
        return self.value if isinstance(self.value, str) else self.name

    def serialize(self) -> Any:
        return self.value

    @classmethod
    def from_value(cls, value: Any):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(
            f"{value!r} is not a valid {cls.__name__}"
        )


class BaseStrEnum(str, BaseEnum):
    """
    String based enum foundation.
    """

    def __str__(self) -> str:
        return self.value


class BaseIntEnum(IntEnum):
    """
    Integer based enum foundation.
    """

    pass


class AutoEnum(BaseEnum):
    """
    Auto generated enum values.
    """

    def _generate_next_value_(
        name,
        start,
        count,
        last_values
    ):
        return name.lower()


# ==========================================================
# Framework Identity
# ==========================================================


class FrameworkMode(BaseStrEnum):
    """
    Running mode of StudioOS framework.
    """

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class EnvironmentType(BaseStrEnum):
    """
    Deployment environment.
    """

    LOCAL = "local"
    SERVER = "server"
    CLOUD = "cloud"
    EDGE = "edge"


class ComponentStatus(BaseStrEnum):
    """
    Generic lifecycle status for framework components.
    """

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    DISABLED = "disabled"


class HealthStatus(BaseStrEnum):
    """
    Universal health states.
    """

    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class OperationResult(BaseStrEnum):
    """
    Generic operation result.
    """

    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    SKIPPED = "skipped"


class PriorityLevel(IntEnum):
    """
    Universal priority system.
    """

    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    CRITICAL = 100
# ==========================================================
# Application Lifecycle
# ==========================================================


class ApplicationState(BaseStrEnum):
    """
    Global application state.
    """

    CREATED = "created"
    BOOTSTRAPPING = "bootstrapping"
    INITIALIZING = "initializing"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    RESUMING = "resuming"
    STOPPING = "stopping"
    STOPPED = "stopped"
    RESTARTING = "restarting"
    TERMINATED = "terminated"
    FAILED = "failed"


class StartupMode(BaseStrEnum):
    """
    Application startup strategies.
    """

    NORMAL = "normal"
    SAFE = "safe"
    RECOVERY = "recovery"
    DEBUG = "debug"
    MINIMAL = "minimal"


class ShutdownMode(BaseStrEnum):
    """
    Application shutdown strategies.
    """

    NORMAL = "normal"
    FORCE = "force"
    GRACEFUL = "graceful"
    EMERGENCY = "emergency"


# ==========================================================
# Runtime
# ==========================================================


class RuntimeState(BaseStrEnum):
    """
    Runtime execution state.
    """

    OFFLINE = "offline"
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    SUSPENDED = "suspended"
    DRAINING = "draining"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class RuntimeMode(BaseStrEnum):
    """
    Runtime operating modes.
    """

    SINGLE = "single"
    MULTI = "multi"
    DISTRIBUTED = "distributed"
    ISOLATED = "isolated"
    CLUSTER = "cluster"


class ExecutionMode(BaseStrEnum):
    """
    Task execution modes.
    """

    SYNC = "sync"
    ASYNC = "async"
    BATCH = "batch"
    STREAM = "stream"
    PARALLEL = "parallel"


class ExecutionPriority(IntEnum):
    """
    Runtime execution priority.
    """

    BACKGROUND = 10
    LOW = 25
    NORMAL = 50
    HIGH = 75
    URGENT = 90
    CRITICAL = 100


# ==========================================================
# Lifecycle Framework
# ==========================================================


class LifecyclePhase(BaseStrEnum):
    """
    Universal component lifecycle phases.
    """

    CREATED = "created"

    PRE_INIT = "pre_init"
    INITIALIZING = "initializing"
    POST_INIT = "post_init"

    STARTING = "starting"
    STARTED = "started"

    ACTIVE = "active"

    STOPPING = "stopping"
    STOPPED = "stopped"

    CLEANUP = "cleanup"
    DESTROYED = "destroyed"


class LifecycleAction(BaseStrEnum):
    """
    Lifecycle operations.
    """

    CREATE = "create"
    INITIALIZE = "initialize"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    STOP = "stop"
    RESTART = "restart"
    DESTROY = "destroy"


class ServiceState(BaseStrEnum):
    """
    Service manager states.
    """

    REGISTERED = "registered"
    LOADING = "loading"
    LOADED = "loaded"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"

# ==========================================================
# Logging System
# ==========================================================


class LogLevel(IntEnum):
    """
    Standard logging severity levels.
    Compatible with common logging systems.
    """

    TRACE = 5
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class LogCategory(BaseStrEnum):
    """
    Log classification categories.
    """

    SYSTEM = "system"
    APPLICATION = "application"
    RUNTIME = "runtime"
    SECURITY = "security"
    PERFORMANCE = "performance"
    NETWORK = "network"
    DATABASE = "database"
    AI = "ai"
    AGENT = "agent"
    WORKFLOW = "workflow"
    USER = "user"


class AuditType(BaseStrEnum):
    """
    Audit event types.
    """

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

    LOGIN = "login"
    LOGOUT = "logout"

    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"

    CONFIG_CHANGED = "config_changed"
    PERMISSION_CHANGED = "permission_changed"


class AuditResult(BaseStrEnum):
    """
    Audit operation results.
    """

    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


# ==========================================================
# Monitoring System
# ==========================================================


class MetricType(BaseStrEnum):
    """
    Monitoring metric types.
    """

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"
    RATE = "rate"


class MonitoringState(BaseStrEnum):
    """
    Monitoring subsystem state.
    """

    DISABLED = "disabled"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"


class DiagnosticLevel(IntEnum):
    """
    Diagnostic verbosity.
    """

    NONE = 0
    BASIC = 1
    NORMAL = 2
    DETAILED = 3
    FULL = 4


class HealthCheckType(BaseStrEnum):
    """
    Health check categories.
    """

    SYSTEM = "system"
    RUNTIME = "runtime"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    SERVICE = "service"
    DEPENDENCY = "dependency"


class HealthCheckResult(BaseStrEnum):
    """
    Health check execution result.
    """

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    UNKNOWN = "unknown"


# ==========================================================
# Alerting
# ==========================================================


class AlertSeverity(IntEnum):
    """
    Alert importance level.
    """

    INFO = 10
    NOTICE = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class AlertState(BaseStrEnum):
    """
    Alert lifecycle.
    """

    CREATED = "created"
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    CLOSED = "closed"


class NotificationChannel(BaseStrEnum):
    """
    Notification delivery channels.
    """

    LOG = "log"
    CONSOLE = "console"
    EMAIL = "email"
    WEBHOOK = "webhook"
    API = "api"
# ==========================================================
# Task Execution System
# ==========================================================


class TaskState(BaseStrEnum):
    """
    Task lifecycle states.
    """

    CREATED = "created"
    QUEUED = "queued"
    SCHEDULED = "scheduled"

    WAITING = "waiting"
    PREPARING = "preparing"

    RUNNING = "running"

    PAUSED = "paused"
    RESUMING = "resuming"

    COMPLETED = "completed"

    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskType(BaseStrEnum):
    """
    Task classification.
    """

    SYSTEM = "system"
    USER = "user"

    WORKFLOW = "workflow"
    AGENT = "agent"

    AI_GENERATION = "ai_generation"
    DATA_PROCESSING = "data_processing"

    BACKGROUND = "background"
    MAINTENANCE = "maintenance"


class TaskPriority(IntEnum):
    """
    Task scheduling priority.
    """

    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    URGENT = 90
    CRITICAL = 100


class TaskResult(BaseStrEnum):
    """
    Task execution result.
    """

    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


# ==========================================================
# Queue System
# ==========================================================


class QueueState(BaseStrEnum):
    """
    Task queue states.
    """

    CREATED = "created"
    INITIALIZING = "initializing"

    ACTIVE = "active"
    PAUSED = "paused"

    DRAINING = "draining"

    STOPPING = "stopping"
    STOPPED = "stopped"

    FAILED = "failed"


class QueueType(BaseStrEnum):
    """
    Queue execution models.
    """

    FIFO = "fifo"
    LIFO = "lifo"
    PRIORITY = "priority"
    DELAYED = "delayed"
    STREAM = "stream"


# ==========================================================
# Scheduler System
# ==========================================================


class SchedulerState(BaseStrEnum):
    """
    Scheduler lifecycle.
    """

    CREATED = "created"
    INITIALIZING = "initializing"

    READY = "ready"
    RUNNING = "running"

    PAUSED = "paused"

    DRAINING = "draining"

    STOPPING = "stopping"
    STOPPED = "stopped"

    ERROR = "error"


class TriggerType(BaseStrEnum):
    """
    Scheduler trigger sources.
    """

    MANUAL = "manual"

    TIME = "time"
    CRON = "cron"
    INTERVAL = "interval"

    EVENT = "event"

    DEPENDENCY = "dependency"

    WEBHOOK = "webhook"


class ScheduleStatus(BaseStrEnum):
    """
    Scheduled job state.
    """

    CREATED = "created"
    ACTIVE = "active"

    PAUSED = "paused"

    EXECUTING = "executing"

    COMPLETED = "completed"

    FAILED = "failed"

    DISABLED = "disabled"


# ==========================================================
# Retry / Recovery
# ==========================================================


class RetryPolicy(BaseStrEnum):
    """
    Retry strategies.
    """

    NONE = "none"

    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"

    IMMEDIATE = "immediate"


class RetryState(BaseStrEnum):
    """
    Retry lifecycle.
    """

    NOT_REQUIRED = "not_required"

    PENDING = "pending"

    RETRYING = "retrying"

    EXHAUSTED = "exhausted"

    SUCCESS = "success"
# ==========================================================
# AI Provider System
# ==========================================================


class AIProviderType(BaseStrEnum):
    """
    Supported AI provider categories.
    """

    OPENAI = "openai"
    OLLAMA = "ollama"
    LM_STUDIO = "lm_studio"

    GEMINI = "gemini"
    CLAUDE = "claude"

    GROQ = "groq"
    OPENROUTER = "openrouter"

    CUSTOM = "custom"


class ProviderStatus(BaseStrEnum):
    """
    AI provider lifecycle state.
    """

    UNKNOWN = "unknown"

    REGISTERED = "registered"

    INITIALIZING = "initializing"

    AVAILABLE = "available"

    BUSY = "busy"

    UNAVAILABLE = "unavailable"

    ERROR = "error"

    DISABLED = "disabled"


class ModelType(BaseStrEnum):
    """
    AI model categories.
    """

    CHAT = "chat"

    COMPLETION = "completion"

    EMBEDDING = "embedding"

    IMAGE = "image"

    AUDIO = "audio"

    VIDEO = "video"

    MULTIMODAL = "multimodal"


class ModelCapability(BaseStrEnum):
    """
    Model supported capabilities.
    """

    TEXT_GENERATION = "text_generation"

    REASONING = "reasoning"

    CODE_GENERATION = "code_generation"

    ANALYSIS = "analysis"

    TRANSLATION = "translation"

    SUMMARIZATION = "summarization"

    EMBEDDING = "embedding"

    VISION = "vision"

    AUDIO_PROCESSING = "audio_processing"


# ==========================================================
# AI Execution
# ==========================================================


class GenerationMode(BaseStrEnum):
    """
    AI generation strategies.
    """

    STANDARD = "standard"

    CREATIVE = "creative"

    PRECISE = "precise"

    FAST = "fast"

    BALANCED = "balanced"


class PromptRole(BaseStrEnum):
    """
    Prompt message roles.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"

    CONTEXT = "context"


class AIRequestState(BaseStrEnum):
    """
    AI request lifecycle.
    """

    CREATED = "created"

    QUEUED = "queued"

    PROCESSING = "processing"

    STREAMING = "streaming"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class AIResponseStatus(BaseStrEnum):
    """
    AI response result.
    """

    SUCCESS = "success"

    PARTIAL = "partial"

    EMPTY = "empty"

    FAILED = "failed"


# ==========================================================
# Agent AI Modes
# ==========================================================


class AgentAIMode(BaseStrEnum):
    """
    AI behavior modes for agents.
    """

    AUTONOMOUS = "autonomous"

    ASSISTED = "assisted"

    SUPERVISED = "supervised"

    DETERMINISTIC = "deterministic"

    EXPLORATORY = "exploratory"


class ContextType(BaseStrEnum):
    """
    AI context sources.
    """

    USER = "user"

    MEMORY = "memory"

    WORKSPACE = "workspace"

    SYSTEM = "system"

    TOOL = "tool"

    EXTERNAL = "external"


class EmbeddingType(BaseStrEnum):
    """
    Embedding strategies.
    """

    TEXT = "text"

    DOCUMENT = "document"

    CODE = "code"

    IMAGE = "image"

    MULTIMODAL = "multimodal"

# ==========================================================
# Agent Framework
# ==========================================================


class AgentType(BaseStrEnum):
    """
    Agent classification.
    """

    GENERAL = "general"

    PLANNER = "planner"

    RESEARCH = "research"

    ARCHITECTURE = "architecture"

    SCRIPT = "script"

    THUMBNAIL = "thumbnail"

    VIDEO = "video"

    COURSE = "course"

    PUBLISH = "publish"

    MEMORY = "memory"

    CUSTOM = "custom"


class AgentState(BaseStrEnum):
    """
    Agent lifecycle states.
    """

    CREATED = "created"

    REGISTERED = "registered"

    INITIALIZING = "initializing"

    READY = "ready"

    IDLE = "idle"

    THINKING = "thinking"

    EXECUTING = "executing"

    WAITING = "waiting"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

    DISABLED = "disabled"


class AgentRole(BaseStrEnum):
    """
    Agent responsibility role.
    """

    EXECUTOR = "executor"

    PLANNER = "planner"

    ANALYST = "analyst"

    COORDINATOR = "coordinator"

    SUPERVISOR = "supervisor"

    SPECIALIST = "specialist"


class AgentCapability(BaseStrEnum):
    """
    Agent capability types.
    """

    REASONING = "reasoning"

    PLANNING = "planning"

    MEMORY = "memory"

    TOOL_USE = "tool_use"

    GENERATION = "generation"

    ANALYSIS = "analysis"

    VALIDATION = "validation"


# ==========================================================
# Brain System
# ==========================================================


class BrainMode(BaseStrEnum):
    """
    Brain operating modes.
    """

    NORMAL = "normal"

    FAST = "fast"

    DEEP = "deep"

    CREATIVE = "creative"

    SAFE = "safe"


class ReasoningMode(BaseStrEnum):
    """
    Reasoning strategies.
    """

    DIRECT = "direct"

    STEP_BY_STEP = "step_by_step"

    TREE_SEARCH = "tree_search"

    REFLECTIVE = "reflective"

    HYBRID = "hybrid"


class DecisionType(BaseStrEnum):
    """
    Brain decision categories.
    """

    ACTION = "action"

    ROUTING = "routing"

    PLANNING = "planning"

    APPROVAL = "approval"

    RETRY = "retry"

    TERMINATION = "termination"


class MemoryContextPriority(IntEnum):
    """
    Brain memory importance.
    """

    LOW = 25

    NORMAL = 50

    HIGH = 75

    CRITICAL = 100


# ==========================================================
# Workflow Engine
# ==========================================================


class WorkflowState(BaseStrEnum):
    """
    Workflow lifecycle.
    """

    CREATED = "created"

    VALIDATING = "validating"

    READY = "ready"

    RUNNING = "running"

    PAUSED = "paused"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class WorkflowStepState(BaseStrEnum):
    """
    Workflow step execution state.
    """

    PENDING = "pending"

    READY = "ready"

    RUNNING = "running"

    SUCCESS = "success"

    FAILED = "failed"

    SKIPPED = "skipped"

    RETRYING = "retrying"


class WorkflowType(BaseStrEnum):
    """
    Workflow categories.
    """

    LINEAR = "linear"

    CONDITIONAL = "conditional"

    PARALLEL = "parallel"

    PIPELINE = "pipeline"

    EVENT_DRIVEN = "event_driven"


class PipelineStage(BaseStrEnum):
    """
    AI content pipeline stages.
    """

    INPUT = "input"

    ANALYSIS = "analysis"

    PLANNING = "planning"

    GENERATION = "generation"

    VALIDATION = "validation"

    OPTIMIZATION = "optimization"

    OUTPUT = "output"
# ==========================================================
# Memory System
# ==========================================================


class MemoryType(BaseStrEnum):
    """
    Memory storage categories.
    """

    SHORT_TERM = "short_term"

    LONG_TERM = "long_term"

    WORKING = "working"

    EPISODIC = "episodic"

    SEMANTIC = "semantic"

    PROCEDURAL = "procedural"


class MemoryScope(BaseStrEnum):
    """
    Memory ownership scope.
    """

    GLOBAL = "global"

    APPLICATION = "application"

    WORKSPACE = "workspace"

    PROJECT = "project"

    SESSION = "session"

    AGENT = "agent"

    USER = "user"


class MemoryOperation(BaseStrEnum):
    """
    Memory operations.
    """

    CREATE = "create"

    READ = "read"

    UPDATE = "update"

    DELETE = "delete"

    SEARCH = "search"

    COMPRESS = "compress"

    RESTORE = "restore"


class StorageType(BaseStrEnum):
    """
    Storage backend types.
    """

    MEMORY = "memory"

    FILE = "file"

    SQLITE = "sqlite"

    DATABASE = "database"

    VECTOR = "vector"

    CLOUD = "cloud"


# ==========================================================
# Workspace System
# ==========================================================


class WorkspaceState(BaseStrEnum):
    """
    Workspace lifecycle.
    """

    CREATED = "created"

    INITIALIZING = "initializing"

    OPENING = "opening"

    OPEN = "open"

    ACTIVE = "active"

    LOCKED = "locked"

    CLOSING = "closing"

    CLOSED = "closed"

    ARCHIVED = "archived"

    DELETED = "deleted"

    FAILED = "failed"


class WorkspaceMode(BaseStrEnum):
    """
    Workspace operation modes.
    """

    NORMAL = "normal"

    READ_ONLY = "read_only"

    RECOVERY = "recovery"

    MAINTENANCE = "maintenance"


class WorkspaceOperation(BaseStrEnum):
    """
    Workspace actions.
    """

    CREATE = "create"

    OPEN = "open"

    CLOSE = "close"

    CLONE = "clone"

    ARCHIVE = "archive"

    RESTORE = "restore"

    DELETE = "delete"


# ==========================================================
# Project Management
# ==========================================================


class ProjectState(BaseStrEnum):
    """
    Project lifecycle states.
    """

    CREATED = "created"

    PLANNING = "planning"

    ACTIVE = "active"

    PAUSED = "paused"

    COMPLETED = "completed"

    ARCHIVED = "archived"

    CANCELLED = "cancelled"


class ProjectType(BaseStrEnum):
    """
    Project categories.
    """

    CONTENT = "content"

    ARCHITECTURE = "architecture"

    RESEARCH = "research"

    DEVELOPMENT = "development"

    CUSTOM = "custom"


class AssetType(BaseStrEnum):
    """
    Project asset categories.
    """

    DOCUMENT = "document"

    IMAGE = "image"

    VIDEO = "video"

    AUDIO = "audio"

    MODEL = "model"

    CODE = "code"

    DATA = "data"

    CONFIGURATION = "configuration"


# ==========================================================
# Session + Snapshot + Versioning
# ==========================================================


class SessionState(BaseStrEnum):
    """
    User/runtime session states.
    """

    CREATED = "created"

    ACTIVE = "active"

    IDLE = "idle"

    EXPIRED = "expired"

    CLOSED = "closed"


class SnapshotType(BaseStrEnum):
    """
    Snapshot categories.
    """

    MANUAL = "manual"

    AUTO = "auto"

    RECOVERY = "recovery"

    BACKUP = "backup"


class VersionState(BaseStrEnum):
    """
    Version lifecycle.
    """

    CREATED = "created"

    CURRENT = "current"

    SUPERSEDED = "superseded"

    RESTORED = "restored"

    DELETED = "deleted"
# ==========================================================
# Event System
# ==========================================================


class EventType(BaseStrEnum):
    """
    Event classification.
    """

    SYSTEM = "system"

    APPLICATION = "application"

    RUNTIME = "runtime"

    WORKSPACE = "workspace"

    PROJECT = "project"

    AGENT = "agent"

    AI = "ai"

    TASK = "task"

    WORKFLOW = "workflow"

    SECURITY = "security"

    HEALTH = "health"

    CUSTOM = "custom"


class EventPriority(IntEnum):
    """
    Event processing priority.
    """

    LOWEST = 0

    LOW = 25

    NORMAL = 50

    HIGH = 75

    CRITICAL = 100


class EventState(BaseStrEnum):
    """
    Event lifecycle.
    """

    CREATED = "created"

    QUEUED = "queued"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"

    RETRYING = "retrying"

    DISCARDED = "discarded"


class EventDeliveryMode(BaseStrEnum):
    """
    Event delivery strategies.
    """

    SYNC = "sync"

    ASYNC = "async"

    BROADCAST = "broadcast"

    QUEUE = "queue"


# ==========================================================
# Plugin System
# ==========================================================


class PluginState(BaseStrEnum):
    """
    Plugin lifecycle.
    """

    REGISTERED = "registered"

    LOADING = "loading"

    LOADED = "loaded"

    ENABLED = "enabled"

    DISABLED = "disabled"

    RUNNING = "running"

    STOPPING = "stopping"

    FAILED = "failed"


class PluginType(BaseStrEnum):
    """
    Plugin categories.
    """

    CORE = "core"

    PROVIDER = "provider"

    AGENT = "agent"

    TOOL = "tool"

    INTEGRATION = "integration"

    EXTENSION = "extension"


class PluginCapability(BaseStrEnum):
    """
    Plugin capabilities.
    """

    EVENT_HANDLER = "event_handler"

    SERVICE = "service"

    STORAGE = "storage"

    UI = "ui"

    PROVIDER = "provider"

    WORKFLOW = "workflow"


# ==========================================================
# Hook System
# ==========================================================


class HookType(BaseStrEnum):
    """
    Hook execution points.
    """

    PRE_INIT = "pre_init"

    POST_INIT = "post_init"

    PRE_EXECUTE = "pre_execute"

    POST_EXECUTE = "post_execute"

    BEFORE_SAVE = "before_save"

    AFTER_SAVE = "after_save"

    BEFORE_CLOSE = "before_close"

    AFTER_CLOSE = "after_close"

    ERROR = "error"


class HookState(BaseStrEnum):
    """
    Hook lifecycle.
    """

    REGISTERED = "registered"

    ACTIVE = "active"

    EXECUTING = "executing"

    COMPLETED = "completed"

    FAILED = "failed"

    DISABLED = "disabled"


# ==========================================================
# Integration Layer
# ==========================================================


class IntegrationStatus(BaseStrEnum):
    """
    External/internal integration state.
    """

    UNKNOWN = "unknown"

    CONNECTING = "connecting"

    CONNECTED = "connected"

    DISCONNECTED = "disconnected"

    DEGRADED = "degraded"

    FAILED = "failed"


class IntegrationType(BaseStrEnum):
    """
    Integration categories.
    """

    API = "api"

    DATABASE = "database"

    CLOUD = "cloud"

    AI_PROVIDER = "ai_provider"

    STORAGE = "storage"

    WEBHOOK = "webhook"


class MessageType(BaseStrEnum):
    """
    Internal communication message types.
    """

    COMMAND = "command"

    REQUEST = "request"

    RESPONSE = "response"

    EVENT = "event"

    NOTIFICATION = "notification"

    BROADCAST = "broadcast"
# ==========================================================
# Security System
# ==========================================================


class SecurityState(BaseStrEnum):
    """
    Global security subsystem state.
    """

    DISABLED = "disabled"

    INITIALIZING = "initializing"

    ACTIVE = "active"

    LOCKED = "locked"

    COMPROMISED = "compromised"

    RECOVERING = "recovering"

    FAILED = "failed"


class PermissionLevel(IntEnum):
    """
    Access permission hierarchy.
    """

    NONE = 0

    GUEST = 10

    USER = 25

    OPERATOR = 50

    ADMIN = 75

    ROOT = 100


class AccessType(BaseStrEnum):
    """
    Resource access operations.
    """

    READ = "read"

    WRITE = "write"

    EXECUTE = "execute"

    DELETE = "delete"

    ADMIN = "admin"


class AuthorizationResult(BaseStrEnum):
    """
    Authorization decision result.
    """

    ALLOWED = "allowed"

    DENIED = "denied"

    EXPIRED = "expired"

    INVALID = "invalid"

    UNKNOWN = "unknown"


# ==========================================================
# Authentication
# ==========================================================


class AuthenticationType(BaseStrEnum):
    """
    Authentication mechanisms.
    """

    NONE = "none"

    PASSWORD = "password"

    TOKEN = "token"

    API_KEY = "api_key"

    CERTIFICATE = "certificate"

    BIOMETRIC = "biometric"


class AuthenticationState(BaseStrEnum):
    """
    Authentication lifecycle.
    """

    UNKNOWN = "unknown"

    PENDING = "pending"

    AUTHENTICATED = "authenticated"

    FAILED = "failed"

    EXPIRED = "expired"

    REVOKED = "revoked"


# ==========================================================
# Encryption & Key Management
# ==========================================================


class EncryptionAlgorithm(BaseStrEnum):
    """
    Supported encryption algorithms.
    """

    AES = "aes"

    RSA = "rsa"

    ECC = "ecc"

    SHA256 = "sha256"

    SHA512 = "sha512"


class EncryptionMode(BaseStrEnum):
    """
    Encryption operation modes.
    """

    NONE = "none"

    SYMMETRIC = "symmetric"

    ASYMMETRIC = "asymmetric"

    HASHING = "hashing"


class KeyStatus(BaseStrEnum):
    """
    Cryptographic key lifecycle.
    """

    CREATED = "created"

    ACTIVE = "active"

    ROTATING = "rotating"

    EXPIRED = "expired"

    REVOKED = "revoked"

    DESTROYED = "destroyed"


class KeyType(BaseStrEnum):
    """
    Cryptographic key types.
    """

    MASTER = "master"

    SESSION = "session"

    API = "api"

    SIGNING = "signing"

    ENCRYPTION = "encryption"


# ==========================================================
# Threat Detection
# ==========================================================


class ThreatLevel(IntEnum):
    """
    Security threat severity.
    """

    NONE = 0

    LOW = 25

    MEDIUM = 50

    HIGH = 75

    CRITICAL = 100


class SecurityEventType(BaseStrEnum):
    """
    Security related events.
    """

    LOGIN_SUCCESS = "login_success"

    LOGIN_FAILED = "login_failed"

    ACCESS_DENIED = "access_denied"

    PERMISSION_CHANGED = "permission_changed"

    KEY_ROTATED = "key_rotated"

    INTRUSION_DETECTED = "intrusion_detected"

    POLICY_VIOLATION = "policy_violation"
# ==========================================================
# Networking System
# ==========================================================


class NetworkState(BaseStrEnum):
    """
    Network subsystem state.
    """

    OFFLINE = "offline"

    CONNECTING = "connecting"

    CONNECTED = "connected"

    DEGRADED = "degraded"

    DISCONNECTED = "disconnected"

    FAILED = "failed"


class NetworkProtocol(BaseStrEnum):
    """
    Supported communication protocols.
    """

    HTTP = "http"

    HTTPS = "https"

    TCP = "tcp"

    UDP = "udp"

    WEBSOCKET = "websocket"

    GRPC = "grpc"


# ==========================================================
# API Layer
# ==========================================================


class APIStatus(BaseStrEnum):
    """
    API lifecycle status.
    """

    CREATED = "created"

    INITIALIZING = "initializing"

    AVAILABLE = "available"

    BUSY = "busy"

    DEGRADED = "degraded"

    DISABLED = "disabled"

    FAILED = "failed"


class RequestMethod(BaseStrEnum):
    """
    HTTP/API request methods.
    """

    GET = "get"

    POST = "post"

    PUT = "put"

    PATCH = "patch"

    DELETE = "delete"

    STREAM = "stream"


class ResponseStatus(IntEnum):
    """
    Generic API response status.
    """

    SUCCESS = 200

    CREATED = 201

    ACCEPTED = 202

    BAD_REQUEST = 400

    UNAUTHORIZED = 401

    FORBIDDEN = 403

    NOT_FOUND = 404

    SERVER_ERROR = 500


# ==========================================================
# System Architecture
# ==========================================================


class SystemArchitecture(BaseStrEnum):
    """
    StudioOS deployment architecture.
    """

    SINGLE_PROCESS = "single_process"

    MULTI_PROCESS = "multi_process"

    DISTRIBUTED = "distributed"

    CLUSTERED = "clustered"

    HYBRID = "hybrid"


class PlatformType(BaseStrEnum):
    """
    Execution platforms.
    """

    WINDOWS = "windows"

    LINUX = "linux"

    MACOS = "macos"

    SERVER = "server"

    CLOUD = "cloud"

    CONTAINER = "container"


class ResourceType(BaseStrEnum):
    """
    System resources.
    """

    CPU = "cpu"

    GPU = "gpu"

    MEMORY = "memory"

    STORAGE = "storage"

    NETWORK = "network"

    PROCESS = "process"


# ==========================================================
# Cache System
# ==========================================================


class CachePolicy(BaseStrEnum):
    """
    Cache behavior policies.
    """

    NONE = "none"

    MEMORY = "memory"

    DISK = "disk"

    DISTRIBUTED = "distributed"

    HYBRID = "hybrid"


class CacheState(BaseStrEnum):
    """
    Cache lifecycle.
    """

    EMPTY = "empty"

    LOADING = "loading"

    READY = "ready"

    EXPIRED = "expired"

    INVALID = "invalid"


# ==========================================================
# Backup & Recovery
# ==========================================================


class BackupState(BaseStrEnum):
    """
    Backup lifecycle.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    RESTORING = "restoring"

    RESTORED = "restored"


class BackupType(BaseStrEnum):
    """
    Backup strategies.
    """

    FULL = "full"

    INCREMENTAL = "incremental"

    DIFFERENTIAL = "differential"

    SNAPSHOT = "snapshot"


class MigrationState(BaseStrEnum):
    """
    Migration lifecycle.
    """

    CREATED = "created"

    PREPARING = "preparing"

    RUNNING = "running"

    VALIDATING = "validating"

    COMPLETED = "completed"

    FAILED = "failed"

    ROLLED_BACK = "rolled_back"


# ==========================================================
# Framework Final States
# ==========================================================


class SystemMode(BaseStrEnum):
    """
    Overall StudioOS mode.
    """

    NORMAL = "normal"

    SAFE = "safe"

    RECOVERY = "recovery"

    MAINTENANCE = "maintenance"

    EMERGENCY = "emergency"


class FeatureState(BaseStrEnum):
    """
    Feature availability.
    """

    ENABLED = "enabled"

    DISABLED = "disabled"

    EXPERIMENTAL = "experimental"

    DEPRECATED = "deprecated"


class OperationMode(BaseStrEnum):
    """
    Generic operation mode.
    """

    AUTOMATIC = "automatic"

    MANUAL = "manual"

    HYBRID = "hybrid"