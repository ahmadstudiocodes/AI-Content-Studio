import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import asyncio


from providers.manager import ProviderManager
from providers.health import ProviderHealthMonitor

from providers.bootstrap import provider_bootstrap
from providers.config import provider_config_manager

from providers.types import ProviderConfig, ProviderType



async def main():

    print("\n=== Provider Health Test ===")


    provider_bootstrap.initialize()


    provider_config_manager.register(
        ProviderConfig(
            name="ollama",
            provider_type=ProviderType.LOCAL,
            endpoint="http://localhost:11434",
            model="qwen3:4b",
        )
    )


    manager = ProviderManager()


    await manager.load(
        "ollama"
    )


    monitor = ProviderHealthMonitor(
        manager
    )


    result = await monitor.check_all()


    print(
        "Health Report:"
    )

    print(
        result
    )


    assert (
        result["total"] >= 1
    )


    print(
        "\n🎉 Provider Health Validation Passed"
    )


if __name__ == "__main__":
    asyncio.run(main())