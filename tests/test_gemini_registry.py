import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.registry import provider_registry
from providers.gemini.client import GeminiProvider


def main():

    print("\n=== Gemini Registry Test ===")


    provider_registry.register(
        GeminiProvider
    )


    assert provider_registry.exists(
        "geminiprovider"
    )


    print(
        "✅ Gemini Registered"
    )


    provider = provider_registry.get(
        "geminiprovider"
    )


    print(
        "✅ Provider Found:",
        provider.__name__
    )


    print(
        "\n🎉 Gemini Registry Validation Passed"
    )


if __name__ == "__main__":
    main()