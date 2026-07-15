import re

from core.quality_rules import QualityRules


class QualityChecker:
    """
    Arman StudioOS Quality Checker

    Validates output structure
    according to Agent rules.
    """

    OLD_KEYWORDS = [

        "v-ray 2.4",
        "vray 2.4",
        "vray2.4",
        "3ds max 2014",
        "3ds max 2016"

    ]

    REPETITION_THRESHOLD = 5

    GARBAGE = [

        "؟؟؟",
        "لورم",
        "xxx",
        "... ...",
        "test test"

    ]

    def evaluate(
        self,
        output,
        task=""
    ):

        text = str(output or "")
        lower = text.lower()

        score = 100
        errors = []

        # ---------------------------------
        # Empty Output
        # ---------------------------------

        if not text.strip():

            return {

                "valid": False,
                "score": 0,
                "errors": [
                    "EMPTY_OUTPUT"
                ]

            }

        # ---------------------------------
        # Load Rules
        # ---------------------------------

        rules = QualityRules.RULES.get(
            task,
            {}
        )

        if not rules:

            return {

                "valid": True,
                "score": score,
                "errors": []

            }

        # ---------------------------------
        # Length
        # ---------------------------------

        minimum = rules.get(
            "min_length",
            0
        )

        if len(text) < minimum:

            score -= 20

            errors.append(
                f"Output shorter than {minimum} chars."
            )

        # ---------------------------------
        # Required Sections
        # ---------------------------------

        required = rules.get(
            "required",
            {}
        )

        missing = []

        for section, keywords in required.items():

            found = False

            for keyword in keywords:

                if keyword.lower() in lower:

                    found = True
                    break

            if not found:

                missing.append(
                    section
                )

        if missing:

            score -= 25

            errors.append(
                "Missing sections: "
                + ", ".join(missing)
            )

        # ---------------------------------
        # Old Content
        # ---------------------------------

        for keyword in self.OLD_KEYWORDS:

            if keyword in lower:

                score -= 15

                errors.append(
                    f"Outdated content: {keyword}"
                )

        # ---------------------------------
        # Repetition
        # ---------------------------------

        words = re.findall(
            r"\w+",
            lower
        )

        counter = {}

        for word in words:

            if len(word) <= 2:
                continue

            counter[word] = counter.get(
                word,
                0
            ) + 1

        repeated = [

            word

            for word, count in counter.items()

            if count >= self.REPETITION_THRESHOLD

        ]

        if repeated:

            score -= 10

            errors.append(
                "Repeated words: "
                + ", ".join(repeated[:10])
            )

        # ---------------------------------
        # Garbage
        # ---------------------------------

        for item in self.GARBAGE:

            if item.lower() in lower:

                score -= 20

                errors.append(
                    f"Garbage text: {item}"
                )

        score = max(
            score,
            0
        )

        return {

            "valid": score >= 70,
            "score": score,
            "errors": errors

        }


quality_checker = QualityChecker()