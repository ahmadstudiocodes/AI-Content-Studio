from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from runtime.context import RuntimeContext

from runtime.execution_pipeline import (
    RuntimeExecutionPipeline,
)

from runtime.failover import (
    RuntimeFailoverManager,
)

from runtime.performance import (
    runtime_performance,
)

from runtime.retry import (
    RuntimeRetryEngine,
    RetryPolicy,
)

from runtime.security import (
    runtime_security_validator,
)


@dataclass(slots=True)
class ProviderExecutionResult:

    success: bool

    provider: Optional[str] = None

    data: Any = None

    error: Optional[str] = None

    trace_id: Optional[str] = None


class RuntimeProviderExecutor:
    """
    Coordinates Runtime execution
    with Provider layer.
    """

    def __init__(self):

        self.pipeline = RuntimeExecutionPipeline()

        self.retry_engine = RuntimeRetryEngine()

        self.failover_manager = RuntimeFailoverManager()

    def execute(
        self,
        context: RuntimeContext,
        providers: Dict[str, Callable],
        retry_policy: RetryPolicy | None = None,
    ) -> ProviderExecutionResult:

        performance_started = runtime_performance.start()

        provider_items = list(
            providers.items()
        )

        validated_provider_items = []

        for provider_name, provider_callable in provider_items:

            validation = (
                runtime_security_validator
                .validate_provider(provider_name)
            )

            if validation.allowed:

                validated_provider_items.append(
                    (
                        provider_name,
                        provider_callable,
                    )
                )

        def run_provider():

            result = (
                self.failover_manager.execute(
                    validated_provider_items
                )
            )

            if not result.success:

                raise RuntimeError(
                    "All providers failed"
                )

            return result

        retry_result = (
            self.retry_engine.execute(
                run_provider,
                retry_policy,
            )
        )

        runtime_performance.stop(
            "provider_executor",
            performance_started,
        )

        if retry_result.success:

            provider_result = (
                retry_result.data
            )

            return ProviderExecutionResult(
                success=True,
                provider=provider_result.provider,
                data=provider_result.data,
                trace_id=context.trace_id,
            )

        return ProviderExecutionResult(
            success=False,
            error=retry_result.error,
            trace_id=context.trace_id,
        )


runtime_provider_executor = (
    RuntimeProviderExecutor()
)