import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from runtime.context import RuntimeContext

from runtime.execution_pipeline import (
    RuntimeExecutionPipeline,
)

from runtime.context_manager import (
    RuntimeContextManager,
)

from runtime.lifecycle import (
    RuntimeLifecycle,
)

from runtime.runtime_metrics import (
    RuntimeMetrics,
)

from runtime.runtime_events import (
    RuntimeEventBus,
)


def test_runtime_freeze():

    # Core Runtime API existence

    assert RuntimeContext is not None

    assert RuntimeExecutionPipeline is not None

    assert RuntimeContextManager is not None

    assert RuntimeLifecycle is not None

    assert RuntimeMetrics is not None

    assert RuntimeEventBus is not None


    # Instantiate core components

    context = RuntimeContext()

    pipeline = RuntimeExecutionPipeline()

    manager = RuntimeContextManager()

    lifecycle = RuntimeLifecycle()


    assert context is not None

    assert pipeline is not None

    assert manager is not None

    assert lifecycle is not None


    # Basic execution contract

    result = pipeline.execute(
        context,
        lambda: "freeze_ok",
    )

    assert result.success

    assert (
        result.data
        == "freeze_ok"
    )


if __name__ == "__main__":

    test_runtime_freeze()

    print(
        "\n🎉 Runtime Freeze Validation Passed"
    )