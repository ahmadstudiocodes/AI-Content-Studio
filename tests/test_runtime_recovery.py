import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.error_handling import (
    runtime_error_handler,
    RuntimeErrorType,
)


from runtime.recovery import (
    RuntimeRecoveryManager,
)



def test_error_classification():


    error = ValueError(
        "invalid data"
    )


    result = (
        runtime_error_handler
        .classify(error)
    )


    assert (
        result.error_type
        ==
        RuntimeErrorType.VALIDATION
    )


    assert result.recoverable is False



def test_recovery_success():


    manager = RuntimeRecoveryManager()


    result = manager.recover(
        lambda: "ok"
    )


    assert result.recovered

    assert result.data == "ok"



def test_recovery_failure():


    manager = RuntimeRecoveryManager()


    def fail():

        raise Exception(
            "failed"
        )


    result = manager.recover(
        fail,
        retries=2
    )


    assert result.recovered is False

    assert result.attempts == 3



if __name__ == "__main__":


    test_error_classification()

    test_recovery_success()

    test_recovery_failure()


    print(
        "\n🎉 Runtime Recovery Validation Passed"
    )