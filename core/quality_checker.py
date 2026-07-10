import re

from core.quality_rules import QualityRules


class QualityChecker:
    """
    Arman StudioOS Quality Checker

    نسخه 2

    بررسی کیفیت خروجی بر اساس
    قوانین اختصاصی هر Agent
    """

    OLD_KEYWORDS = [

        "v-ray 2.4",
        "vray 2.4",
        "vray2.4",
        "3ds max 2014",
        "3ds max 2016"

    ]

    REPETITION_THRESHOLD = 4

    GARBAGE = [

        "؟؟؟",
        "لورم",
        "xxx",
        "... ...",
        "test test"

    ]

    def evaluate(self, output, command):

        text = str(output)

        lower = text.lower()

        errors = []

        score = 100

        # -----------------------------------
        # Agent Rules
        # -----------------------------------

        agent = ""

        if command.intent:

            agent = command.intent.domain

        rules = QualityRules.get(agent)

        # -----------------------------------
        # Minimum Length
        # -----------------------------------

        if len(text) < rules["min_length"]:

            errors.append(

                f"Output shorter than {rules['min_length']} chars."

            )

            score -= 20

        # -----------------------------------
        # Required Sections
        # -----------------------------------

        missing = []

        for section in rules["required"]:

            if section.lower() not in lower:

                missing.append(section)

        if missing:

            errors.append(

                "Missing sections: "

                + ", ".join(missing)

            )

            score -= 25

        # -----------------------------------
        # Old Content
        # -----------------------------------

        for keyword in self.OLD_KEYWORDS:

            if keyword in lower:

                errors.append(

                    f"Outdated content: {keyword}"

                )

                score -= 20

        # -----------------------------------
        # Word Repetition
        # -----------------------------------

        words = re.findall(

            r"\w+",

            lower

        )

        counter = {}

        for word in words:

            if len(word) <= 2:

                continue

            counter[word] = counter.get(word, 0) + 1

        repeated = [

            word

            for word, count in counter.items()

            if count >= self.REPETITION_THRESHOLD

        ]

        if repeated:

            errors.append(

                "Repeated words: "

                + ", ".join(repeated[:10])

            )

            score -= 15

        # -----------------------------------
        # Garbage Detection
        # -----------------------------------

        for item in self.GARBAGE:

            if item.lower() in lower:

                errors.append(

                    f"Garbage text: {item}"

                )

                score -= 20

        # -----------------------------------
        # Final Score
        # -----------------------------------

        score = max(score, 0)

        passed = (

            score >= 70

            and len(errors) == 0

        )

        return {

            "passed": passed,

            "score": score,

            "errors": errors

        }


quality_checker = QualityChecker()