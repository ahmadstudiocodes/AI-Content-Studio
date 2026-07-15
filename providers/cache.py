"""
Arman StudioOS
Provider Cache Layer

Runtime response caching for AI providers.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class CacheEntry:
    """
    Cached provider response.
    """

    value: Any

    created_at: float

    ttl: float


class ProviderCache:
    """
    In-memory provider response cache.
    """

    def __init__(
        self,
        default_ttl: float = 300.0,
    ) -> None:

        self.default_ttl = default_ttl

        self._cache: Dict[
            str,
            CacheEntry,
        ] = {}


    def _create_key(
        self,
        provider: str,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:

        raw = (
            f"{provider}:"
            f"{model}:"
            f"{prompt}"
        )

        return hashlib.sha256(
            raw.encode()
        ).hexdigest()


    def get(
        self,
        provider: str,
        prompt: str,
        model: Optional[str] = None,
    ) -> Optional[Any]:

        key = self._create_key(
            provider,
            prompt,
            model,
        )

        entry = self._cache.get(
            key
        )

        if not entry:
            return None


        expired = (
            time.time()
            -
            entry.created_at
            >
            entry.ttl
        )

        if expired:
            self._cache.pop(
                key,
                None,
            )

            return None


        return entry.value


    def set(
        self,
        provider: str,
        prompt: str,
        value: Any,
        model: Optional[str] = None,
        ttl: Optional[float] = None,
    ) -> None:

        key = self._create_key(
            provider,
            prompt,
            model,
        )

        self._cache[key] = CacheEntry(
            value=value,
            created_at=time.time(),
            ttl=(
                ttl
                if ttl is not None
                else self.default_ttl
            ),
        )


    def clear(
        self,
    ) -> None:

        self._cache.clear()


    def size(
        self,
    ) -> int:

        return len(
            self._cache
        )


provider_cache = ProviderCache()


__all__ = [
    "ProviderCache",
    "provider_cache",
]