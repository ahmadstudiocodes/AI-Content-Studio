"""
Arman StudioOS
Provider Metrics

Usage and performance tracking.
"""

from __future__ import annotations

import time

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Dict, Any



@dataclass
class ProviderMetric:

    provider: str

    requests: int = 0

    successes: int = 0

    failures: int = 0

    total_latency: float = 0.0

    last_used: datetime | None = None


    @property
    def average_latency(
        self,
    ) -> float:

        if self.requests == 0:
            return 0.0

        return (
            self.total_latency
            /
            self.requests
        )



class ProviderMetrics:

    """
    Central metrics collector.
    """


    def __init__(
        self,
    ) -> None:

        self._metrics: Dict[
            str,
            ProviderMetric,
        ] = {}



    def _get(
        self,
        provider: str,
    ) -> ProviderMetric:

        if provider not in self._metrics:

            self._metrics[
                provider
            ] = ProviderMetric(
                provider=provider
            )

        return self._metrics[
            provider
        ]



    def record_success(
        self,
        provider: str,
        latency: float,
    ) -> None:

        metric = self._get(
            provider
        )

        metric.requests += 1

        metric.successes += 1

        metric.total_latency += latency

        metric.last_used = datetime.now(
            UTC
        )



    def record_failure(
        self,
        provider: str,
        latency: float = 0.0,
    ) -> None:

        metric = self._get(
            provider
        )

        metric.requests += 1

        metric.failures += 1

        metric.total_latency += latency



    def get(
        self,
        provider: str,
    ) -> Dict[str, Any]:

        metric = self._get(
            provider
        )

        return {
            "provider": metric.provider,
            "requests": metric.requests,
            "successes": metric.successes,
            "failures": metric.failures,
            "average_latency": (
                metric.average_latency
            ),
            "last_used": (
                metric.last_used.isoformat()
                if metric.last_used
                else None
            ),
        }



    def all(
        self,
    ) -> Dict[str, Any]:

        return {
            name: self.get(name)
            for name in self._metrics
        }



    def clear(
        self,
    ) -> None:

        self._metrics.clear()



provider_metrics = ProviderMetrics()



__all__ = [
    "ProviderMetric",
    "ProviderMetrics",
    "provider_metrics",
]