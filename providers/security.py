"""
Arman StudioOS
Provider Security

Secret management and masking utilities.
"""

from __future__ import annotations

from typing import Dict, Optional


class SecretManager:
    """
    Manage provider secrets safely.
    """


    def __init__(self):

        self._secrets: Dict[
            str,
            str,
        ] = {}



    def set(
        self,
        name: str,
        value: str,
    ) -> None:

        self._secrets[
            name
        ] = value



    def get(
        self,
        name: str,
    ) -> Optional[str]:

        return self._secrets.get(
            name
        )



    def remove(
        self,
        name: str,
    ) -> None:

        self._secrets.pop(
            name,
            None,
        )



    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._secrets



    def mask(
        self,
        value: str | None,
    ) -> str:

        if not value:
            return ""


        if len(value) <= 8:
            return "****"


        return (
            value[:4]
            +
            "****"
            +
            value[-4:]
        )



provider_secrets = SecretManager()



__all__ = [
    "SecretManager",
    "provider_secrets",
]