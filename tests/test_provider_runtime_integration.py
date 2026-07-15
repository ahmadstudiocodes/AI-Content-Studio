import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.bootstrap import (
    ProviderBootstrap,
)

from providers.runtime import (
    ProviderRuntime,
)

from providers.manager import (
    ProviderManager,
)



async def main():

    print(
        "\n=== Provider Runtime Integration Test ==="
    )


    # Initialize providers

    bootstrap = ProviderBootstrap()


    initialized = bootstrap.initialize()


    print(
        "Initialized:",
        initialized,
    )


    assert initialized



    manager = ProviderManager()


    runtime = ProviderRuntime(
        manager
    )


    health = await runtime.health()


    print(
        "Health:",
        health,
    )


    assert isinstance(
        health,
        dict,
    )


    status = (
        bootstrap.status()
    )


    print(
        "Bootstrap Status:",
        status,
    )


    assert (
        status["initialized"]
        is True
    )


    print(
        "\n🎉 Provider Runtime Integration Validation Passed"
    )



if __name__ == "__main__":

    asyncio.run(main())