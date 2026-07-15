# providers/ollama/config.py
"""
Arman StudioOS
Ollama Provider Configuration

Configuration model for local Ollama runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OllamaConfig:
    """
    Ollama runtime configuration.
    """

    name: str = "ollama"

    endpoint: str = (
        "http://localhost:11434"
    )

    model: str = (
        "qwen3:4b"
    )

    timeout: float = 120.0

    enabled: bool = True

    keep_alive: str = (
        "5m"
    )

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
            "endpoint": self.endpoint,
            "model": self.model,
            "timeout": self.timeout,
            "enabled": self.enabled,
            "keep_alive": self.keep_alive,
            "options": self.options,
        }


    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "OllamaConfig":
        """
        Create config from dictionary.
        """

        return cls(
            name=data.get(
                "name",
                "ollama",
            ),
            endpoint=data.get(
                "endpoint",
                "http://localhost:11434",
            ),
            model=data.get(
                "model",
                "qwen3:4b",
            ),
            timeout=data.get(
                "timeout",
                120.0,
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            keep_alive=data.get(
                "keep_alive",
                "5m",
            ),
            options=data.get(
                "options",
                {},
            ),
        )


__all__ = [
    "OllamaConfig",
]