# core/events.py
# Part 92
# EventBus Multi-Tenant Architecture and Isolation Layer


from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, Optional

import json
import threading
import uuid

from .core import BaseEvent
from .middleware import (
    EventMiddleware,
)

# ============================================================
# Tenant State
# ============================================================


class EventTenantState(str, Enum):
    """
    Tenant lifecycle.
    """

    CREATED = "created"

    ACTIVE = "active"

    SUSPENDED = "suspended"

    DISABLED = "disabled"



# ============================================================
# Tenant Isolation Level
# ============================================================


class EventIsolationLevel(str, Enum):
    """
    Tenant separation modes.
    """

    SHARED = "shared"

    LOGICAL = "logical"

    STRICT = "strict"



# ============================================================
# Tenant Configuration
# ============================================================


@dataclass(slots=True)
class EventTenantConfiguration:
    """
    Tenant runtime settings.
    """

    tenant_id: str

    name: str

    isolation:      EventIsolationLevel

    max_events_per_second: int = 1000

    storage_namespace: str = ""

    encryption_enabled: bool = True



# ============================================================
# Tenant Record
# ============================================================


@dataclass(slots=True)
class EventTenant:
    """
    Multi tenant identity.
    """

    tenant_id: str

    configuration:      EventTenantConfiguration

    state:      EventTenantState = (
            EventTenantState.CREATED
        )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(UTC)
    )



# ============================================================
# Tenant Registry
# ============================================================


class EventTenantRegistry:
    """
    Stores isolated tenants.
    """

    def __init__(
        self,
    ) -> None:

        self.tenants: Dict[
            str,
            EventTenant
        ] = {}

        self.lock = threading.RLock()



    def register(
        self,
        tenant:
            EventTenant,
    ) -> None:

        with self.lock:

            self.tenants[
                tenant.tenant_id
            ] = tenant



    def get(
        self,
        tenant_id:
            str,
    ) -> Optional[
        EventTenant
    ]:

        return self.tenants.get(
            tenant_id
        )



    def activate(
        self,
        tenant_id:
            str,
    ) -> bool:

        tenant = (
            self.get(
                tenant_id
            )
        )


        if not tenant:

            return False


        tenant.state = (
            EventTenantState.ACTIVE
        )


        return True



# ============================================================
# Tenant Context
# ============================================================


@dataclass(slots=True)
class EventTenantContext:
    """
    Execution isolation context.
    """

    tenant_id: str

    permissions: list[str] = field(
        default_factory=list
    )

    metadata: Dict[
        str,
        Any
    ] = field(
        default_factory=dict
    )



# ============================================================
# Tenant Resolver
# ============================================================


class EventTenantResolver:
    """
    Resolves event ownership.
    """

    def resolve(
        self,
        event:
            BaseEvent,
    ) -> Optional[str]:

        if hasattr(
            event,
            "tenant_id",
        ):

            return event.tenant_id


        return None



# ============================================================
# Tenant Event Router
# ============================================================


class EventTenantRouter:
    """
    Routes events inside tenants.
    """

    def __init__(
        self,
        registry:
            EventTenantRegistry,
    ) -> None:

        self.registry = registry



    def route(
        self,
        tenant_id:
            str,
        event:
            BaseEvent,
    ) -> bool:

        tenant = (
            self.registry.get(
                tenant_id
            )
        )


        if not tenant:

            return False


        if (
            tenant.state
            !=
            EventTenantState.ACTIVE
        ):

            return False


        return True



# ============================================================
# Resource Quota Manager
# ============================================================


class EventTenantQuotaManager:
    """
    Controls tenant resource limits.
    """

    def __init__(
        self,
    ) -> None:

        self.usage: Dict[
            str,
            int
        ] = {}



    def consume(
        self,
        tenant_id:
            str,
        amount:
            int = 1,
    ) -> int:

        current = (
            self.usage.get(
                tenant_id,
                0
            )
        )


        current += amount


        self.usage[
            tenant_id
        ] = current


        return current



    def reset(
        self,
        tenant_id:
            str,
    ) -> None:

        self.usage[
            tenant_id
        ] = 0



# ============================================================
# Multi Tenant Controller
# ============================================================


class EventMultiTenantController:
    """
    Complete tenant isolation engine.

    Features:
    - Tenant management
    - Routing
    - Quotas
    - Isolation
    """

    def __init__(
        self,
    ) -> None:

        self.registry = (
            EventTenantRegistry()
        )

        self.resolver = (
            EventTenantResolver()
        )

        self.router = (
            EventTenantRouter(
                self.registry
            )
        )

        self.quota = (
            EventTenantQuotaManager()
        )



    def create_tenant(
        self,
        configuration:
            EventTenantConfiguration,
    ) -> EventTenant:

        tenant = EventTenant(
            tenant_id=
                configuration.tenant_id,

            configuration=
                configuration,
        )


        self.registry.register(
            tenant
        )


        return tenant



# ============================================================
# Multi Tenant Middleware
# ============================================================


class EventMultiTenantMiddleware(
    EventMiddleware
):
    """
    Tenant isolation middleware.
    """

    def __init__(
        self,
        controller:
            EventMultiTenantController,
    ) -> None:

        super().__init__(
            "multi_tenant_isolation"
        )

        self.controller = controller



# ============================================================
# Global Multi Tenant Objects
# ============================================================


event_multi_tenant_controller = (
    EventMultiTenantController()
)


event_multi_tenant_middleware = (
    EventMultiTenantMiddleware(
        event_multi_tenant_controller
    )
)