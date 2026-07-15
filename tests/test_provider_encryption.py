import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.encryption import (
    provider_encryption,
)



def main():

    print("\n=== Provider Encryption Test ===")


    secret = (
        "sk-openai-secret-key"
    )


    encrypted = (
        provider_encryption.encrypt(
            secret
        )
    )


    print(
        "Encrypted:",
        encrypted[:30],
        "..."
    )


    decrypted = (
        provider_encryption.decrypt(
            encrypted
        )
    )


    print(
        "Decrypted:",
        decrypted,
    )


    assert decrypted == secret


    print(
        "\n🎉 Provider Encryption Validation Passed"
    )



if __name__ == "__main__":
    main()