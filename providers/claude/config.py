"""
Arman StudioOS
Claude Provider Configuration

Configuration model for Anthropic Claude API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ClaudeConfig:
    """
    Claude runtime configuration.
    """

    name: str = "claude"

    api_key: Optional[str] = None

    endpoint: str = (
        "https://api.anthropic.com/v1"
    )

    model: str = (
        "claude-3-5-sonnet-latest"
    )

    timeout: float = 60.0

    enabled: bool = True

    organization: Optional[str] = None

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
            "options": self.options,
        }


    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "ClaudeConfig":
        """
        Create config from dictionary.
        """

        return cls(
            name=data.get(
                "name",
                "claude",
            ),
            api_key=data.get(
                "api_key"
            ),
            endpoint=data.get(
                "endpoint",
                "https://api.anthropic.com/v1",
            ),
            model=data.get(
                "model",
                "claude-3-5-sonnet-latest",
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
            options=data.get(
                "options",
                {},
            ),
        )


__all__ = [
    "ClaudeConfig",
]