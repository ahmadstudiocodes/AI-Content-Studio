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

        """
        Normalize Persian variations
        for better quality detection.
        """


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

            "مدلسازی": "مدلسازی",


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





    def evaluate(
        self,
        output: str,
        task: str = "",
        topic: str = ""
    ):


        output = str(output or "")


        score = 100

        issues = []


        lower = output.lower()



        # ---------------------------------
        # Empty Output
        # ---------------------------------

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



        # ---------------------------------
        # Normalize Text
        # ---------------------------------

        normalized_output = re.sub(

            r"[^a-zA-Z0-9\u0600-\u06FF\s]",

            " ",

            lower

        )


        normalized_output = self.normalize_words(

            normalized_output

        )



        # ---------------------------------
        # Load Rules
        # ---------------------------------

        rules = QualityRules.RULES.get(

            task,

            {}

        )


        print(
            "DEBUG TASK:",
            task
        )


        print(
            "DEBUG RULES:",
            rules
        )



        min_length = rules.get(

            "min_length",

            250

        )



        # ---------------------------------
        # Length Check
        # ---------------------------------

        if len(output) < min_length:

            score -= 20


            issues.append(

                f"Output too short. Minimum length: {min_length}"

            )



        # ---------------------------------
        # Language Check
        # ---------------------------------

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



        # ---------------------------------
        # Smart Duplicate Detection
        # ---------------------------------

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



        # ---------------------------------
        # Required Sections
        # ---------------------------------

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
        # Topic Check
        # ---------------------------------

        if topic:


            normalized_topic = self.normalize_words(

                topic.lower()

            )


            if normalized_topic not in normalized_output:


                score -= 5


                issues.append(

                    "Topic not detected."

                )



        # ---------------------------------
        # Final Score
        # ---------------------------------

        score = max(

            0,

            min(

                score,

                100

            )

        )



        retry = score < self.MIN_SCORE



        return {

            "score": score,

            "passed": not retry,

            "retry": retry,

            "issues": issues,

            "task": task,

            "topic": topic

        }




quality_evaluator = QualityEvaluator()