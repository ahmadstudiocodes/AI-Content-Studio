import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio

from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.claude.client import ClaudeProvider
from providers.types import ProviderConfig, ProviderType


async def main():

    print("\n=== Claude Manager Test ===")


    # Register Provider

    provider_registry.register(
        ClaudeProvider
    )

    print(
        "✅ Registry Register OK"
    )


    # Register Config

    provider_config_manager.register(
        ProviderConfig(
            name="claudeprovider",
            provider_type=ProviderType.CLOUD,
            endpoint=(
                "https://api.anthropic.com/v1"
            ),
            model=(
                "claude-3-5-sonnet-latest"
            ),
        )
    )


    print(
        "✅ Config Register OK"
    )


    manager = ProviderManager()


    provider = await manager.load(
        "claudeprovider"
    )


    print(
        "✅ Load OK:",
        provider.name,
    )


    loaded = manager.get(
        "claudeprovider"
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
        "claudeprovider"
    )


    print(
        "✅ Unload OK"
    )


    await manager.shutdown_all()


    print(
        "✅ Shutdown All OK"
    )


    print(
        "\n🎉 Claude Manager Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())