import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.health import (
    RuntimeHealthManager,
    HealthStatus,
)


from runtime.diagnostics import (
    RuntimeDiagnostics,
)



def test_health_check():


    manager = RuntimeHealthManager()


    manager.register_check(
        "runtime",
        lambda: True
    )


    result = (
        manager.check_health()
    )


    assert len(result) == 1

    assert (
        result[0].status
        ==
        HealthStatus.HEALTHY
    )



def test_diagnostics():


    diagnostics = RuntimeDiagnostics()


    snapshot = diagnostics.snapshot(
        "running",
        {
            "runtime": "ok"
        }
    )


    assert (
        snapshot.state
        ==
        "running"
    )


    assert (
        snapshot.components["runtime"]
        ==
        "ok"
    )



if __name__ == "__main__":

    test_health_check()

    test_diagnostics()


    print(
        "\n🎉 Runtime Health Diagnostics Validation Passed"
    )