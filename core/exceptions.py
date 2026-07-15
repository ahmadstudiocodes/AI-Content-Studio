# core/exceptions.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


# ==========================================================
# Error Metadata
# ==========================================================


@dataclass(frozen=True)
class ErrorMetadata:
    """
    Structured metadata for framework errors.
    """

    code: str

    category: str

    severity: str

    recoverable: bool = False


# ==========================================================
# Base Framework Exception
# ==========================================================


class StudioOSError(Exception):
    """
    Root exception for Arman StudioOS.

    Every framework exception inherits from this class.
    """

    default_code = "STUDIOOS_ERROR"
    default_category = "system"
    default_severity = "error"
    default_recoverable = False

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        category: str | None = None,
        severity: str | None = None,
        recoverable: bool | None = None,
        details: Mapping[str, Any] | None = None,
    ):
        super().__init__(message)

        self.message = message

        self.metadata = ErrorMetadata(
            code=code or self.default_code,
            category=category or self.default_category,
            severity=severity or self.default_severity,
            recoverable=(
                recoverable
                if recoverable is not None
                else self.default_recoverable
            ),
        )

        self.details = dict(details or {})

    def serialize(self) -> dict[str, Any]:
        """
        Convert exception to transport-safe format.
        """

        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.metadata.code,
            "category": self.metadata.category,
            "severity": self.metadata.severity,
            "recoverable": self.metadata.recoverable,
            "details": self.details,
        }

    def __str__(self) -> str:
        return (
            f"[{self.metadata.code}] "
            f"{self.message}"
        )


# ==========================================================
# Configuration Errors
# ==========================================================


class ConfigurationError(StudioOSError):
    """
    Configuration related failures.
    """

    default_code = "CONFIG_ERROR"
    default_category = "configuration"


class InvalidConfigurationError(ConfigurationError):
    default_code = "INVALID_CONFIGURATION"


class MissingConfigurationError(ConfigurationError):
    default_code = "MISSING_CONFIGURATION"


# ==========================================================
# Initialization Errors
# ==========================================================


class InitializationError(StudioOSError):
    """
    Component initialization failure.
    """

    default_code = "INITIALIZATION_ERROR"
    default_category = "lifecycle"


class StartupError(InitializationError):
    default_code = "STARTUP_ERROR"


class ShutdownError(InitializationError):
    default_code = "SHUTDOWN_ERROR"
# ==========================================================
# Runtime Errors
# ==========================================================


class RuntimeException(StudioOSError):
    """
    Runtime subsystem failures.
    """

    default_code = "RUNTIME_ERROR"
    default_category = "runtime"


class RuntimeStateError(RuntimeException):
    """
    Invalid runtime state transition.
    """

    default_code = "RUNTIME_STATE_ERROR"


class RuntimeExecutionError(RuntimeException):
    """
    Runtime execution failure.
    """

    default_code = "RUNTIME_EXECUTION_ERROR"
    default_recoverable = True


class RuntimeTimeoutError(RuntimeException):
    """
    Runtime operation timeout.
    """

    default_code = "RUNTIME_TIMEOUT"
    default_recoverable = True


# ==========================================================
# Component Errors
# ==========================================================


class ComponentError(StudioOSError):
    """
    Framework component failures.
    """

    default_code = "COMPONENT_ERROR"
    default_category = "component"


class ComponentNotFoundError(ComponentError):
    """
    Requested component does not exist.
    """

    default_code = "COMPONENT_NOT_FOUND"


class ComponentAlreadyExistsError(ComponentError):
    """
    Duplicate component registration.
    """

    default_code = "COMPONENT_ALREADY_EXISTS"


class ComponentInitializationError(ComponentError):
    """
    Component startup failure.
    """

    default_code = "COMPONENT_INITIALIZATION_ERROR"


class ComponentStateError(ComponentError):
    """
    Invalid component lifecycle transition.
    """

    default_code = "COMPONENT_STATE_ERROR"


# ==========================================================
# Service Errors
# ==========================================================


class ServiceError(StudioOSError):
    """
    Service layer failures.
    """

    default_code = "SERVICE_ERROR"
    default_category = "service"


class ServiceUnavailableError(ServiceError):
    """
    Service unavailable.
    """

    default_code = "SERVICE_UNAVAILABLE"
    default_recoverable = True


class ServiceTimeoutError(ServiceError):
    """
    Service timeout.
    """

    default_code = "SERVICE_TIMEOUT"
    default_recoverable = True


class ServiceDependencyError(ServiceError):
    """
    Required service dependency failure.
    """

    default_code = "SERVICE_DEPENDENCY_ERROR"


# ==========================================================
# Dependency Errors
# ==========================================================


class DependencyError(StudioOSError):
    """
    Dependency management failures.
    """

    default_code = "DEPENDENCY_ERROR"
    default_category = "dependency"


class MissingDependencyError(DependencyError):
    """
    Required dependency missing.
    """

    default_code = "MISSING_DEPENDENCY"


class IncompatibleDependencyError(DependencyError):
    """
    Dependency version conflict.
    """

    default_code = "INCOMPATIBLE_DEPENDENCY"


# ==========================================================
# Resource Errors
# ==========================================================


class ResourceError(StudioOSError):
    """
    Resource management failures.
    """

    default_code = "RESOURCE_ERROR"
    default_category = "resource"


class ResourceNotFoundError(ResourceError):
    """
    Resource does not exist.
    """

    default_code = "RESOURCE_NOT_FOUND"


class ResourceBusyError(ResourceError):
    """
    Resource currently locked or busy.
    """

    default_code = "RESOURCE_BUSY"
    default_recoverable = True


class ResourceLimitExceededError(ResourceError):
    """
    Resource quota exceeded.
    """

    default_code = "RESOURCE_LIMIT_EXCEEDED"

    # ==========================================================
# Event System Errors
# ==========================================================


class EventError(StudioOSError):
    """
    EventBus related failures.
    """

    default_code = "EVENT_ERROR"
    default_category = "event"


class EventNotFoundError(EventError):
    """
    Event type or event instance not found.
    """

    default_code = "EVENT_NOT_FOUND"


class EventDispatchError(EventError):
    """
    Event dispatching failure.
    """

    default_code = "EVENT_DISPATCH_ERROR"
    default_recoverable = True


class EventHandlerError(EventError):
    """
    Event handler execution failure.
    """

    default_code = "EVENT_HANDLER_ERROR"


class EventQueueError(EventError):
    """
    Event queue operation failure.
    """

    default_code = "EVENT_QUEUE_ERROR"
    default_recoverable = True


# ==========================================================
# Workflow Errors
# ==========================================================


class WorkflowError(StudioOSError):
    """
    Workflow engine failures.
    """

    default_code = "WORKFLOW_ERROR"
    default_category = "workflow"


class WorkflowNotFoundError(WorkflowError):
    """
    Workflow does not exist.
    """

    default_code = "WORKFLOW_NOT_FOUND"


class WorkflowStateError(WorkflowError):
    """
    Invalid workflow state transition.
    """

    default_code = "WORKFLOW_STATE_ERROR"


class WorkflowExecutionError(WorkflowError):
    """
    Workflow execution failure.
    """

    default_code = "WORKFLOW_EXECUTION_ERROR"
    default_recoverable = True


class WorkflowValidationError(WorkflowError):
    """
    Workflow definition validation failure.
    """

    default_code = "WORKFLOW_VALIDATION_ERROR"


# ==========================================================
# Task Execution Errors
# ==========================================================


class TaskError(StudioOSError):
    """
    Task execution failures.
    """

    default_code = "TASK_ERROR"
    default_category = "task"


class TaskNotFoundError(TaskError):
    """
    Task does not exist.
    """

    default_code = "TASK_NOT_FOUND"


class TaskExecutionError(TaskError):
    """
    Task failed during execution.
    """

    default_code = "TASK_EXECUTION_ERROR"
    default_recoverable = True


class TaskCancelledError(TaskError):
    """
    Task was cancelled.
    """

    default_code = "TASK_CANCELLED"


class TaskTimeoutError(TaskError):
    """
    Task exceeded allowed execution time.
    """

    default_code = "TASK_TIMEOUT"
    default_recoverable = True


# ==========================================================
# Scheduler Errors
# ==========================================================


class SchedulerError(StudioOSError):
    """
    Scheduler subsystem failures.
    """

    default_code = "SCHEDULER_ERROR"
    default_category = "scheduler"


class ScheduleNotFoundError(SchedulerError):
    """
    Scheduled job not found.
    """

    default_code = "SCHEDULE_NOT_FOUND"


class SchedulerStateError(SchedulerError):
    """
    Invalid scheduler state transition.
    """

    default_code = "SCHEDULER_STATE_ERROR"


class SchedulerExecutionError(SchedulerError):
    """
    Scheduled execution failure.
    """

    default_code = "SCHEDULER_EXECUTION_ERROR"
    default_recoverable = True


# ==========================================================
# Retry System Errors
# ==========================================================


class RetryError(StudioOSError):
    """
    Retry engine failures.
    """

    default_code = "RETRY_ERROR"
    default_category = "retry"


class RetryExhaustedError(RetryError):
    """
    All retry attempts consumed.
    """

    default_code = "RETRY_EXHAUSTED"


class RetryConfigurationError(RetryError):
    """
    Invalid retry configuration.
    """

    default_code = "INVALID_RETRY_CONFIGURATION"

# ==========================================================
# AI System Errors
# ==========================================================


class AIError(StudioOSError):
    """
    Root exception for AI subsystem.
    """

    default_code = "AI_ERROR"
    default_category = "ai"


class AIRequestError(AIError):
    """
    AI request processing failure.
    """

    default_code = "AI_REQUEST_ERROR"
    default_recoverable = True


class AIResponseError(AIError):
    """
    Invalid AI response.
    """

    default_code = "AI_RESPONSE_ERROR"


class AIContextError(AIError):
    """
    AI context preparation failure.
    """

    default_code = "AI_CONTEXT_ERROR"


class AIQuotaExceededError(AIError):
    """
    Provider quota limitation.
    """

    default_code = "AI_QUOTA_EXCEEDED"
    default_recoverable = True


# ==========================================================
# Provider Errors
# ==========================================================


class ProviderError(AIError):
    """
    AI provider failures.
    """

    default_code = "PROVIDER_ERROR"
    default_category = "provider"


class ProviderNotFoundError(ProviderError):
    """
    Provider is not registered.
    """

    default_code = "PROVIDER_NOT_FOUND"


class ProviderConnectionError(ProviderError):
    """
    Provider connection failure.
    """

    default_code = "PROVIDER_CONNECTION_ERROR"
    default_recoverable = True


class ProviderUnavailableError(ProviderError):
    """
    Provider temporarily unavailable.
    """

    default_code = "PROVIDER_UNAVAILABLE"
    default_recoverable = True


class ProviderConfigurationError(ProviderError):
    """
    Provider configuration failure.
    """

    default_code = "PROVIDER_CONFIGURATION_ERROR"


# ==========================================================
# Model Errors
# ==========================================================


class ModelError(ProviderError):
    """
    AI model related failures.
    """

    default_code = "MODEL_ERROR"


class ModelNotFoundError(ModelError):
    """
    Requested model unavailable.
    """

    default_code = "MODEL_NOT_FOUND"


class ModelLoadError(ModelError):
    """
    Model loading failure.
    """

    default_code = "MODEL_LOAD_ERROR"


class ModelExecutionError(ModelError):
    """
    Model inference failure.
    """

    default_code = "MODEL_EXECUTION_ERROR"
    default_recoverable = True


# ==========================================================
# Agent Framework Errors
# ==========================================================


class AgentError(StudioOSError):
    """
    Agent subsystem failures.
    """

    default_code = "AGENT_ERROR"
    default_category = "agent"


class AgentNotFoundError(AgentError):
    """
    Agent is not registered.
    """

    default_code = "AGENT_NOT_FOUND"


class AgentStateError(AgentError):
    """
    Invalid agent lifecycle transition.
    """

    default_code = "AGENT_STATE_ERROR"


class AgentExecutionError(AgentError):
    """
    Agent execution failure.
    """

    default_code = "AGENT_EXECUTION_ERROR"
    default_recoverable = True


class AgentCommunicationError(AgentError):
    """
    Agent communication failure.
    """

    default_code = "AGENT_COMMUNICATION_ERROR"
    default_recoverable = True


# ==========================================================
# Brain / Reasoning Errors
# ==========================================================


class BrainError(AgentError):
    """
    Brain engine failures.
    """

    default_code = "BRAIN_ERROR"


class ReasoningError(BrainError):
    """
    Reasoning process failure.
    """

    default_code = "REASONING_ERROR"


class DecisionError(BrainError):
    """
    Decision generation failure.
    """

    default_code = "DECISION_ERROR"


# ==========================================================
# Memory / Context Errors
# ==========================================================


class MemoryError(StudioOSError):
    """
    Memory subsystem failures.
    """

    default_code = "MEMORY_ERROR"
    default_category = "memory"


class MemoryNotFoundError(MemoryError):
    """
    Memory item unavailable.
    """

    default_code = "MEMORY_NOT_FOUND"


class MemoryStorageError(MemoryError):
    """
    Memory persistence failure.
    """

    default_code = "MEMORY_STORAGE_ERROR"


class MemoryCompressionError(MemoryError):
    """
    Memory compression failure.
    """

    default_code = "MEMORY_COMPRESSION_ERROR"


class ContextError(MemoryError):
    """
    Context management failure.
    """

    default_code = "CONTEXT_ERROR"

# ==========================================================
# Workspace Errors
# ==========================================================


class WorkspaceError(StudioOSError):
    """
    Workspace subsystem failures.
    """

    default_code = "WORKSPACE_ERROR"
    default_category = "workspace"


class WorkspaceNotFoundError(WorkspaceError):
    """
    Workspace does not exist.
    """

    default_code = "WORKSPACE_NOT_FOUND"


class WorkspaceLockedError(WorkspaceError):
    """
    Workspace is locked.
    """

    default_code = "WORKSPACE_LOCKED"
    default_recoverable = True


class WorkspaceStateError(WorkspaceError):
    """
    Invalid workspace lifecycle transition.
    """

    default_code = "WORKSPACE_STATE_ERROR"


class WorkspaceRecoveryError(WorkspaceError):
    """
    Workspace recovery failure.
    """

    default_code = "WORKSPACE_RECOVERY_ERROR"


# ==========================================================
# Project Errors
# ==========================================================


class ProjectError(StudioOSError):
    """
    Project management failures.
    """

    default_code = "PROJECT_ERROR"
    default_category = "project"


class ProjectNotFoundError(ProjectError):
    """
    Project unavailable.
    """

    default_code = "PROJECT_NOT_FOUND"


class ProjectConfigurationError(ProjectError):
    """
    Project configuration failure.
    """

    default_code = "PROJECT_CONFIGURATION_ERROR"


class ProjectStateError(ProjectError):
    """
    Invalid project state.
    """

    default_code = "PROJECT_STATE_ERROR"


# ==========================================================
# Asset Management Errors
# ==========================================================


class AssetError(StudioOSError):
    """
    Asset registry failures.
    """

    default_code = "ASSET_ERROR"
    default_category = "asset"


class AssetNotFoundError(AssetError):
    """
    Asset does not exist.
    """

    default_code = "ASSET_NOT_FOUND"


class AssetRegistrationError(AssetError):
    """
    Asset registration failure.
    """

    default_code = "ASSET_REGISTRATION_ERROR"


class AssetValidationError(AssetError):
    """
    Asset validation failure.
    """

    default_code = "ASSET_VALIDATION_ERROR"


# ==========================================================
# Storage Errors
# ==========================================================


class StorageError(StudioOSError):
    """
    Storage subsystem failures.
    """

    default_code = "STORAGE_ERROR"
    default_category = "storage"


class StorageConnectionError(StorageError):
    """
    Storage backend connection failure.
    """

    default_code = "STORAGE_CONNECTION_ERROR"
    default_recoverable = True


class StorageReadError(StorageError):
    """
    Storage read failure.
    """

    default_code = "STORAGE_READ_ERROR"


class StorageWriteError(StorageError):
    """
    Storage write failure.
    """

    default_code = "STORAGE_WRITE_ERROR"


class StorageCorruptionError(StorageError):
    """
    Data corruption detected.
    """

    default_code = "STORAGE_CORRUPTION_ERROR"


# ==========================================================
# Snapshot & Versioning Errors
# ==========================================================


class SnapshotError(StudioOSError):
    """
    Snapshot management failures.
    """

    default_code = "SNAPSHOT_ERROR"
    default_category = "versioning"


class SnapshotCreationError(SnapshotError):
    """
    Snapshot creation failed.
    """

    default_code = "SNAPSHOT_CREATION_ERROR"


class SnapshotRestoreError(SnapshotError):
    """
    Snapshot restoration failed.
    """

    default_code = "SNAPSHOT_RESTORE_ERROR"


class VersionError(StudioOSError):
    """
    Version management failures.
    """

    default_code = "VERSION_ERROR"
    default_category = "versioning"


class VersionConflictError(VersionError):
    """
    Version conflict detected.
    """

    default_code = "VERSION_CONFLICT"


# ==========================================================
# Transaction System
# ==========================================================


class TransactionError(StudioOSError):
    """
    Transaction failures.
    """

    default_code = "TRANSACTION_ERROR"
    default_category = "transaction"


class TransactionConflictError(TransactionError):
    """
    Transaction conflict.
    """

    default_code = "TRANSACTION_CONFLICT"


class RollbackError(TransactionError):
    """
    Rollback operation failure.
    """

    default_code = "ROLLBACK_ERROR"


class CommitError(TransactionError):
    """
    Commit operation failure.
    """

    default_code = "COMMIT_ERROR"

# ==========================================================
# Security Errors
# ==========================================================


class SecurityError(StudioOSError):
    """
    Security subsystem failures.
    """

    default_code = "SECURITY_ERROR"
    default_category = "security"


class AuthenticationError(SecurityError):
    """
    Authentication failures.
    """

    default_code = "AUTHENTICATION_ERROR"


class AuthenticationFailedError(AuthenticationError):
    """
    Invalid authentication attempt.
    """

    default_code = "AUTHENTICATION_FAILED"


class SessionExpiredError(AuthenticationError):
    """
    Session expiration failure.
    """

    default_code = "SESSION_EXPIRED"


class AuthorizationError(SecurityError):
    """
    Authorization failures.
    """

    default_code = "AUTHORIZATION_ERROR"


class PermissionDeniedError(AuthorizationError):
    """
    Access permission denied.
    """

    default_code = "PERMISSION_DENIED"


class SecurityPolicyViolationError(SecurityError):
    """
    Security policy violation.
    """

    default_code = "SECURITY_POLICY_VIOLATION"


# ==========================================================
# Encryption Errors
# ==========================================================


class EncryptionError(SecurityError):
    """
    Encryption subsystem failures.
    """

    default_code = "ENCRYPTION_ERROR"


class EncryptionFailedError(EncryptionError):
    """
    Encryption operation failure.
    """

    default_code = "ENCRYPTION_FAILED"


class DecryptionFailedError(EncryptionError):
    """
    Decryption operation failure.
    """

    default_code = "DECRYPTION_FAILED"


class KeyManagementError(EncryptionError):
    """
    Cryptographic key failures.
    """

    default_code = "KEY_MANAGEMENT_ERROR"


class KeyExpiredError(KeyManagementError):
    """
    Expired cryptographic key.
    """

    default_code = "KEY_EXPIRED"


class KeyRevokedError(KeyManagementError):
    """
    Revoked cryptographic key.
    """

    default_code = "KEY_REVOKED"


# ==========================================================
# Plugin System Errors
# ==========================================================


class PluginError(StudioOSError):
    """
    Plugin framework failures.
    """

    default_code = "PLUGIN_ERROR"
    default_category = "plugin"


class PluginNotFoundError(PluginError):
    """
    Plugin unavailable.
    """

    default_code = "PLUGIN_NOT_FOUND"


class PluginLoadError(PluginError):
    """
    Plugin loading failure.
    """

    default_code = "PLUGIN_LOAD_ERROR"


class PluginInitializationError(PluginError):
    """
    Plugin initialization failure.
    """

    default_code = "PLUGIN_INITIALIZATION_ERROR"


class PluginDependencyError(PluginError):
    """
    Plugin dependency failure.
    """

    default_code = "PLUGIN_DEPENDENCY_ERROR"


class PluginExecutionError(PluginError):
    """
    Plugin runtime failure.
    """

    default_code = "PLUGIN_EXECUTION_ERROR"
    default_recoverable = True


# ==========================================================
# Integration Errors
# ==========================================================


class IntegrationError(StudioOSError):
    """
    Integration layer failures.
    """

    default_code = "INTEGRATION_ERROR"
    default_category = "integration"


class IntegrationConnectionError(IntegrationError):
    """
    External connection failure.
    """

    default_code = "INTEGRATION_CONNECTION_ERROR"
    default_recoverable = True


class IntegrationTimeoutError(IntegrationError):
    """
    Integration timeout.
    """

    default_code = "INTEGRATION_TIMEOUT"
    default_recoverable = True


class IntegrationConfigurationError(IntegrationError):
    """
    Integration configuration failure.
    """

    default_code = "INTEGRATION_CONFIGURATION_ERROR"


# ==========================================================
# API Errors
# ==========================================================


class APIError(IntegrationError):
    """
    API communication failures.
    """

    default_code = "API_ERROR"


class APIRequestError(APIError):
    """
    Invalid API request.
    """

    default_code = "API_REQUEST_ERROR"


class APIResponseError(APIError):
    """
    Invalid API response.
    """

    default_code = "API_RESPONSE_ERROR"


class APIRateLimitError(APIError):
    """
    API rate limitation.
    """

    default_code = "API_RATE_LIMIT"
    default_recoverable = True

# ==========================================================
# Network Errors
# ==========================================================


class NetworkError(StudioOSError):
    """
    Network subsystem failures.
    """

    default_code = "NETWORK_ERROR"
    default_category = "network"


class ConnectionError(NetworkError):
    """
    Connection failures.
    """

    default_code = "CONNECTION_ERROR"
    default_recoverable = True


class ConnectionTimeoutError(ConnectionError):
    """
    Connection timeout.
    """

    default_code = "CONNECTION_TIMEOUT"
    default_recoverable = True


class ConnectionRefusedError(ConnectionError):
    """
    Connection refused.
    """

    default_code = "CONNECTION_REFUSED"


class NetworkUnavailableError(NetworkError):
    """
    Network unavailable.
    """

    default_code = "NETWORK_UNAVAILABLE"
    default_recoverable = True


class ProtocolError(NetworkError):
    """
    Communication protocol failure.
    """

    default_code = "PROTOCOL_ERROR"


# ==========================================================
# System Errors
# ==========================================================


class SystemError(StudioOSError):
    """
    Core operating system failures.
    """

    default_code = "SYSTEM_ERROR"
    default_category = "system"


class HardwareError(SystemError):
    """
    Hardware related failures.
    """

    default_code = "HARDWARE_ERROR"


class CPUError(HardwareError):
    """
    CPU resource failure.
    """

    default_code = "CPU_ERROR"


class GPUError(HardwareError):
    """
    GPU resource failure.
    """

    default_code = "GPU_ERROR"


class MemoryResourceError(SystemError):
    """
    Memory exhaustion or failure.
    """

    default_code = "MEMORY_RESOURCE_ERROR"
    default_recoverable = True


class StorageResourceError(SystemError):
    """
    Storage resource failure.
    """

    default_code = "STORAGE_RESOURCE_ERROR"


# ==========================================================
# Recovery System Errors
# ==========================================================


class RecoveryError(StudioOSError):
    """
    Recovery subsystem failures.
    """

    default_code = "RECOVERY_ERROR"
    default_category = "recovery"


class CrashRecoveryError(RecoveryError):
    """
    Crash recovery failure.
    """

    default_code = "CRASH_RECOVERY_ERROR"


class StateRestoreError(RecoveryError):
    """
    Runtime state restore failure.
    """

    default_code = "STATE_RESTORE_ERROR"


class RecoveryValidationError(RecoveryError):
    """
    Recovery validation failure.
    """

    default_code = "RECOVERY_VALIDATION_ERROR"


# ==========================================================
# Backup Errors
# ==========================================================


class BackupError(StudioOSError):
    """
    Backup subsystem failures.
    """

    default_code = "BACKUP_ERROR"
    default_category = "backup"


class BackupCreationError(BackupError):
    """
    Backup creation failure.
    """

    default_code = "BACKUP_CREATION_ERROR"


class BackupRestoreError(BackupError):
    """
    Backup restoration failure.
    """

    default_code = "BACKUP_RESTORE_ERROR"


class BackupValidationError(BackupError):
    """
    Backup integrity failure.
    """

    default_code = "BACKUP_VALIDATION_ERROR"


# ==========================================================
# Migration Errors
# ==========================================================


class MigrationError(StudioOSError):
    """
    Migration subsystem failures.
    """

    default_code = "MIGRATION_ERROR"
    default_category = "migration"


class MigrationExecutionError(MigrationError):
    """
    Migration execution failure.
    """

    default_code = "MIGRATION_EXECUTION_ERROR"


class MigrationRollbackError(MigrationError):
    """
    Migration rollback failure.
    """

    default_code = "MIGRATION_ROLLBACK_ERROR"

# ==========================================================
# Validation Errors
# ==========================================================


class ValidationError(StudioOSError):
    """
    Data and object validation failures.
    """

    default_code = "VALIDATION_ERROR"
    default_category = "validation"


class InvalidValueError(ValidationError):
    """
    Invalid value provided.
    """

    default_code = "INVALID_VALUE"


class MissingFieldError(ValidationError):
    """
    Required field missing.
    """

    default_code = "MISSING_FIELD"


class ConstraintViolationError(ValidationError):
    """
    Validation constraint violation.
    """

    default_code = "CONSTRAINT_VIOLATION"


class TypeValidationError(ValidationError):
    """
    Invalid data type.
    """

    default_code = "TYPE_VALIDATION_ERROR"


# ==========================================================
# Schema Errors
# ==========================================================


class SchemaError(ValidationError):
    """
    Schema definition failures.
    """

    default_code = "SCHEMA_ERROR"


class InvalidSchemaError(SchemaError):
    """
    Invalid schema structure.
    """

    default_code = "INVALID_SCHEMA"


class SchemaMismatchError(SchemaError):
    """
    Schema compatibility failure.
    """

    default_code = "SCHEMA_MISMATCH"


# ==========================================================
# Serialization Errors
# ==========================================================


class SerializationError(StudioOSError):
    """
    Serialization subsystem failures.
    """

    default_code = "SERIALIZATION_ERROR"
    default_category = "serialization"


class SerializationFailedError(SerializationError):
    """
    Object serialization failure.
    """

    default_code = "SERIALIZATION_FAILED"


class DeserializationError(SerializationError):
    """
    Object deserialization failure.
    """

    default_code = "DESERIALIZATION_ERROR"


class UnsupportedFormatError(SerializationError):
    """
    Unsupported data format.
    """

    default_code = "UNSUPPORTED_FORMAT"


# ==========================================================
# Data Errors
# ==========================================================


class DataError(StudioOSError):
    """
    Data processing failures.
    """

    default_code = "DATA_ERROR"
    default_category = "data"


class DataNotFoundError(DataError):
    """
    Requested data unavailable.
    """

    default_code = "DATA_NOT_FOUND"


class DataIntegrityError(DataError):
    """
    Data integrity violation.
    """

    default_code = "DATA_INTEGRITY_ERROR"


class DataCorruptionError(DataError):
    """
    Corrupted data detected.
    """

    default_code = "DATA_CORRUPTION_ERROR"


class DataFormatError(DataError):
    """
    Invalid data format.
    """

    default_code = "DATA_FORMAT_ERROR"


# ==========================================================
# Parsing Errors
# ==========================================================


class ParsingError(DataError):
    """
    Parsing operation failures.
    """

    default_code = "PARSING_ERROR"


class SyntaxParsingError(ParsingError):
    """
    Syntax parsing failure.
    """

    default_code = "SYNTAX_PARSING_ERROR"


class ContentParsingError(ParsingError):
    """
    Content extraction failure.
    """

    default_code = "CONTENT_PARSING_ERROR"

# ==========================================================
# Concurrency Errors
# ==========================================================


class ConcurrencyError(StudioOSError):
    """
    Concurrency subsystem failures.
    """

    default_code = "CONCURRENCY_ERROR"
    default_category = "concurrency"


class ThreadError(ConcurrencyError):
    """
    Thread management failures.
    """

    default_code = "THREAD_ERROR"


class ThreadCreationError(ThreadError):
    """
    Thread creation failure.
    """

    default_code = "THREAD_CREATION_ERROR"


class ThreadExecutionError(ThreadError):
    """
    Thread execution failure.
    """

    default_code = "THREAD_EXECUTION_ERROR"
    default_recoverable = True


# ==========================================================
# Async Errors
# ==========================================================


class AsyncError(ConcurrencyError):
    """
    Async execution failures.
    """

    default_code = "ASYNC_ERROR"


class AsyncTaskError(AsyncError):
    """
    Async task failure.
    """

    default_code = "ASYNC_TASK_ERROR"


class AsyncTimeoutError(AsyncError):
    """
    Async operation timeout.
    """

    default_code = "ASYNC_TIMEOUT"
    default_recoverable = True


class AsyncCancelledError(AsyncError):
    """
    Async operation cancelled.
    """

    default_code = "ASYNC_CANCELLED"


# ==========================================================
# Locking System Errors
# ==========================================================


class LockError(ConcurrencyError):
    """
    Lock management failures.
    """

    default_code = "LOCK_ERROR"


class LockAcquisitionError(LockError):
    """
    Unable to acquire lock.
    """

    default_code = "LOCK_ACQUISITION_ERROR"
    default_recoverable = True


class LockReleaseError(LockError):
    """
    Unable to release lock.
    """

    default_code = "LOCK_RELEASE_ERROR"


class DeadlockError(LockError):
    """
    Deadlock detected.
    """

    default_code = "DEADLOCK_ERROR"


# ==========================================================
# Synchronization Errors
# ==========================================================


class SynchronizationError(ConcurrencyError):
    """
    Synchronization failures.
    """

    default_code = "SYNCHRONIZATION_ERROR"


class RaceConditionError(SynchronizationError):
    """
    Race condition detected.
    """

    default_code = "RACE_CONDITION_ERROR"


class StateSynchronizationError(SynchronizationError):
    """
    Shared state synchronization failure.
    """

    default_code = "STATE_SYNCHRONIZATION_ERROR"


# ==========================================================
# Queue Concurrency Errors
# ==========================================================


class QueueOverflowError(ConcurrencyError):
    """
    Queue capacity exceeded.
    """

    default_code = "QUEUE_OVERFLOW_ERROR"
    default_recoverable = True


class QueueTimeoutError(ConcurrencyError):
    """
    Queue operation timeout.
    """

    default_code = "QUEUE_TIMEOUT_ERROR"
    default_recoverable = True

# ==========================================================
# Framework Critical Errors
# ==========================================================


class FatalError(StudioOSError):
    """
    Non-recoverable framework failure.
    """

    default_code = "FATAL_ERROR"
    default_category = "framework"
    default_severity = "critical"
    default_recoverable = False


class InternalError(StudioOSError):
    """
    Internal framework failure.
    """

    default_code = "INTERNAL_ERROR"
    default_category = "framework"


class UnknownError(StudioOSError):
    """
    Unknown/unclassified failure.
    """

    default_code = "UNKNOWN_ERROR"
    default_category = "unknown"


# ==========================================================
# Feature Compatibility Errors
# ==========================================================


class FeatureError(StudioOSError):
    """
    Feature subsystem failures.
    """

    default_code = "FEATURE_ERROR"
    default_category = "feature"


class DeprecatedFeatureError(FeatureError):
    """
    Deprecated feature usage.
    """

    default_code = "DEPRECATED_FEATURE"


class NotImplementedFeatureError(FeatureError):
    """
    Feature not implemented yet.
    """

    default_code = "FEATURE_NOT_IMPLEMENTED"


class FeatureDisabledError(FeatureError):
    """
    Disabled feature access.
    """

    default_code = "FEATURE_DISABLED"


# ==========================================================
# Framework Compatibility
# ==========================================================


class CompatibilityError(StudioOSError):
    """
    Compatibility related failures.
    """

    default_code = "COMPATIBILITY_ERROR"
    default_category = "compatibility"


class FrameworkCompatibilityError(CompatibilityError):
    """
    Framework version incompatibility.
    """

    default_code = "FRAMEWORK_COMPATIBILITY_ERROR"


class VersionConflictError(CompatibilityError):
    """
    Version mismatch.
    """

    default_code = "VERSION_CONFLICT_ERROR"


# ==========================================================
# Exception Utilities
# ==========================================================


def wrap_exception(
    exc: Exception,
    *,
    message: str | None = None,
    category: str = "unknown",
) -> StudioOSError:
    """
    Convert native exceptions into StudioOS exceptions.
    """

    if isinstance(exc, StudioOSError):
        return exc

    return InternalError(
        message or str(exc),
        category=category,
        details={
            "original_type": exc.__class__.__name__,
        },
    )


def is_recoverable(exc: Exception) -> bool:
    """
    Check if exception can be recovered.
    """

    if isinstance(exc, StudioOSError):
        return exc.metadata.recoverable

    return False


def serialize_exception(
    exc: Exception,
) -> dict[str, Any]:
    """
    Serialize any exception safely.
    """

    if isinstance(exc, StudioOSError):
        return exc.serialize()

    return {
        "error": exc.__class__.__name__,
        "message": str(exc),
        "recoverable": False,
    }
