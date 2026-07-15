import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from runtime.context import RuntimeContext
from runtime.context_manager import RuntimeContextManager


def test_push_context():

    manager = RuntimeContextManager()

    ctx = RuntimeContext()

    manager.push(ctx)

    assert manager.current() == ctx



def test_pop_context():

    manager = RuntimeContextManager()

    ctx = RuntimeContext()

    manager.push(ctx)

    result = manager.pop()

    assert result == ctx

    assert manager.current() is None



def test_nested_context():

    manager = RuntimeContextManager()

    ctx1 = RuntimeContext()
    ctx2 = RuntimeContext()


    with manager.scope(ctx1):

        assert manager.current() == ctx1


        with manager.scope(ctx2):

            assert manager.current() == ctx2


        assert manager.current() == ctx1


    assert manager.current() is None



if __name__ == "__main__":

    test_push_context()

    test_pop_context()

    test_nested_context()

    print(
        "\n🎉 Runtime Context Manager Validation Passed"
    )