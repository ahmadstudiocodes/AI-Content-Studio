import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio

from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.gemini.client import GeminiProvider
from providers.types import ProviderConfig, ProviderType


async def main():

    print("\n=== Gemini Manager Test ===")


    # Register Provider

    provider_registry.register(
        GeminiProvider
    )

    print(
        "✅ Registry Register OK"
    )


    # Register Config

    provider_config_manager.register(
        ProviderConfig(
            name="geminiprovider",
            provider_type=ProviderType.CLOUD,
            endpoint=(
                "https://generativelanguage.googleapis.com/v1beta"
            ),
            model="gemini-2.0-flash",
        )
    )


    print(
        "✅ Config Register OK"
    )


    manager = ProviderManager()


    provider = await manager.load(
        "geminiprovider"
    )


    print(
        "✅ Load OK:",
        provider.name,
    )


    loaded = manager.get(
        "geminiprovider"
    )


    print(
        "✅ Get OK:",
        loaded.name,
    )


    health = await manager.health()


    print(
        "✅ Health OK:"
    )

    print(
        health
    )


    await manager.unload(
        "geminiprovider"
    )


    print(
        "✅ Unload OK"
    )


    print(
        "\n🎉 Gemini Manager Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())