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


def test_runtime_stability():

    runtime_event_bus.events.clear()

    start_count = (
        runtime_metrics.total_executions
    )


    for _ in range(100):

        result = (
            runtime_execution_pipeline.execute(
                RuntimeContext(),
                lambda: "ok",
            )
        )

        assert result.success

        assert result.data == "ok"


    executed = (
        runtime_metrics.total_executions
        - start_count
    )


    assert executed == 100

    assert (
        len(runtime_event_bus.events)
        >= 200
    )


if __name__ == "__main__":

    test_runtime_stability()

    print(
        "\n🎉 Runtime Stability Validation Passed"
    )