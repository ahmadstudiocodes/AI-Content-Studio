# providers/ollama/client.py
"""
Arman StudioOS
Ollama Provider Client

Local Ollama model provider implementation.
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict

import aiohttp

from ..base import BaseProvider
from ..exceptions import (
    ProviderConnectionError,
    ProviderResponseError,
)
from ..types import (
    ProviderCapabilities,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
)

from .config import OllamaConfig


class OllamaProvider(BaseProvider):
    """
    Ollama local model provider.

    Communicates with Ollama HTTP API.
    """

    def __init__(
        self,
        config: ProviderConfig | OllamaConfig,
    ) -> None:

        super().__init__(
            config
        )

        self.config = config

        self.endpoint = getattr(
            config,
            "endpoint",
            "http://localhost:11434",
        )

        self.model = getattr(
            config,
            "model",
            "qwen3:4b",
        )


    @property
    def name(
        self,
    ) -> str:
        return "ollama"


    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:

        return ProviderCapabilities(
            chat=True,
            completion=True,
            streaming=True,
            embedding=False,
            vision=False,
            tool_calling=False,
        )


    async def initialize(
        self,
    ) -> None:
        """
        Initialize Ollama provider.
        """

        await super().initialize()


    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """
        Generate response using Ollama API.
        """

        payload = {
            "model": (
                request.model
                or self.model
            ),
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
            },
        }

        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{self.endpoint}/api/generate",
                    json=payload,
                ) as response:

                    if response.status != 200:
                        raise ProviderConnectionError(
                            "Ollama request failed",
                            provider=self.name,
                        )

                    data = await response.json()


        except aiohttp.ClientError as exc:

            raise ProviderConnectionError(
                str(exc),
                provider=self.name,
            ) from exc


        if "response" not in data:

            raise ProviderResponseError(
                "Invalid Ollama response",
                provider=self.name,
            )


        return ProviderResponse(
            content=data["response"],
            provider=self.name,
            model=payload["model"],
            metadata=data,
        )


    async def stream(
        self,
        request: ProviderRequest,
    ) -> AsyncIterator[str]:
        """
        Streaming generation.
        """

        payload = {
            "model": (
                request.model
                or self.model
            ),
            "prompt": request.prompt,
            "stream": True,
        }


        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{self.endpoint}/api/generate",
                    json=payload,
                ) as response:


                    async for line in (
                        response.content
                    ):

                        if not line:
                            continue


                        data = json.loads(
                            line.decode()
                        )


                        if "response" in data:
                            yield data["response"]


        except Exception as exc:

            raise ProviderConnectionError(
                str(exc),
                provider=self.name,
            ) from exc


    async def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Check Ollama server health.
        """

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    f"{self.endpoint}/api/tags"
                ) as response:

                    return {
                        "provider": self.name,
                        "available": (
                            response.status == 200
                        ),
                        "endpoint": self.endpoint,
                    }


        except Exception:

            return {
                "provider": self.name,
                "available": False,
                "endpoint": self.endpoint,
            }


__all__ = [
    "OllamaProvider",
]