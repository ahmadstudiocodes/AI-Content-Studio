import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncio

from providers.ollama.client import OllamaProvider
from providers.types import ProviderRequest
from providers.ollama.config import OllamaConfig


async def main():

    config = OllamaConfig()

    provider = OllamaProvider(
        config=config
    )

    request = ProviderRequest(
        prompt="Say hello to Arman StudioOS",
        model="qwen3:4b",
    )

    result = await provider.generate(
        request
    )

    print("\n===== RESPONSE =====")
    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())