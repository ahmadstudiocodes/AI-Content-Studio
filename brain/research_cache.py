from typing import Dict, Optional

from models.research_package import ResearchPackage


class ResearchCache:
    """
    Arman StudioOS Research Cache

    Stores research results to avoid
    repeating the same research.
    """

    def __init__(self):

        self._cache: Dict[str, ResearchPackage] = {}

    def has(
        self,
        topic: str
    ) -> bool:

        return topic in self._cache

    def get(
        self,
        topic: str
    ) -> Optional[ResearchPackage]:

        return self._cache.get(topic)

    def save(
        self,
        package: ResearchPackage
    ) -> None:

        self._cache[package.topic] = package

    def clear(self) -> None:

        self._cache.clear()


research_cache = ResearchCache()