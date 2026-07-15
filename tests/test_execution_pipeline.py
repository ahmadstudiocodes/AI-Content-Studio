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



def test_success_execution():

    pipeline = RuntimeExecutionPipeline()

    context = RuntimeContext()


    def handler():

        return "OK"


    result = pipeline.execute(
        context,
        handler
    )


    assert result.success is True

    assert result.data == "OK"

    assert result.trace_id == context.trace_id



def test_failed_execution():

    pipeline = RuntimeExecutionPipeline()

    context = RuntimeContext()


    def handler():

        raise ValueError(
            "failed"
        )


    result = pipeline.execute(
        context,
        handler
    )


    assert result.success is False

    assert (
        result.error
        ==
        "failed"
    )



def test_context_binding():

    pipeline = RuntimeExecutionPipeline()

    context = RuntimeContext()


    def handler():

        from runtime.context_manager import (
            runtime_context_manager,
        )

        return (
            runtime_context_manager.current()
        )


    result = pipeline.execute(
        context,
        handler
    )


    assert (
        result.data
        ==
        context
    )



if __name__ == "__main__":

    test_success_execution()

    test_failed_execution()

    test_context_binding()


    print(
        "\n🎉 Runtime Execution Pipeline Validation Passed"
    )
    