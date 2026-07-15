import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.registry import provider_registry
from providers.claude.client import ClaudeProvider


def main():

    print("\n=== Claude Registry Test ===")


    provider_registry.register(
        ClaudeProvider
    )


    print(
        "✅ Claude Registered"
    )


    assert provider_registry.exists(
        "claudeprovider"
    )


    provider = provider_registry.get(
        "claudeprovider"
    )


    print(
        "✅ Provider Found:",
        provider.__name__,
    )


    print(
        "\n🎉 Claude Registry Validation Passed"
    )


if __name__ == "__main__":
    main()