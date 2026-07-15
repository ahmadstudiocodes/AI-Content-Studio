import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.ollama.client import OllamaProvider
from providers.openai.client import OpenAIProvider
from providers.gemini.client import GeminiProvider
from providers.claude.client import ClaudeProvider

from providers.types import (
    ProviderConfig,
    ProviderType,
)


async def main():

    print("\n=== Multi Provider Integration Test ===")


    # Clear old state
    provider_registry.clear()
    provider_config_manager.clear()


    # Register Providers

    provider_registry.register(
        OllamaProvider,
        "ollama",
    )

    print(
        "✅ Registered: ollama"
    )


    provider_registry.register(
        OpenAIProvider,
        "openai",
    )

    print(
        "✅ Registered: openai"
    )


    provider_registry.register(
        GeminiProvider,
        "gemini",
    )

    print(
        "✅ Registered: gemini"
    )


    provider_registry.register(
        ClaudeProvider,
        "claude",
    )

    print(
        "✅ Registered: claude"
    )



    # Register Configs

    configs = [

        ProviderConfig(
            name="ollama",
            provider_type=ProviderType.LOCAL,
            endpoint="http://localhost:11434",
            model="qwen3:4b",
        ),


        ProviderConfig(
            name="openai",
            provider_type=ProviderType.CLOUD,
            endpoint="https://api.openai.com/v1",
            model="gpt-4.1-mini",
        ),


        ProviderConfig(
            name="gemini",
            provider_type=ProviderType.CLOUD,
            endpoint="https://generativelanguage.googleapis.com/v1beta",
            model="gemini-2.0-flash",
        ),


        ProviderConfig(
            name="claude",
            provider_type=ProviderType.CLOUD,
            endpoint="https://api.anthropic.com/v1",
            model="claude-3-5-sonnet-latest",
        ),

    ]


    for config in configs:

        provider_config_manager.register(
            config
        )


    manager = ProviderManager()



    # Load All Providers

    providers = [
        "ollama",
        "openai",
        "gemini",
        "claude",
    ]


    for name in providers:

        provider = await manager.load(
            name
        )

        print(
            "✅ Loaded:",
            name,
        )



    # Health

    health = await manager.health()


    print(
        "\n✅ Health:"
    )

    print(
        health
    )



    # Shutdown

    await manager.shutdown_all()


    print(
        "\n✅ Shutdown Complete"
    )


    print(
        "\n🎉 Multi Provider Integration Validation Passed"
    )



if __name__ == "__main__":

    asyncio.run(main())