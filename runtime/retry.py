from __future__ import annotations

import time

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class RetryPolicy:

    max_attempts: int = 3

    delay_seconds: float = 0.1

    backoff_multiplier: float = 2.0



@dataclass
class RetryResult:

    success: bool

    data: Any = None

    attempts: int = 0

    error: str | None = None



class RuntimeRetryEngine:
    """
    Runtime retry controller.
    """


    def execute(
        self,
        operation: Callable,
        policy: RetryPolicy | None = None,
    ) -> RetryResult:


        if policy is None:

            policy = RetryPolicy()


        attempt = 0

        delay = policy.delay_seconds


        while attempt < policy.max_attempts:

            attempt += 1


            try:

                result = operation()


                return RetryResult(
                    success=True,
                    data=result,
                    attempts=attempt,
                )


            except Exception as exc:


                if attempt >= policy.max_attempts:

                    return RetryResult(
                        success=False,
                        attempts=attempt,
                        error=str(exc),
                    )


                time.sleep(delay)

                delay *= (
                    policy.backoff_multiplier
                )



runtime_retry_engine = RuntimeRetryEngine()