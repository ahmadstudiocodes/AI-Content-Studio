import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.diagnostics import (
    runtime_diagnostics,
)


def test_runtime_hardening():

    snapshot = (
        runtime_diagnostics.snapshot(
            state="running",
            components={
                "context": object(),
                "metrics": object(),
                "events": object(),
            },
        )
    )

    report = (
        runtime_diagnostics.validate(
            snapshot,
        )
    )

    assert report["healthy"]

    assert (
        report["component_count"]
        == 3
    )

    assert (
        len(report["issues"])
        == 0
    )


def test_runtime_hardening_failure():

    snapshot = (
        runtime_diagnostics.snapshot(
            state="",
            components={
                "context": None,
            },
        )
    )

    report = (
        runtime_diagnostics.validate(
            snapshot,
        )
    )

    assert not report["healthy"]

    assert len(
        report["issues"]
    ) >= 2


if __name__ == "__main__":

    test_runtime_hardening()

    test_runtime_hardening_failure()

    print(
        "\n🎉 Runtime Hardening Validation Passed"
    )