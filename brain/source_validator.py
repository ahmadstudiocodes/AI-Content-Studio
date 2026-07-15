from models.research_package import (
    ResearchPackage,
    ResearchSource
)


class SourceValidator:
    """
    Arman StudioOS Source Validator

    Validates research sources.
    """

    def __init__(self):

        self.minimum_credibility = 0.5

    def validate(
        self,
        package: ResearchPackage
    ) -> ResearchPackage:

        validated = []

        for source in package.sources:

            source.credibility = self.score(source)

            if source.credibility >= self.minimum_credibility:
                validated.append(source)

        package.sources = validated

        return package

    def score(
        self,
        source: ResearchSource
    ) -> float:
        """
        Calculate source credibility.
        """

        score = 0.5

        if source.url.startswith("https://"):
            score += 0.2

        if source.source:
            score += 0.2

        if source.published_at:
            score += 0.1

        return min(score, 1.0)


source_validator = SourceValidator()