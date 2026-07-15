import re
from collections import Counter

from core.quality_rules import QualityRules


class QualityEvaluator:
    """
    Agent-aware Quality Evaluator

    Checks Agent outputs against QualityRules.
    """

    MIN_SCORE = 70

    TECHNICAL_TERMS = [

        "v-ray",
        "vray",
        "3ds",
        "max",
        "3ds max",
        "رندر",
        "مدلسازی",
        "معماری",
        "ساختمان",
        "cgi",
        "visualization",
        "ویژوال",
        "نورپردازی",
        "architecture",
        "render",
        "rendering"

    ]


    def normalize_words(
        self,
        text
    ):

        text = text.replace(
            "‌",
            " "
        )

        text = text.replace(
            "ي",
            "ی"
        )

        text = text.replace(
            "ك",
            "ک"
        )


        replacements = {

            "مدل سازی": "مدلسازی",
            "مدل‌سازی": "مدلسازی",

            "رندرینگ": "رندر",
            "رندرهای": "رندر",
            "رندرها": "رندر",

            "پروژه های": "پروژه",
            "پروژه‌های": "پروژه",
            "پروژهها": "پروژه",

            "ساختمانهای": "ساختمان",
            "ساختمان‌های": "ساختمان"

        }


        for old, new in replacements.items():

            text = text.replace(
                old,
                new
            )


        return text



    def extract_keywords(
        self,
        text
    ):

        text = re.sub(

            r"[^a-zA-Z0-9\u0600-\u06FF\s]",

            " ",

            text.lower()

        )


        text = self.normalize_words(
            text
        )


        stop_words = [

            "the",
            "for",
            "and",
            "with",
            "create",
            "content",
            "strategy",
            "advanced",
            "professional",
            "ایجاد",
            "ساخت",
            "حرفه‌ای",
            "حرفه ای"

        ]


        words = [

            word.strip()

            for word in text.split()

            if len(word.strip()) > 2

            and word.strip() not in stop_words

        ]


        return words



    def evaluate(
        self,
        output: str,
        task: str = "",
        topic: str = ""
    ):

        output = str(output or "")

        score = 100

        issues = []


        if not output.strip():

            return {

                "score": 0,

                "passed": False,

                "retry": True,

                "issues": [
                    "Empty output."
                ],

                "task": task,

                "topic": topic

            }


        normalized_output = re.sub(

            r"[^a-zA-Z0-9\u0600-\u06FF\s]",

            " ",

            output.lower()

        )


        normalized_output = self.normalize_words(
            normalized_output
        )



        rules = QualityRules.RULES.get(
            task,
            {}
        )


        min_length = rules.get(
            "min_length",
            250
        )



        if len(output) < min_length:

            score -= 20

            issues.append(
                f"Output too short. Minimum length: {min_length}"
            )



        persian_chars = len(

            re.findall(
                r"[\u0600-\u06FF]",
                output
            )

        )


        english_chars = len(

            re.findall(
                r"[A-Za-z]",
                output
            )

        )


        if task not in [

            "thumbnail",

            "image_prompt"

        ]:


            if english_chars > persian_chars:

                score -= 15

                issues.append(
                    "Output language mismatch."
                )



        words = normalized_output.split()


        filtered_words = [

            word

            for word in words

            if word not in self.TECHNICAL_TERMS

        ]


        if len(filtered_words) > 50:


            counter = Counter(filtered_words)


            repeated_words = [

                word

                for word, count in counter.items()

                if count >= 6

            ]


            if len(repeated_words) >= 5:

                score -= 10

                issues.append(
                    "High word repetition."
                )



        required = rules.get(
            "required",
            {}
        )


        for section, alternatives in required.items():

            found = False


            for keyword in alternatives:


                keyword = self.normalize_words(
                    keyword.lower()
                )


                if keyword in normalized_output:

                    found = True

                    break


            if not found:

                score -= 5

                issues.append(
                    f"Missing section: {section}"
                )



        # ---------------------------------
        # Improved Topic Detection
        # ---------------------------------

        if topic:

            topic_keywords = self.extract_keywords(
                topic
            )


            detected = 0


            for keyword in topic_keywords:

                if keyword in normalized_output:

                    detected += 1



            if topic_keywords and detected == 0:

                score -= 5

                issues.append(
                    "Topic not detected."
                )



        score = max(
            0,
            min(
                score,
                100
            )
        )



        critical_issues = any(

            issue.startswith("Missing section")

            or issue == "Topic not detected."

            for issue in issues

        )



        retry = (

            score < self.MIN_SCORE

            or critical_issues

        )



        return {

            "score": score,

            "passed": not retry,

            "retry": retry,

            "issues": issues,

            "task": task,

            "topic": topic

        }



quality_evaluator = QualityEvaluator()