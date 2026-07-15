import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.context import RuntimeContext
from runtime.context_manager import (
    runtime_context_manager,
)


def test_cleanup():

    runtime_context_manager.clear()

    runtime_context_manager.push(
        RuntimeContext(),
    )

    assert (
        runtime_context_manager.depth
        == 1
    )

    runtime_context_manager.cleanup()

    assert (
        runtime_context_manager.depth
        == 0
    )

    assert (
        runtime_context_manager.current()
        is None
    )


def test_scope_cleanup():

    with runtime_context_manager.scope(
        RuntimeContext(),
    ):

        assert (
            runtime_context_manager.depth
            == 1
        )

    assert (
        runtime_context_manager.depth
        == 0
    )

    assert (
        runtime_context_manager.current()
        is None
    )


if __name__ == "__main__":

    test_cleanup()

    test_scope_cleanup()

    print(
        "\n🎉 Runtime Cleanup Validation Passed"
    )