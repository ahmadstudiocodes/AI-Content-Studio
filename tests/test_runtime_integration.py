import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.context import RuntimeContext

from runtime.execution_pipeline import (
    RuntimeExecutionPipeline,
)

from runtime.runtime_events import (
    runtime_event_bus,
)

from runtime.runtime_metrics import (
    runtime_metrics,
)



def test_runtime_observability():

    pipeline = RuntimeExecutionPipeline()

    context = RuntimeContext()


    def handler():

        return "success"


    result = pipeline.execute(
        context,
        handler
    )


    assert result.success


    assert (
        runtime_metrics.successful_executions
        >= 1
    )


    events = (
        runtime_event_bus.all_events()
    )


    assert len(events) >= 2


    assert (
        events[-1].trace_id
        ==
        context.trace_id
    )



if __name__ == "__main__":

    test_runtime_observability()

    print(
        "\n🎉 Runtime Event Metrics Integration Validation Passed"
    )