import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.context import RuntimeContext
from runtime.execution_pipeline import (
    runtime_execution_pipeline,
)
from runtime.runtime_metrics import (
    runtime_metrics,
)
from runtime.runtime_events import (
    runtime_event_bus,
)
from runtime.lifecycle import (
    RuntimeLifecycle,
)


def test_runtime_smoke():

    runtime_event_bus.events.clear()

    before = (
        runtime_metrics.total_executions
    )

    lifecycle = RuntimeLifecycle()

    lifecycle.initialize()

    context = RuntimeContext()

    result = (
        runtime_execution_pipeline.execute(
            context,
            lambda: {
                "status": "ok",
            },
        )
    )

    assert result.success

    assert (
        result.data["status"]
        == "ok"
    )

    lifecycle.shutdown()

    assert (
        runtime_metrics.total_executions
        == before + 1
    )

    assert (
        len(runtime_event_bus.events)
        >= 2
    )

    assert lifecycle.is_stopped


if __name__ == "__main__":

    test_runtime_smoke()

    print(
        "\n🎉 Runtime Smoke Validation Passed"
    )