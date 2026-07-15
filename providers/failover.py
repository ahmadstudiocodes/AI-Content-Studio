"""
Arman StudioOS
Provider Failover System

Fallback and retry management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FailoverPolicy:
    """
    Provider fallback policy.
    """

    providers: List[str] = field(
        default_factory=list
    )

    max_retries: int = 1



class ProviderFailover:

    """
    Provider fallback resolver.
    """


    def __init__(
        self,
        policy: FailoverPolicy | None = None,
    ) -> None:

        self.policy = (
            policy
            or FailoverPolicy()
        )


        self.failures: Dict[
            str,
            int,
        ] = {}



    def next_provider(
        self,
        failed_provider: str,
    ) -> str | None:
        """
        Return next available provider.
        """


        providers = (
            self.policy.providers
        )


        if failed_provider not in providers:
            return None


        index = providers.index(
            failed_provider
        )


        if (
            index + 1
            <
            len(providers)
        ):

            return providers[
                index + 1
            ]


        return None



    def record_failure(
        self,
        provider: str,
    ) -> None:

        self.failures[
            provider
        ] = (
            self.failures.get(
                provider,
                0,
            )
            + 1
        )



    def health(
        self,
    ) -> Dict[str, int]:

        return dict(
            self.failures
        )



__all__ = [
    "FailoverPolicy",
    "ProviderFailover",
]