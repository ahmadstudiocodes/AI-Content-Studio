# providers/types.py
"""
Arman StudioOS
Provider Type Definitions

Shared data models used by all AI providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderType(str, Enum):
    """
    Supported provider categories.
    """

    CLOUD = "cloud"
    LOCAL = "local"
    HYBRID = "hybrid"


class ProviderCapability(str, Enum):
    """
    AI provider capabilities.
    """

    CHAT = "chat"
    COMPLETION = "completion"
    STREAMING = "streaming"
    EMBEDDING = "embedding"
    VISION = "vision"
    TOOL_CALLING = "tool_calling"
    FUNCTION_CALLING = "function_calling"


@dataclass(
    frozen=True,
)
class ProviderCapabilities:
    """
    Provider feature map.
    """

    chat: bool = False
    completion: bool = False
    streaming: bool = False
    embedding: bool = False
    vision: bool = False
    tool_calling: bool = False
    function_calling: bool = False


    def supports(
        self,
        capability: ProviderCapability,
    ) -> bool:
        """
        Check capability support.
        """

        mapping = {
            ProviderCapability.CHAT: self.chat,
            ProviderCapability.COMPLETION: self.completion,
            ProviderCapability.STREAMING: self.streaming,
            ProviderCapability.EMBEDDING: self.embedding,
            ProviderCapability.VISION: self.vision,
            ProviderCapability.TOOL_CALLING: self.tool_calling,
            ProviderCapability.FUNCTION_CALLING: (
                self.function_calling
            ),
        }

        return mapping.get(
            capability,
            False,
        )


    def to_dict(
        self,
    ) -> Dict[str, bool]:
        """
        Serialize capabilities.
        """

        return {
            "chat": self.chat,
            "completion": self.completion,
            "streaming": self.streaming,
            "embedding": self.embedding,
            "vision": self.vision,
            "tool_calling": self.tool_calling,
            "function_calling": self.function_calling,
        }


@dataclass
class ProviderConfig:
    """
    Provider runtime configuration.
    """

    name: str

    provider_type: ProviderType = (
        ProviderType.LOCAL
    )

    model: Optional[str] = None

    api_key: Optional[str] = None

    endpoint: Optional[str] = None

    timeout: float = 60.0

    enabled: bool = True

    options: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProviderRequest:
    """
    Standard AI request object.
    """

    prompt: str

    model: Optional[str] = None

    system_prompt: Optional[str] = None

    temperature: float = 0.7

    max_tokens: Optional[int] = None

    stream: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProviderResponse:
    """
    Standard AI response object.
    """

    content: str

    provider: str

    model: Optional[str] = None

    tokens_used: Optional[int] = None

    finish_reason: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ProviderInfo:
    """
    Provider registration information.
    """

    name: str

    provider_type: ProviderType

    capabilities: ProviderCapabilities

    description: str = ""

    version: str = "1.0.0"

    enabled: bool = True


__all__ = [
    "ProviderType",
    "ProviderCapability",
    "ProviderCapabilities",
    "ProviderConfig",
    "ProviderRequest",
    "ProviderResponse",
    "ProviderInfo",
]