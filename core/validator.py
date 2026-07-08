import re


class Validator:
    """
    Validator for Arman StudioOS

    Validates LLM outputs before they are returned
    to the user.
    """

    def __init__(self):

        self.forbidden_patterns = [

            r"<think>",
            r"</think>",
            r"<thinking>",
            r"</thinking>",

            r"Thinking:",
            r"Reasoning:",
            r"Internal reasoning",
            r"Chain of Thought",
            r"analysis:",
            r"Let's think",
            r"I will think",

        ]

    def validate(
        self,
        output: str,
        task: str = "",
        topic: str = ""
    ):

        errors = []

        retry = False

        reason = "VALID"

        if output is None:

            return {
                "valid": False,
                "retry": True,
                "reason": "EMPTY_OUTPUT",
                "errors": [
                    "Output is None."
                ]
            }

        output = str(output)

        if output.strip() == "":

            return {
                "valid": False,
                "retry": True,
                "reason": "EMPTY_OUTPUT",
                "errors": [
                    "Output is empty."
                ]
            }

        for pattern in self.forbidden_patterns:

            if re.search(
                pattern,
                output,
                flags=re.IGNORECASE
            ):

                errors.append(
                    f"Forbidden pattern detected: {pattern}"
                )

        if errors:

            retry = True

            reason = "FORBIDDEN_PATTERN"

        if topic:

            topic_words = [

                w.lower()

                for w in topic.split()

                if len(w) > 2

            ]

            if topic_words:

                found = False

                lower_output = output.lower()

                for word in topic_words:

                    if word in lower_output:

                        found = True

                        break

                if not found:

                    errors.append(
                        "Topic not detected in output."
                    )

                    if not retry:

                        retry = True
                        reason = "TOPIC_MISSING"

        if len(output.strip()) < 5:

            errors.append(
                "Output too short."
            )

            if not retry:

                retry = True
                reason = "OUTPUT_TOO_SHORT"

        return {

            "valid": len(errors) == 0,

            "retry": retry,

            "reason": reason,

            "errors": errors

        }