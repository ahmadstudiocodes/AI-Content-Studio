import re


class OutputGuard:
    """
    Central Output Cleaner and Validator

    Cleans LLM responses before returning
    to the user.
    """

    def clean(self, text):

        if not isinstance(text, str):

            return ""

        if not text.strip():

            return ""

        # -----------------------------
        # Remove Qwen thinking blocks
        # -----------------------------

        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL
        )

        text = text.replace(
            "<think>",
            ""
        )

        text = text.replace(
            "</think>",
            ""
        )

        # -----------------------------
        # Remove markdown noise
        # -----------------------------

        text = text.strip()

        # -----------------------------
        # Fix repeated spaces
        # -----------------------------

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        text = re.sub(
            r" {2,}",
            " ",
            text
        )

        return text.strip()

    def validate(self, text):

        if not isinstance(text, str):

            return {

                "valid": False,

                "reason": "EMPTY_OUTPUT"

            }

        text = text.strip()

        if not text:

            return {

                "valid": False,

                "reason": "EMPTY_OUTPUT"

            }

        if len(text) < 20:

            return {

                "valid": False,

                "reason": "OUTPUT_TOO_SHORT"

            }

        return {

            "valid": True,

            "reason": "OK"

        }

    def process(self, text):

        cleaned = self.clean(text)

        validation = self.validate(cleaned)

        return {

            "output": cleaned,

            "validation": validation

        }


output_guard = OutputGuard()