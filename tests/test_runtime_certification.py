import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from runtime.context import RuntimeContext
from runtime.execution_pipeline import (
    runtime_execution_pipeline,
)

from runtime.lifecycle import (
    RuntimeLifecycle,
)

from runtime.runtime_metrics import (
    runtime_metrics,
)

from runtime.runtime_events import (
    runtime_event_bus,
)

from runtime.diagnostics import (
    runtime_diagnostics,
)


def test_runtime_certification():

    lifecycle = RuntimeLifecycle()

    lifecycle.initialize()

    start_execution = (
        runtime_metrics.total_executions
    )

    result = (
        runtime_execution_pipeline.execute(
            RuntimeContext(),
            lambda: {
                "certified": True,
            },
        )
    )


    assert result.success

    assert (
        result.data["certified"]
        is True
    )


    assert (
        runtime_metrics.total_executions
        == start_execution + 1
    )


    snapshot = (
        runtime_diagnostics.snapshot(
            state=lifecycle.state.value,
            components={
                "metrics": runtime_metrics,
                "events": runtime_event_bus,
            },
        )
    )


    report = (
        runtime_diagnostics.validate(
            snapshot
        )
    )


    assert report["healthy"]


    lifecycle.shutdown()


    assert lifecycle.is_stopped



if __name__ == "__main__":

    test_runtime_certification()

    print(
        "\n🎉 Runtime Certification Passed"
    )