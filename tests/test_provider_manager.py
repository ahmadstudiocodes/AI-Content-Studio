import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncio

from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.ollama.client import OllamaProvider
from providers.types import ProviderConfig, ProviderType, ProviderRequest


async def main():

    print("\n=== Provider Manager Test ===")


    provider_registry.register(
        OllamaProvider,
        "ollama",
    )

    print(
        "✅ Registry Register OK"
    )


    provider_config_manager.register(
        ProviderConfig(
            name="ollama",
            provider_type=ProviderType.LOCAL,
            endpoint="http://localhost:11434",
            model="qwen3:4b",
        )
    )

    print(
        "✅ Config Register OK"
    )


    manager = ProviderManager()


    provider = await manager.load(
        "ollama"
    )


    print(
        "✅ Load OK:",
        provider.name,
    )


    loaded = manager.get(
        "ollama"
    )


    print(
        "✅ Get OK:",
        loaded.name,
    )


    response = await manager.generate(
        "ollama",
        ProviderRequest(
            prompt="Explain Arman StudioOS"
        )
    )


    print(
        "\n===== MANAGER RESPONSE ====="
    )

    print(
        response.content
    )


    await manager.shutdown_all()


    print(
        "\n🎉 Provider Manager Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())