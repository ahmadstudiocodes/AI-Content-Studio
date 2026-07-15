# providers/openai/client.py
"""
Arman StudioOS
OpenAI Provider Client

OpenAI API provider implementation.
"""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict

import aiohttp

from ..base import BaseProvider
from ..exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderResponseError,
)
from ..types import (
    ProviderCapabilities,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
)

from .config import OpenAIConfig


class OpenAIProvider(BaseProvider):
    """
    OpenAI cloud provider.

    Compatible with OpenAI Chat Completions API.
    """

    def __init__(
        self,
        config: ProviderConfig | OpenAIConfig,
    ) -> None:

        super().__init__(
            config
        )

        self.config = config

        self.api_key = getattr(
            config,
            "api_key",
            None,
        )

        self.endpoint = getattr(
            config,
            "endpoint",
            "https://api.openai.com/v1",
        )

        self.model = getattr(
            config,
            "model",
            "gpt-4.1-mini",
        )


    @property
    def name(
        self,
    ) -> str:
        return "openai"


    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:

        return ProviderCapabilities(
            chat=True,
            completion=True,
            streaming=True,
            embedding=True,
            vision=True,
            tool_calling=True,
            function_calling=True,
        )


    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:
        """
        Generate response using OpenAI API.
        """

        if not self.api_key:

            raise ProviderAuthenticationError(
                "OpenAI API key missing",
                provider=self.name,
            )


        payload = {
            "model": (
                request.model
                or self.model
            ),
            "messages": [
                {
                    "role": "system",
                    "content": (
                        request.system_prompt
                        or "You are a helpful assistant."
                    ),
                },
                {
                    "role": "user",
                    "content": request.prompt,
                },
            ],
            "temperature": request.temperature,
        }


        headers = {
            "Authorization": (
                f"Bearer {self.api_key}"
            ),
            "Content-Type": (
                "application/json"
            ),
        }


        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{self.endpoint}/chat/completions",
                    json=payload,
                    headers=headers,
                ) as response:


                    if response.status == 401:

                        raise ProviderAuthenticationError(
                            "Invalid OpenAI API key",
                            provider=self.name,
                        )


                    if response.status != 200:

                        raise ProviderConnectionError(
                            "OpenAI request failed",
                            provider=self.name,
                        )


                    data = await response.json()


        except aiohttp.ClientError as exc:

            raise ProviderConnectionError(
                str(exc),
                provider=self.name,
            ) from exc


        try:

            content = (
                data["choices"][0]
                ["message"]
                ["content"]
            )


        except (
            KeyError,
            IndexError,
        ) as exc:

            raise ProviderResponseError(
                "Invalid OpenAI response",
                provider=self.name,
            ) from exc


        return ProviderResponse(
            content=content,
            provider=self.name,
            model=payload["model"],
            metadata=data,
        )


    async def stream(
        self,
        request: ProviderRequest,
    ) -> AsyncIterator[str]:
        """
        Streaming response support.
        """

        if not self.api_key:

            raise ProviderAuthenticationError(
                "OpenAI API key missing",
                provider=self.name,
            )


        payload = {
            "model": (
                request.model
                or self.model
            ),
            "messages": [
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
            "stream": True,
        }


        headers = {
            "Authorization": (
                f"Bearer {self.api_key}"
            ),
            "Content-Type": (
                "application/json"
            ),
        }


        async with aiohttp.ClientSession() as session:

            async with session.post(
                f"{self.endpoint}/chat/completions",
                json=payload,
                headers=headers,
            ) as response:


                async for line in (
                    response.content
                ):

                    if not line:
                        continue

                    decoded = line.decode(
                        "utf-8"
                    )

                    if decoded.startswith(
                        "data:"
                    ):

                        yield (
                            decoded
                            .replace(
                                "data:",
                                "",
                            )
                            .strip()
                        )


    async def health_check(
        self,
    ) -> Dict[str, Any]:
        """
        Basic provider health state.
        """

        return {
            "provider": self.name,
            "available": bool(
                self.api_key
            ),
            "endpoint": self.endpoint,
            "model": self.model,
        }


__all__ = [
    "OpenAIProvider",
]