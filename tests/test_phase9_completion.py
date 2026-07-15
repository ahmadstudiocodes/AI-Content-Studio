import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )


from runtime.diagnostics import (
    runtime_diagnostics,
)


def test_phase9_completion_certificate():

    certificate = {

        "phase": "PHASE_9",

        "name": "CORE_RUNTIME_ENGINE",

        "version": "1.0.0",

        "runtime_status": "COMPLETE",

        "freeze": True,

        "package_validation": True,

        "release_snapshot": True,

        "certified": True,
    }


    snapshot = (
        runtime_diagnostics.snapshot(
            state="completed",
            components=certificate,
        )
    )


    report = (
        runtime_diagnostics.validate(
            snapshot
        )
    )


    assert report["healthy"]

    assert (
        snapshot.components["runtime_status"]
        == "COMPLETE"
    )

    assert (
        snapshot.components["certified"]
        is True
    )

    assert (
        snapshot.components["freeze"]
        is True
    )



if __name__ == "__main__":

    test_phase9_completion_certificate()

    print(
        "\n🎉 Phase 9 Completion Certificate Passed"
    )