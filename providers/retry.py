"""
Arman StudioOS
Provider Retry Engine

Resilience layer for provider execution.
"""

from __future__ import annotations

import asyncio

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class RetryPolicy:
    """
    Retry configuration.
    """

    max_attempts: int = 3

    initial_delay: float = 0.5

    backoff_factor: float = 2.0



class ProviderRetryEngine:
    """
    Executes retry strategy.
    """


    def __init__(
        self,
        policy: RetryPolicy | None = None,
    ) -> None:

        self.policy = (
            policy
            or RetryPolicy()
        )

        self.attempts = 0



    async def execute(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute function with retry.
        """

        delay = (
            self.policy.initial_delay
        )


        last_error = None


        for attempt in range(
            1,
            self.policy.max_attempts + 1,
        ):

            self.attempts = attempt


            try:

                return await func(
                    *args,
                    **kwargs,
                )


            except Exception as exc:

                last_error = exc


                if (
                    attempt
                    >=
                    self.policy.max_attempts
                ):
                    break


                await asyncio.sleep(
                    delay
                )


                delay *= (
                    self.policy.backoff_factor
                )


        raise last_error



__all__ = [
    "RetryPolicy",
    "ProviderRetryEngine",
]