"""
Arman StudioOS
Provider Encryption Layer

Secret encryption utilities.
"""

from __future__ import annotations

from cryptography.fernet import Fernet



class SecretEncryption:

    """
    Encrypt and decrypt provider secrets.
    """


    def __init__(
        self,
        key: bytes | None = None,
    ) -> None:

        self.key = (
            key
            or Fernet.generate_key()
        )

        self.cipher = Fernet(
            self.key
        )



    def encrypt(
        self,
        value: str,
    ) -> str:

        encrypted = (
            self.cipher.encrypt(
                value.encode(
                    "utf-8"
                )
            )
        )

        return encrypted.decode(
            "utf-8"
        )



    def decrypt(
        self,
        value: str,
    ) -> str:

        decrypted = (
            self.cipher.decrypt(
                value.encode(
                    "utf-8"
                )
            )
        )

        return decrypted.decode(
            "utf-8"
        )



provider_encryption = SecretEncryption()



__all__ = [
    "SecretEncryption",
    "provider_encryption",
]