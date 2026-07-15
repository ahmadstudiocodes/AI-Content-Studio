"""
Arman StudioOS
Gemini Provider Configuration

Configuration model for Google Gemini API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class GeminiConfig:
    """
    Gemini runtime configuration.
    """

    name: str = "gemini"

    api_key: Optional[str] = None

    endpoint: str = (
        "https://generativelanguage.googleapis.com/v1beta"
    )

    model: str = (
        "gemini-2.0-flash"
    )

    timeout: float = 60.0

    enabled: bool = True

    project: Optional[str] = None

    location: Optional[str] = None

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
            "project": self.project,
            "location": self.location,
            "options": self.options,
        }


    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "GeminiConfig":
        """
        Create config from dictionary.
        """

        return cls(
            name=data.get(
                "name",
                "gemini",
            ),
            api_key=data.get(
                "api_key"
            ),
            endpoint=data.get(
                "endpoint",
                "https://generativelanguage.googleapis.com/v1beta",
            ),
            model=data.get(
                "model",
                "gemini-2.0-flash",
            ),
            timeout=data.get(
                "timeout",
                60.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            project=data.get(
                "project"
            ),
            location=data.get(
                "location"
            ),
            options=data.get(
                "options",
                {},
            ),
        )


__all__ = [
    "GeminiConfig",
]