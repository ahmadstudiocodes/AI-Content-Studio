# providers/ollama/__init__.py
"""
Arman StudioOS
Ollama Provider Package

Local AI provider integration.
"""

from .client import OllamaProvider
from .config import OllamaConfig


__all__ = [
    "OllamaProvider",
    "OllamaConfig",
]