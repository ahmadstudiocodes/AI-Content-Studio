"""
Arman StudioOS

Enterprise Retry Manager
"""

from __future__ import annotations

import time
from typing import Callable, Optional, Tuple, Type


# ============================================================
# Retry Policy
# ============================================================

class RetryPolicy:

    def __init__(
        self,
        retries: int = 3,
        delay: float = 0.0,
        retry_exceptions: Tuple[
            Type[Exception],
            ...
        ] = (
            TimeoutError,
            ConnectionError,
        ),
    ):

        self.retries = retries

        self.delay = delay

        self.retry_exceptions = (
            retry_exceptions
        )

    def should_retry(
        self,
        attempt: int
    ) -> bool:

        return attempt < self.retries


# ============================================================
# Retry Manager
# ============================================================

class RetryManager:

    def __init__(
        self,
        policy: Optional[
            RetryPolicy
        ] = None
    ):

        self.policy = (
            policy
            or RetryPolicy()
        )

    def execute(
        self,
        callback: Callable,
        *args,
        **kwargs
    ):

        attempt = 0

        while True:

            try:

                return callback(
                    *args,
                    **kwargs
                )

            except self.policy.retry_exceptions:

                attempt += 1

                if not self.policy.should_retry(
                    attempt
                ):
                    raise

                if self.policy.delay > 0:

                    time.sleep(
                        self.policy.delay
                    )

            except Exception:

                raise

    def update_policy(
        self,
        policy: RetryPolicy
    ):

        self.policy = policy

    def reset(self):

        self.policy = RetryPolicy()


# ============================================================
# Singleton
# ============================================================

retry_manager = RetryManager()