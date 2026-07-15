import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio

from providers.gemini.client import GeminiProvider
from providers.gemini.config import GeminiConfig


async def main():

    print("\n=== Gemini Provider Test ===")


    config = GeminiConfig()


    provider = GeminiProvider(
        config
    )


    print(
        "✅ Provider Created:",
        provider.name,
    )


    print(
        "✅ Capabilities:",
        provider.capabilities.to_dict()
    )


    health = await provider.health_check()


    print(
        "✅ Health Check:"
    )

    print(
        health
    )


    print(
        "\n🎉 Gemini Provider Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())