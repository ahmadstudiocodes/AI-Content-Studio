"""
Arman StudioOS
Provider Configuration Vault

Secure storage for provider configurations.
"""

from __future__ import annotations

from typing import Dict, Any, Optional


from .encryption import (
    SecretEncryption,
)



class ProviderVault:
    """
    Secure provider configuration storage.
    """


    def __init__(
        self,
        encryption: SecretEncryption | None = None,
    ) -> None:

        self.encryption = (
            encryption
            or SecretEncryption()
        )


        self._configs: Dict[
            str,
            Dict[str, Any],
        ] = {}



    def save(
        self,
        provider: str,
        config: Dict[str, Any],
    ) -> None:
        """
        Save provider configuration securely.
        """


        stored = dict(
            config
        )


        if (
            "api_key"
            in stored
            and stored["api_key"]
        ):

            stored["api_key"] = (
                self.encryption.encrypt(
                    stored["api_key"]
                )
            )


        self._configs[
            provider
        ] = stored



    def load(
        self,
        provider: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Load configuration.
        """


        config = self._configs.get(
            provider
        )


        if not config:
            return None


        result = dict(
            config
        )


        if (
            "api_key"
            in result
            and result["api_key"]
        ):

            result["api_key"] = (
                self.encryption.decrypt(
                    result["api_key"]
                )
            )


        return result



    def exists(
        self,
        provider: str,
    ) -> bool:

        return (
            provider
            in self._configs
        )



    def remove(
        self,
        provider: str,
    ) -> None:

        self._configs.pop(
            provider,
            None,
        )



    def list(
        self,
    ):

        return list(
            self._configs.keys()
        )



provider_vault = ProviderVault()



__all__ = [
    "ProviderVault",
    "provider_vault",
]