from __future__ import annotations

import uuid
import time

from dataclasses import dataclass, field, asdict
from datetime import UTC, datetime
from typing import Any, Dict, Optional


@dataclass
class RequestContext:
    request_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    trace_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    timestamp: float = field(
        default_factory=time.time
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SessionContext:
    session_id: Optional[str] = None

    user_id: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class WorkspaceContext:
    workspace_id: Optional[str] = None

    path: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProviderContext:
    provider_id: Optional[str] = None

    provider_name: Optional[str] = None

    version: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class RuntimeContext:
    """
    Central runtime context container.

    Shared across:
    - Requests
    - Providers
    - Events
    - Metrics
    """

    request: RequestContext = field(
        default_factory=RequestContext
    )

    session: SessionContext = field(
        default_factory=SessionContext
    )

    workspace: WorkspaceContext = field(
        default_factory=WorkspaceContext
    )

    provider: ProviderContext = field(
        default_factory=ProviderContext
    )


    def add_metadata(
        self,
        key: str,
        value: Any
    ) -> None:

        self.request.metadata[key] = value


    @property
    def trace_id(self) -> str:
        return self.request.trace_id


    def propagate(self) -> Dict[str, Any]:
        """
        Context payload for:
        - Events
        - Metrics
        - Logging
        """

        return {
            "trace_id": self.trace_id,
            "request_id": self.request.request_id,
            "timestamp": self.request.timestamp,

            "session_id":
                self.session.session_id,

            "workspace_id":
                self.workspace.workspace_id,

            "provider_id":
                self.provider.provider_id,

            "metadata":
                self.request.metadata,
        }


    def to_dict(self) -> Dict[str, Any]:

        return {
            "request":
                self.request.to_dict(),

            "session":
                asdict(self.session),

            "workspace":
                asdict(self.workspace),

            "provider":
                asdict(self.provider),
        }


def create_runtime_context(
    *,
    session_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    provider_id: Optional[str] = None,
) -> RuntimeContext:

    context = RuntimeContext()

    context.session.session_id = session_id

    context.workspace.workspace_id = workspace_id

    context.provider.provider_id = provider_id

    return context