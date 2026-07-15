import json
import re


class OutputCleaner:
    """
    Central LLM Output Cleaner

    Cleans responses from all agents
    before validation and user output.
    """

    @staticmethod
    def clean(output):

        # ----------------------------------
        # Dictionary
        # ----------------------------------

        if isinstance(output, dict):

            output = json.dumps(

                output,

                ensure_ascii=False,

                indent=2

            )

        # ----------------------------------
        # List / Tuple
        # ----------------------------------

        elif isinstance(

            output,

            (list, tuple)

        ):

            output = json.dumps(

                output,

                ensure_ascii=False,

                indent=2

            )

        # ----------------------------------
        # Other Objects
        # ----------------------------------

        elif not isinstance(output, str):

            output = str(output)

        # ----------------------------------
        # Remove Qwen Thinking
        # ----------------------------------

        output = re.sub(

            r"<think>.*?</think>",

            "",

            output,

            flags=re.DOTALL

        )

        output = output.replace(

            "<think>",

            ""

        )

        output = output.replace(

            "</think>",

            ""

        )

        # ----------------------------------
        # Remove Markdown Fences Only
        # ----------------------------------

        output = re.sub(

            r"```[a-zA-Z0-9_-]*\n?",

            "",

            output

        )

        output = output.replace(

            "```",

            ""

        )

        # ----------------------------------
        # Remove common LLM artifacts
        # ----------------------------------

        forbidden_patterns = [

            "I need to think",

            "Let's analyze",

            "I will reason",

            "در حال فکر کردن",

            "تحلیل داخلی"

        ]

        for pattern in forbidden_patterns:

            output = output.replace(

                pattern,

                ""

            )

        # ----------------------------------
        # Fix spacing
        # ----------------------------------

        output = re.sub(

            r"\n{3,}",

            "\n\n",

            output

        )

        output = re.sub(

            r"[ \t]{2,}",

            " ",

            output

        )

        return output.strip()