# core/events.py
# Part 96
# Global Configuration Management Layer


from enum import Enum

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
    Dict,
    List,
    Optional,
)

import threading
import uuid

from .middleware import (
    EventMiddleware,
)
# ============================================================
# Configuration Scope
# ============================================================


class EventConfigurationScope(str, Enum):
    """
    Configuration levels.
    """

    GLOBAL = "global"

    CLUSTER = "cluster"

    NODE = "node"

    TENANT = "tenant"

    RUNTIME = "runtime"



# ============================================================
# Configuration Type
# ============================================================


class EventConfigurationType(str, Enum):
    """
    Configuration value types.
    """

    STRING = "string"

    INTEGER = "integer"

    BOOLEAN = "boolean"

    JSON = "json"

    SECRET = "secret"



# ============================================================
# Configuration Entry
# ============================================================


@dataclass(slots=True)
class EventConfigurationEntry:
    """
    Single configuration item.
    """

    key: str

    value: Any

    value_type:      EventConfigurationType

    scope:      EventConfigurationScope

    description: str = ""

    updated_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Configuration Snapshot
# ============================================================


@dataclass(slots=True)
class EventConfigurationSnapshot:
    """
    Versioned configuration state.
    """

    snapshot_id: str

    version: int

    entries: list[
        EventConfigurationEntry
    ]

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Configuration Registry
# ============================================================


class EventConfigurationRegistry:
    """
    Stores enterprise configuration.
    """

    def __init__(
        self,
    ) -> None:

        self.entries: Dict[
            str,
            EventConfigurationEntry
        ] = {}

        self.history: list[
            EventConfigurationSnapshot
        ] = []

        self.version = 0



    def set(
        self,
        entry:
            EventConfigurationEntry,
    ) -> None:

        self.entries[
            entry.key
        ] = entry



    def get(
        self,
        key:
            str,
        default:
            Any = None,
    ) -> Any:

        entry = (
            self.entries.get(
                key
            )
        )


        if not entry:

            return default


        return entry.value



    def snapshot(
        self,
    ) -> EventConfigurationSnapshot:

        self.version += 1


        snapshot = (
            EventConfigurationSnapshot(
                snapshot_id=
                    uuid.uuid4().hex,

                version=
                    self.version,

                entries=
                    list(
                        self.entries.values()
                    ),
            )
        )


        self.history.append(
            snapshot
        )


        return snapshot



# ============================================================
# Configuration Validator
# ============================================================


class EventConfigurationValidator:
    """
    Validates configuration safety.
    """

    def validate(
        self,
        registry:
            EventConfigurationRegistry,
    ) -> Dict[str, Any]:

        checks = {

            "security":
                registry.get(
                    "security.enabled",
                    False,
                ),

            "monitoring":
                registry.get(
                    "monitoring.enabled",
                    False,
                ),

            "queue":
                registry.get(
                    "queue.size",
                    0,
                )
                >
                0,

        }


        return {

            "valid":
                all(
                    checks.values()
                ),

            "checks":
                checks,

        }



# ============================================================
# Dynamic Configuration Loader
# ============================================================


class EventDynamicConfigurationLoader:
    """
    Runtime configuration loader.

    Supports:
    - Hot reload
    - Environment update
    """

    def __init__(
        self,
        registry:
            EventConfigurationRegistry,
    ) -> None:

        self.registry = registry



    def reload(
        self,
        values:
            Dict[str, Any],
    ) -> None:

        for key, value in (
            values.items()
        ):

            self.registry.set(
                EventConfigurationEntry(
                    key=
                        key,

                    value=
                        value,

                    value_type=
                        EventConfigurationType.JSON,

                    scope=
                        EventConfigurationScope.RUNTIME,
                )
            )



# ============================================================
# Configuration Manager
# ============================================================


class EventGlobalConfigurationManager:
    """
    Enterprise configuration controller.

    Features:
    - Central configuration
    - Versioning
    - Validation
    - Dynamic reload
    """

    def __init__(
        self,
    ) -> None:

        self.registry = (
            EventConfigurationRegistry()
        )

        self.validator = (
            EventConfigurationValidator()
        )

        self.loader = (
            EventDynamicConfigurationLoader(
                self.registry
            )
        )



    def initialize_defaults(
        self,
    ) -> None:


        defaults = {

            "security.enabled":
                True,

            "monitoring.enabled":
                True,

            "backup.enabled":
                True,

            "queue.size":
                50000,

            "workers":
                16,

            "replication.enabled":
                True,

        }


        for key, value in (
            defaults.items()
        ):

            self.registry.set(
                EventConfigurationEntry(
                    key=
                        key,

                    value=
                        value,

                    value_type=
                        EventConfigurationType.JSON,

                    scope=
                        EventConfigurationScope.GLOBAL,
                )
            )



    def validate(
        self,
    ) -> Dict[str, Any]:

        return (
            self.validator.validate(
                self.registry
            )
        )



# ============================================================
# Configuration Middleware
# ============================================================


class EventConfigurationMiddleware(
    EventMiddleware
):
    """
    Global configuration middleware.
    """

    def __init__(
        self,
        manager:
            EventGlobalConfigurationManager,
    ) -> None:

        super().__init__(
            "configuration_manager"
        )

        self.manager = manager



# ============================================================
# Global Configuration Objects
# ============================================================


event_global_configuration_manager = (
    EventGlobalConfigurationManager()
)


event_global_configuration_manager.initialize_defaults()


event_configuration_middleware = (
    EventConfigurationMiddleware(
        event_global_configuration_manager
    )
)