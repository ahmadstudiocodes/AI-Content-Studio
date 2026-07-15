from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Callable

from runtime.security import (
    runtime_security_validator,
)

from runtime.context import (
    create_runtime_context,
    RuntimeContext,
)

from runtime.provider_executor import (
    RuntimeProviderExecutor,
)


@dataclass
class GatewayResponse:

    success: bool

    data: Any = None

    error: str | None = None

    trace_id: str | None = None



class RuntimeAPIGateway:
    """
    Public entry point for Runtime Engine.

    Responsibilities:
    - Validate request
    - Create context
    - Dispatch execution
    - Normalize response
    """


    def __init__(self):

        self.executor = (
            RuntimeProviderExecutor()
        )


    def handle(
        self,
        request: Dict[str, Any],
        providers: Dict[str, Callable],
    ) -> GatewayResponse:

        security = runtime_security_validator.validate_request(
           request
        )

        if not security.allowed:

           return GatewayResponse(
              success=False,
              error=security.reason,
        )

        if not isinstance(
            request,
            dict
        ):

            return GatewayResponse(
                success=False,
                error="Invalid request",
            )


        context = create_runtime_context(
            session_id=
                request.get(
                    "session_id"
                ),

            workspace_id=
                request.get(
                    "workspace_id"
                ),
        )


        result = self.executor.execute(
            context,
            providers,
        )


        if result.success:

            return GatewayResponse(
                success=True,
                data=result.data,
                trace_id=result.trace_id,
            )


        return GatewayResponse(
            success=False,
            error=result.error,
            trace_id=result.trace_id,
        )



runtime_api_gateway = RuntimeAPIGateway()