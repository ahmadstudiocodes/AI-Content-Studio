import sys
from pathlib import Path
from datetime import datetime, UTC


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )


from runtime.diagnostics import (
    runtime_diagnostics,
)


def test_runtime_release_snapshot():

    snapshot = {
        "phase": "PHASE_9",
        "component": "RUNTIME_ENGINE",
        "version": "1.0.0",
        "status": "READY",
        "certified": True,
        "timestamp": datetime.now(
            UTC
        ).isoformat(),
    }


    report = (
        runtime_diagnostics.snapshot(
            state="released",
            components=snapshot,
        )
    )


    validation = (
        runtime_diagnostics.validate(
            report
        )
    )


    assert validation["healthy"]

    assert (
        report.components["version"]
        == "1.0.0"
    )

    assert (
        report.components["certified"]
        is True
    )

    assert (
        report.components["status"]
        == "READY"
    )


if __name__ == "__main__":

    test_runtime_release_snapshot()

    print(
        "\n🎉 Runtime Release Snapshot Validation Passed"
    )