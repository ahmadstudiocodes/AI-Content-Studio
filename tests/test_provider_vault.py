import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.vault import (
    provider_vault,
)



def main():

    print("\n=== Provider Vault Test ===")


    provider_vault.save(
        "openai",
        {
            "model": "gpt-4.1-mini",
            "api_key": "sk-test-secret",
        },
    )


    raw = (
        provider_vault._configs[
            "openai"
        ]
    )


    print(
        "Stored:",
        raw,
    )


    loaded = (
        provider_vault.load(
            "openai"
        )
    )


    print(
        "Loaded:",
        loaded,
    )


    assert (
        loaded["api_key"]
        ==
        "sk-test-secret"
    )


    assert (
        raw["api_key"]
        !=
        "sk-test-secret"
    )


    print(
        "\n🎉 Provider Vault Validation Passed"
    )



if __name__ == "__main__":
    main()