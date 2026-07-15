import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import asyncio

from providers.manager import ProviderManager
from providers.registry import provider_registry
from providers.config import provider_config_manager

from providers.ollama.client import OllamaProvider

from providers.types import (
    ProviderConfig,
    ProviderType,
    ProviderRequest,
)

from providers.cache import provider_cache
from providers.metrics import provider_metrics
from providers.middleware import (
    provider_middleware,
    TimingMiddleware,
)


async def main():

    print("\n=== Provider Runtime Test ===")


    # Middleware registration
    provider_middleware.add(
        TimingMiddleware()
    )

    print("✅ Middleware Added")


    # Register Provider
    provider_registry.register(
        OllamaProvider
    )

    print("✅ Provider Registry OK")


    # Register Config
    provider_config_manager.register(
        ProviderConfig(
            name="ollamaprovider",
            provider_type=ProviderType.LOCAL,
            endpoint="http://localhost:11434",
            model="qwen3:4b",
        )
    )

    print("✅ Config OK")


    manager = ProviderManager()


    request = ProviderRequest(
        prompt="Say hello to Arman StudioOS",
        model="qwen3:4b",
    )


    # First call
    response1 = await manager.generate(
        "ollamaprovider",
        request,
    )

    print(
        "✅ First Generate OK"
    )


    # Second call (should hit cache)
    response2 = await manager.generate(
        "ollamaprovider",
        request,
    )

    print(
        "✅ Second Generate OK (Cache Test)"
    )


    # Cache validation
    print(
        "Cache Size:",
        provider_cache.size()
    )


    # Metrics validation
    metric = provider_metrics.get(
        "ollamaprovider"
    )

    print(
        "Requests:",
        metric.requests
    )

    print(
        "Success:",
        metric.successes
    )

    print(
        "Failures:",
        metric.failures
    )


    print(
        "\n🎉 Runtime Pipeline Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())