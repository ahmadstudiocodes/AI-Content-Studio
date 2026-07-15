import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.ollama.client import OllamaProvider
from providers.types import ProviderConfig, ProviderType


async def main():

    print("\n=== Provider Lifecycle Test ===")


    # Register Provider

    provider_registry.register(
        OllamaProvider,
        "ollama",
    )

    print(
        "✅ Registry Register OK"
    )


    # Register Config

    provider_config_manager.register(
        ProviderConfig(
            name="ollama",
            provider_type=ProviderType.LOCAL,
            endpoint=(
                "http://localhost:11434"
            ),
            model="qwen3:4b",
        )
    )


    print(
        "✅ Config Register OK"
    )


    manager = ProviderManager()


    # Load

    provider = await manager.load(
        "ollama"
    )


    print(
        "✅ Load OK:",
        provider.name,
    )


    # Get

    loaded = manager.get(
        "ollama"
    )


    print(
        "✅ Get OK:",
        loaded.name,
    )


    # Health

    health = await manager.health()


    print(
        "✅ Health OK:",
        health,
    )


    # Unload

    await manager.unload(
        "ollama"
    )


    print(
        "✅ Unload OK"
    )


    # Shutdown

    await manager.shutdown_all()


    print(
        "✅ Shutdown All OK"
    )


    print(
        "\n🎉 Provider Lifecycle Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())