import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio

from providers.claude.client import ClaudeProvider
from providers.claude.config import ClaudeConfig


async def main():

    print("\n=== Claude Provider Test ===")


    config = ClaudeConfig()


    provider = ClaudeProvider(
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
        "\n🎉 Claude Provider Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())