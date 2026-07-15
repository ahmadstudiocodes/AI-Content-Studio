import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.context import (
    RuntimeContext,
)

from runtime.provider_executor import (
    RuntimeProviderExecutor,
)



def test_provider_execution():


    executor = RuntimeProviderExecutor()

    context = RuntimeContext()


    providers = {

        "primary":
            lambda: (
                (_ for _ in ()).throw(
                    Exception("failed")
                )
            ),


        "backup":
            lambda: "provider-result",

    }


    result = executor.execute(
        context,
        providers
    )


    assert result.success is True

    assert (
        result.provider
        ==
        "backup"
    )

    assert (
        result.data
        ==
        "provider-result"
    )

    assert (
        result.trace_id
        ==
        context.trace_id
    )



if __name__ == "__main__":

    test_provider_execution()


    print(
        "\n🎉 Provider Executor Validation Passed"
    )