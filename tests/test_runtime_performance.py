import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.performance import (
    RuntimePerformance,
)


def test_timer():

    performance = RuntimePerformance()

    started = performance.start()

    time.sleep(0.01)

    duration = performance.stop(
        "pipeline",
        started,
    )

    assert duration > 0

    assert (
        performance.get_duration(
            "pipeline"
        ) > 0
    )


def test_report():

    performance = RuntimePerformance()

    started = performance.start()

    time.sleep(0.005)

    performance.stop(
        "provider_executor",
        started,
    )

    report = performance.report()

    assert report["total_records"] == 1

    assert "provider_executor" in report["records"]

    assert (
        report["records"]["provider_executor"]
        > 0
    )

def test_runtime_performance_integration():

    from runtime.performance import (
        runtime_performance,
    )

    runtime_performance.clear()

    started = runtime_performance.start()

    time.sleep(0.002)

    runtime_performance.stop(
        "integration",
        started,
    )

    report = runtime_performance.report()

    assert report["total_records"] == 1

    assert "integration" in report["records"]

    assert report["records"]["integration"] > 0

if __name__ == "__main__":

    test_timer()

    test_report()

    test_runtime_performance_integration()

    print(
        "\n🎉 Runtime Performance Validation Passed"
    )