"""
Arman StudioOS
Claude Provider Client

Anthropic Claude API provider implementation.
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


class ClaudeProvider(BaseProvider):
    """
    Anthropic Claude cloud provider.
    """

    def __init__(
        self,
        config: ProviderConfig,
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
            "https://api.anthropic.com/v1",
        )

        self.model = getattr(
            config,
            "model",
            "claude-3-5-sonnet-latest",
        )


    @property
    def name(
        self,
    ) -> str:

        return "claude"


    @property
    def capabilities(
        self,
    ) -> ProviderCapabilities:

        return ProviderCapabilities(
            chat=True,
            completion=True,
            streaming=True,
            embedding=False,
            vision=True,
            tool_calling=True,
            function_calling=True,
        )


    async def generate(
        self,
        request: ProviderRequest,
    ) -> ProviderResponse:

        if not self.api_key:

            raise ProviderAuthenticationError(
                "Claude API key missing",
                provider=self.name,
            )


        payload = {
            "model": (
                request.model
                or self.model
            ),
            "max_tokens": (
                request.max_tokens
                or 1024
            ),
            "messages": [
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
        }


        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }


        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    f"{self.endpoint}/messages",
                    json=payload,
                    headers=headers,
                ) as response:


                    if response.status == 401:

                        raise ProviderAuthenticationError(
                            "Invalid Claude API key",
                            provider=self.name,
                        )


                    if response.status != 200:

                        raise ProviderConnectionError(
                            "Claude request failed",
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
                data["content"][0]["text"]
            )


        except (
            KeyError,
            IndexError,
        ) as exc:

            raise ProviderResponseError(
                "Invalid Claude response",
                provider=self.name,
            ) from exc


        return ProviderResponse(
            content=content,
            provider=self.name,
            model=(
                request.model
                or self.model
            ),
            metadata=data,
        )


    async def stream(
        self,
        request: ProviderRequest,
    ) -> AsyncIterator[str]:

        raise NotImplementedError(
            "Claude streaming will be implemented in runtime upgrade"
        )


    async def health_check(
        self,
    ) -> Dict[str, Any]:

        return {
            "provider": self.name,
            "available": bool(
                self.api_key
            ),
            "endpoint": self.endpoint,
            "model": self.model,
        }


__all__ = [
    "ClaudeProvider",
]