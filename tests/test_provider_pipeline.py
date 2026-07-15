import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.manager import ProviderManager
from providers.runtime import ProviderRuntime
from providers.pipeline import ProviderPipeline



async def main():

    print(
        "\n=== Provider Pipeline Test ==="
    )


    manager = ProviderManager()


    runtime = ProviderRuntime(
        manager
    )


    pipeline = ProviderPipeline(
        runtime
    )


    assert pipeline.validate(
        "test request"
    )


    assert not pipeline.validate(
        None
    )


    health = await pipeline.health()


    print(
        "Health:",
        health,
    )


    print(
        "\n🎉 Provider Pipeline Validation Passed"
    )



if __name__ == "__main__":
    asyncio.run(main())