import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.security import (
    provider_secrets,
)



def main():

    print("\n=== Provider Security Test ===")


    provider_secrets.set(
        "openai_key",
        "sk-1234567890abcdef",
    )


    key = provider_secrets.get(
        "openai_key"
    )


    print(
        "Stored:",
        provider_secrets.mask(
            key
        )
    )


    assert key == (
        "sk-1234567890abcdef"
    )


    assert (
        provider_secrets.mask(key)
        ==
        "sk-1****cdef"
    )


    print(
        "\n🎉 Provider Security Validation Passed"
    )



if __name__ == "__main__":
    main()