import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.lifecycle import (
    RuntimeLifecycle,
    RuntimeState,
)



def test_startup():

    lifecycle = RuntimeLifecycle()

    executed = []


    lifecycle.register_startup(
        lambda:
            executed.append(True)
    )


    lifecycle.initialize()


    assert (
        lifecycle.state
        ==
        RuntimeState.RUNNING
    )


    assert executed



def test_shutdown():

    lifecycle = RuntimeLifecycle()


    lifecycle.initialize()


    lifecycle.shutdown()


    assert (
        lifecycle.state
        ==
        RuntimeState.STOPPED
    )



def test_shutdown_hook():

    lifecycle = RuntimeLifecycle()

    cleaned = []


    lifecycle.register_shutdown(
        lambda:
            cleaned.append(True)
    )


    lifecycle.initialize()

    lifecycle.shutdown()


    assert cleaned



if __name__ == "__main__":

    test_startup()

    test_shutdown()

    test_shutdown_hook()


    print(
        "\n🎉 Runtime Lifecycle Validation Passed"
    )