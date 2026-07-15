import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.bootstrap import provider_bootstrap
from providers.registry import provider_registry



def main():

    print("\n=== Provider Bootstrap Test ===")


    provider_registry.clear()


    providers = (
        provider_bootstrap.initialize()
    )


    print(
        "Initialized Providers:",
        providers,
    )


    status = (
        provider_bootstrap.status()
    )


    print(
        "Status:",
        status,
    )


    assert status["initialized"] is True

    assert (
        status["registry_size"] >= 4
    )


    print(
        "\n🎉 Provider Bootstrap Validation Passed"
    )



if __name__ == "__main__":
    main()