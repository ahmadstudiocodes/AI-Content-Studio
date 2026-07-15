from __future__ import annotations

import time

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from runtime.context import RuntimeContext
from runtime.context_manager import (
    runtime_context_manager,
)

from runtime.performance import (
    runtime_performance,
)

from runtime.runtime_events import (
    RuntimeEvent,
    runtime_event_bus,
)

from runtime.runtime_metrics import (
    runtime_metrics,
)


@dataclass(slots=True)
class ExecutionResult:
    """
    Runtime execution result container.
    """

    success: bool

    data: Any = None

    error: Optional[str] = None

    execution_time: float = 0.0

    trace_id: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


class RuntimeExecutionPipeline:
    """
    Core runtime execution pipeline.

    Handles:
    - Context binding
    - Execution lifecycle
    - Result wrapping
    - Error capture
    - Events
    - Metrics
    - Performance
    """

    def __init__(self):

        self.executions = 0

    def execute(
        self,
        context: RuntimeContext,
        handler: Callable[..., Any],
        *args,
        **kwargs,
    ) -> ExecutionResult:

        start = time.time()

        # High precision performance timer
        performance_started = runtime_performance.start()

        self.executions += 1

        with runtime_context_manager.scope(
            context
        ):

            runtime_event_bus.emit(
                RuntimeEvent(
                    name="execution_started",
                    trace_id=context.trace_id,
                    payload=context.propagate(),
                )
            )

            try:

                result = handler(
                    *args,
                    **kwargs
                )

                duration = (
                    time.time() - start
                )

                runtime_metrics.record_success(
                    duration
                )

                runtime_event_bus.emit(
                    RuntimeEvent(
                        name="execution_completed",
                        trace_id=context.trace_id,
                        payload={
                            "duration": duration,
                        },
                    )
                )

                runtime_performance.stop(
                    "execution_pipeline",
                    performance_started,
                )

                return ExecutionResult(
                    success=True,
                    data=result,
                    execution_time=duration,
                    trace_id=context.trace_id,
                    metadata=context.propagate(),
                )

            except Exception as exc:

                duration = (
                    time.time() - start
                )

                runtime_metrics.record_failure(
                    duration
                )

                runtime_event_bus.emit(
                    RuntimeEvent(
                        name="execution_failed",
                        trace_id=context.trace_id,
                        payload={
                            "error": str(exc),
                            "duration": duration,
                        },
                    )
                )

                runtime_performance.stop(
                    "execution_pipeline",
                    performance_started,
                )

                return ExecutionResult(
                    success=False,
                    error=str(exc),
                    execution_time=duration,
                    trace_id=context.trace_id,
                    metadata=context.propagate(),
                )


runtime_execution_pipeline = (
    RuntimeExecutionPipeline()
)