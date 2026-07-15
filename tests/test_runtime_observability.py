import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.observability import (
    RuntimeObservability,
)


def test_dashboard():

    dashboard = RuntimeObservability()

    dashboard.record_request()

    dashboard.record_event()

    dashboard.record_metric()

    dashboard.record_error()

    snapshot = dashboard.snapshot()

    assert snapshot["requests"] == 1
    assert snapshot["events"] == 1
    assert snapshot["metrics"] == 1
    assert snapshot["errors"] == 1

def test_runtime_integration():

    from runtime.observability import (
        runtime_observability,
    )

    from runtime.runtime_events import (
        RuntimeEvent,
        runtime_event_bus,
    )

    from runtime.runtime_metrics import (
        runtime_metrics,
    )

    # Reset dashboard counters
    runtime_observability.events = 0
    runtime_observability.metrics = 0

    runtime_event_bus.emit(
        RuntimeEvent(
            name="integration",
            trace_id="test-trace",
        )
    )

    runtime_metrics.record_success(0.25)

    snapshot = runtime_observability.snapshot()

    assert snapshot["events"] == 1
    assert snapshot["metrics"] == 1

if __name__ == "__main__":

    test_dashboard()
    test_runtime_integration()

    print(
        "\n🎉 Runtime Observability Validation Passed"
    )