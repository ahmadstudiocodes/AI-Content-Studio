import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.lifecycle import (
    RuntimeLifecycle,
    RuntimeState,
)


def test_valid_lifecycle():

    lifecycle = RuntimeLifecycle()

    lifecycle.initialize()

    assert lifecycle.is_running

    lifecycle.shutdown()

    assert lifecycle.is_stopped


def test_invalid_transition():

    lifecycle = RuntimeLifecycle()

    try:

        lifecycle.shutdown()

        raise AssertionError(
            "Expected RuntimeError"
        )

    except RuntimeError:

        pass


if __name__ == "__main__":

    test_valid_lifecycle()

    test_invalid_transition()

    print(
        "\n🎉 Runtime Consistency Validation Passed"
    )