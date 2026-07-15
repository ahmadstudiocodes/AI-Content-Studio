import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from runtime.lifecycle import (
    runtime_lifecycle,
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


def test_runtime_validation_report():

    snapshot = (
        runtime_diagnostics.snapshot(
            state=runtime_lifecycle.state.value,
            components={
                "metrics": runtime_metrics,
                "events": runtime_event_bus,
                "lifecycle": runtime_lifecycle,
            },
        )
    )

    report = (
        runtime_diagnostics.validate(
            snapshot
        )
    )

    assert report["healthy"]

    assert (
        report["component_count"]
        == 3
    )

    assert (
        runtime_metrics.total_executions
        >= 0
    )

    assert (
        len(runtime_event_bus.events)
        >= 0
    )


if __name__ == "__main__":

    test_runtime_validation_report()

    print(
        "\n🎉 Runtime Validation Report Passed"
    )