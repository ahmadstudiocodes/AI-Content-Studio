import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.discovery import discover_providers
from providers.registry import provider_registry


def main():

    print("\n=== Provider Discovery Test ===")


    # Clean old registry
    provider_registry.clear()


    discovered = discover_providers()


    print(
        "Discovered:",
        discovered,
    )


    expected = [
        "ollama",
        "openai",
        "gemini",
        "claude",
    ]


    for provider in expected:

        if provider_registry.exists(
            provider
        ):

            print(
                f"✅ Found: {provider}"
            )

        else:

            raise Exception(
                f"Provider missing: {provider}"
            )


    print(
        "\nRegistered Providers:"
    )

    print(
        list(
            provider_registry.list()
        )
    )


    print(
        "\n🎉 Provider Discovery Validation Passed"
    )


if __name__ == "__main__":
    main()