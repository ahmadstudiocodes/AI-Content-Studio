import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncio

from providers.openai.client import OpenAIProvider
from providers.openai.config import OpenAIConfig


async def main():

    print("\n=== OpenAI Provider Test ===")

    config = OpenAIConfig()

    provider = OpenAIProvider(
        config
    )

    print(
        "✅ Provider Created:",
        provider.name
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


if __name__ == "__main__":
    asyncio.run(main())