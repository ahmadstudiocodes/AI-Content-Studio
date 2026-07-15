from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import json


@dataclass
class ResearchSource:
    """
    A research source.
    """

    title: str
    url: str
    source: str = ""
    published_at: str = ""
    credibility: float = 0.0


@dataclass
class ResearchStatistic:
    """
    Statistical information extracted from research.
    """

    value: str
    description: str
    source: str = ""


@dataclass
class ResearchQuote:
    """
    Quote extracted from research.
    """

    text: str
    author: str = ""
    source: str = ""


@dataclass
class ResearchPackage:
    """
    Final research package produced by ResearchAgent.
    """

    topic: str

    summary: str = ""

    key_points: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)

    sources: List[ResearchSource] = field(default_factory=list)

    statistics: List[ResearchStatistic] = field(default_factory=list)

    quotes: List[ResearchQuote] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(
        self,
        indent: int = 2
    ) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any]
    ):

        return cls(
            topic=data.get("topic", ""),
            summary=data.get("summary", ""),
            key_points=data.get("key_points", []),
            keywords=data.get("keywords", []),
            sources=[
                ResearchSource(**s)
                for s in data.get("sources", [])
            ],
            statistics=[
                ResearchStatistic(**s)
                for s in data.get("statistics", [])
            ],
            quotes=[
                ResearchQuote(**q)
                for q in data.get("quotes", [])
            ],
            metadata=data.get("metadata", {})
        )