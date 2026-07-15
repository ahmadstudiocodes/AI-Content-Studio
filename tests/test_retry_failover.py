import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.retry import (
    RuntimeRetryEngine,
    RetryPolicy,
)


from runtime.failover import (
    RuntimeFailoverManager,
)



def test_retry_success():


    engine = RuntimeRetryEngine()


    result = engine.execute(
        lambda: "ok"
    )


    assert result.success

    assert result.data == "ok"



def test_retry_failure():


    engine = RuntimeRetryEngine()


    def fail():

        raise Exception(
            "error"
        )


    result = engine.execute(
        fail,
        RetryPolicy(
            max_attempts=2,
            delay_seconds=0
        )
    )


    assert result.success is False

    assert result.attempts == 2



def test_failover():


    manager = RuntimeFailoverManager()


    providers = [

        (
            "primary",
            lambda: (
                (_ for _ in ()).throw(
                    Exception()
                )
            ),
        ),

        (
            "backup",
            lambda: "backup-result",
        ),

    ]


    result = manager.execute(
        providers
    )


    assert result.success

    assert (
        result.provider
        ==
        "backup"
    )



if __name__ == "__main__":


    test_retry_success()

    test_retry_failure()

    test_failover()


    print(
        "\n🎉 Retry Failover Validation Passed"
    )