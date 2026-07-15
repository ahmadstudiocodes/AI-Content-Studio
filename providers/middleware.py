"""
Arman StudioOS
Provider Middleware Layer

Request pipeline middleware for AI providers.
"""

from __future__ import annotations

import time
from typing import Any, Awaitable, Callable, Dict


ProviderHandler = Callable[
    [Any],
    Awaitable[Any],
]


class ProviderMiddleware:
    """
    Base middleware component.
    """

    async def before(
        self,
        request: Any,
    ) -> Any:
        return request


    async def after(
        self,
        request: Any,
        response: Any,
    ) -> Any:
        return response



class TimingMiddleware(
    ProviderMiddleware
):
    """
    Measures execution time.
    """

    def __init__(
        self,
    ) -> None:

        self.last_duration = 0.0


    async def before(
        self,
        request: Any,
    ) -> Any:

        self._start = time.time()

        return request


    async def after(
        self,
        request: Any,
        response: Any,
    ) -> Any:

        self.last_duration = (
            time.time()
            -
            self._start
        )

        return response



class MiddlewarePipeline:
    """
    Executes provider middleware chain.
    """

    def __init__(
        self,
    ) -> None:

        self.middlewares = []


    def add(
        self,
        middleware: ProviderMiddleware,
    ) -> None:

        self.middlewares.append(
            middleware
        )


    async def process_before(
        self,
        request: Any,
    ) -> Any:

        for middleware in (
            self.middlewares
        ):
            request = await middleware.before(
                request
            )

        return request


    async def process_after(
        self,
        request: Any,
        response: Any,
    ) -> Any:

        for middleware in reversed(
            self.middlewares
        ):
            response = await middleware.after(
                request,
                response,
            )

        return response



provider_middleware = MiddlewarePipeline()


__all__ = [
    "ProviderMiddleware",
    "TimingMiddleware",
    "MiddlewarePipeline",
    "provider_middleware",
]
