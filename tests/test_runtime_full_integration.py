import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.context import RuntimeContext
from runtime.execution_pipeline import runtime_execution_pipeline
from runtime.performance import runtime_performance
from runtime.runtime_metrics import runtime_metrics
from runtime.runtime_events import runtime_event_bus


def sample_handler():

    return {
        "status": "ok",
    }


def test_runtime_full_integration():

    runtime_performance.clear()

    runtime_event_bus.events.clear()

    context = RuntimeContext()

    result = runtime_execution_pipeline.execute(
        context,
        sample_handler,
    )

    assert result.success

    assert result.data["status"] == "ok"

    assert len(runtime_event_bus.events) >= 2

    report = runtime_performance.report()

    assert report["total_records"] >= 1

    assert runtime_metrics.total_executions >= 1

from runtime.provider_executor import runtime_provider_executor


def provider_ok():

    class Result:

        success = True
        provider = "mock-provider"
        data = {
            "message": "ok",
        }

    return Result()


def test_end_to_end_runtime():

    context = RuntimeContext()

    result = runtime_provider_executor.execute(
        context=context,
        providers={
            "mock-provider": provider_ok,
        },
    )

    assert result.success

    assert result.provider == "mock-provider"

    assert result.data.data["message"] == "ok"

def test_cross_component_validation():

    from runtime.context import RuntimeContext
    from runtime.execution_pipeline import (
        runtime_execution_pipeline,
    )
    from runtime.performance import (
        runtime_performance,
    )
    from runtime.runtime_events import (
        runtime_event_bus,
    )
    from runtime.runtime_metrics import (
        runtime_metrics,
    )

    runtime_performance.clear()
    runtime_event_bus.events.clear()

    metrics_before = runtime_metrics.total_executions

    context = RuntimeContext()

    result = runtime_execution_pipeline.execute(
        context,
        lambda: "runtime-ok",
    )

    assert result.success
    assert result.data == "runtime-ok"

    # Events
    assert len(runtime_event_bus.events) >= 2

    # Metrics
    assert (
        runtime_metrics.total_executions
        == metrics_before + 1
    )

    # Performance
    report = runtime_performance.report()

    assert report["total_records"] >= 1

    assert (
        "execution_pipeline"
        in report["records"]
    )
def test_runtime_stress_validation():

    from runtime.context import RuntimeContext
    from runtime.execution_pipeline import (
        runtime_execution_pipeline,
    )

    total_runs = 25

    for index in range(total_runs):

        context = RuntimeContext()

        result = runtime_execution_pipeline.execute(
            context,
            lambda i=index: i,
        )

        assert result.success
        assert result.data == index
def test_runtime_integration_finalization():

    from runtime.performance import (
        runtime_performance,
    )
    from runtime.runtime_metrics import (
        runtime_metrics,
    )
    from runtime.runtime_events import (
        runtime_event_bus,
    )

    report = runtime_performance.report()

    assert report["total_records"] >= 1

    assert runtime_metrics.total_executions > 0

    assert len(runtime_event_bus.events) > 0

if __name__ == "__main__":

    test_runtime_full_integration()

    test_end_to_end_runtime()

    test_cross_component_validation()

    test_runtime_stress_validation()

    test_runtime_integration_finalization()

    print(
        "\n🎉 Runtime Full Integration Validation Passed"
    )