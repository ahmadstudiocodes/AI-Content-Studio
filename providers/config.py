# providers/config.py
"""
Arman StudioOS
Provider Configuration System

Central configuration management for all AI providers.
"""

from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from .exceptions import ProviderConfigurationError
from .types import (
    ProviderConfig,
    ProviderType,
)


class ProviderConfigManager:
    """
    Manage provider configurations.

    Responsibilities:
    - Create configs
    - Load environment settings
    - Validate configurations
    - Export configurations
    """

    def __init__(
        self,
        config_path: Optional[str | Path] = None,
    ) -> None:

        self.config_path = (
            Path(config_path)
            if config_path
            else None
        )

        self._configs: Dict[str, ProviderConfig] = {}


    def register(
        self,
        config: ProviderConfig,
    ) -> None:
        """
        Register provider configuration.
        """

        self.validate(config)

        self._configs[
            config.name
        ] = config


    def get(
        self,
        name: str,
    ) -> ProviderConfig:

        if name not in self._configs:
            raise ProviderConfigurationError(
                f"Provider config not found: {name}",
                provider=name,
            )

        return self._configs[name]


    def remove(
        self,
        name: str,
    ) -> None:

        self._configs.pop(
            name,
            None,
        )


    def all(
        self,
    ) -> Dict[str, ProviderConfig]:
        """
        Return all configurations.
        """

        return dict(
            self._configs
        )


    def validate(
        self,
        config: ProviderConfig,
    ) -> bool:
        """
        Validate provider configuration.
        """

        if not config.name:
            raise ProviderConfigurationError(
                "Provider name is required"
            )

        if not isinstance(
            config.provider_type,
            ProviderType,
        ):
            raise ProviderConfigurationError(
                "Invalid provider type",
                provider=config.name,
            )

        if config.timeout <= 0:
            raise ProviderConfigurationError(
                "Timeout must be positive",
                provider=config.name,
            )

        return True


    def load_environment(
        self,
        name: str,
        prefix: str = "PROVIDER",
    ) -> ProviderConfig:
        """
        Load provider configuration from environment.

        Example:
            PROVIDER_API_KEY
            PROVIDER_ENDPOINT
        """

        config = ProviderConfig(
            name=name,
            api_key=os.getenv(
                f"{prefix}_API_KEY"
            ),
            endpoint=os.getenv(
                f"{prefix}_ENDPOINT"
            ),
            model=os.getenv(
                f"{prefix}_MODEL"
            ),
        )

        self.register(
            config
        )

        return config


    def export(
        self,
        name: str,
    ) -> Dict[str, Any]:
        """
        Export provider configuration.
        """

        config = self.get(
            name
        )

        return asdict(
            config
        )


    def clear(
        self,
    ) -> None:
        """
        Remove all configurations.
        """

        self._configs.clear()


provider_config_manager = ProviderConfigManager()


__all__ = [
    "ProviderConfigManager",
    "provider_config_manager",
]