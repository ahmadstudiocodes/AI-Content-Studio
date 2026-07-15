"""
Arman StudioOS
Gemini Provider Client

Google Gemini API provider implementation.
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


class GeminiProvider(BaseProvider):
    """
    Google Gemini cloud provider.
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
            "https://generativelanguage.googleapis.com/v1beta",
        )

        self.model = getattr(
            config,
            "model",
            "gemini-2.0-flash",
        )


    @property
    def name(
        self,
    ) -> str:

        return "gemini"


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
                "Gemini API key missing",
                provider=self.name,
            )


        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": request.prompt
                        }
                    ]
                }
            ]
        }


        url = (
            f"{self.endpoint}/models/"
            f"{request.model or self.model}"
            f":generateContent"
            f"?key={self.api_key}"
        )


        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    url,
                    json=payload,
                ) as response:

                    if response.status != 200:

                        raise ProviderConnectionError(
                            "Gemini request failed",
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
                data["candidates"][0]
                ["content"]
                ["parts"][0]
                ["text"]
            )


        except (
            KeyError,
            IndexError,
        ) as exc:

            raise ProviderResponseError(
                "Invalid Gemini response",
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
            "Gemini streaming will be implemented in runtime upgrade"
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
    "GeminiProvider",
]