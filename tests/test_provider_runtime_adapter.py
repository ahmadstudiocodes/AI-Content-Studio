import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.manager import (
    ProviderManager,
)

from providers.runtime import (
    ProviderRuntime,
)



async def main():

    print(
        "\n=== Provider Runtime Adapter Test ==="
    )


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


    print(
        "\n🎉 Provider Runtime Adapter Validation Passed"
    )



if __name__ == "__main__":
    asyncio.run(main())