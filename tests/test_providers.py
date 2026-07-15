import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncio

from providers.ollama.client import OllamaProvider


async def main():

    provider = OllamaProvider()

    result = await provider.generate(
        prompt="Say hello to Arman StudioOS",
        model="qwen3:4b",
    )

    print("\n===== RESPONSE =====")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())