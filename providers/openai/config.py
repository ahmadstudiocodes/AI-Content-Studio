# providers/openai/config.py
"""
Arman StudioOS
OpenAI Provider Configuration

Configuration model for OpenAI API runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OpenAIConfig:
    """
    OpenAI runtime configuration.
    """

    name: str = "openai"

    api_key: Optional[str] = None

    endpoint: str = (
        "https://api.openai.com/v1"
    )

    model: str = (
        "gpt-4.1-mini"
    )

    timeout: float = 60.0

    enabled: bool = True

    organization: Optional[str] = None

    project: Optional[str] = None

    options: Dict[str, Any] = field(
        default_factory=dict
    )


    def to_dict(
        self,
    ) -> Dict[str, Any]:
        """
        Serialize configuration.
        """

        return {
            "name": self.name,
            "api_key": self.api_key,
            "endpoint": self.endpoint,
            "model": self.model,
            "timeout": self.timeout,
            "enabled": self.enabled,
            "organization": self.organization,
            "project": self.project,
            "options": self.options,
        }


    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "OpenAIConfig":
        """
        Create configuration from dictionary.
        """

        return cls(
            name=data.get(
                "name",
                "openai",
            ),
            api_key=data.get(
                "api_key"
            ),
            endpoint=data.get(
                "endpoint",
                "https://api.openai.com/v1",
            ),
            model=data.get(
                "model",
                "gpt-4.1-mini",
            ),
            timeout=data.get(
                "timeout",
                60.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            organization=data.get(
                "organization"
            ),
            project=data.get(
                "project"
            ),
            options=data.get(
                "options",
                {},
            ),
        )


__all__ = [
    "OpenAIConfig",
]