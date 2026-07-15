import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.error_handling import (
    RuntimeErrorType,
    runtime_error_handler,
)


def test_safe_execute_success():

    ok, value, error = (
        runtime_error_handler.safe_execute(
            lambda: 123,
        )
    )

    assert ok

    assert value == 123

    assert error is None


def test_safe_execute_failure():

    def failing():

        raise ValueError(
            "invalid input",
        )

    ok, value, error = (
        runtime_error_handler.safe_execute(
            failing,
        )
    )

    assert not ok

    assert value is None

    assert (
        error.error_type
        == RuntimeErrorType.VALIDATION
    )

    assert error.metadata["handled"]


if __name__ == "__main__":

    test_safe_execute_success()

    test_safe_execute_failure()

    print(
        "\n🎉 Runtime Exception Hardening Validation Passed"
    )