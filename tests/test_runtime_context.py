import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from runtime.context import (
    RuntimeContext,
    create_runtime_context,
)


def test_runtime_context_creation():

    ctx = RuntimeContext()

    assert ctx.request.request_id
    assert ctx.trace_id

    print(
        "Trace:",
        ctx.trace_id
    )


def test_context_metadata():

    ctx = RuntimeContext()

    ctx.add_metadata(
        "environment",
        "test"
    )

    assert (
        ctx.request.metadata["environment"]
        ==
        "test"
    )


def test_context_propagation():

    ctx = create_runtime_context(
        session_id="session-1",
        workspace_id="workspace-1",
        provider_id="provider-openai",
    )

    payload = ctx.propagate()

    assert payload["session_id"] == "session-1"
    assert payload["workspace_id"] == "workspace-1"
    assert payload["provider_id"] == "provider-openai"
    assert payload["trace_id"]


if __name__ == "__main__":

    test_runtime_context_creation()
    test_runtime_context_metadata if False else None
    test_context_metadata()
    test_context_propagation()

    print(
        "\n🎉 Runtime Context Validation Passed"
    )