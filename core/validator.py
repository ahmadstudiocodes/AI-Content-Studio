import re


class Validator:
    """
    Arman StudioOS Output Validator

    Checks output health only.
    Content quality will be handled
    by Quality Evaluator later.
    """



    def __init__(self):


        self.forbidden_patterns = [


            # Qwen / LLM thinking tags

            r"<think>",

            r"</think>",

            r"<thinking>",

            r"</thinking>",


            # Analysis leaks

            r"Thinking:",

            r"Reasoning:",

            r"Internal reasoning",

            r"Chain of Thought",

            r"analysis:",

            r"</analysis>",


            # Common model leaks

            r"Let's think",

            r"I will think",

            r"I need to analyze",

            r"My reasoning is",

            r"من فکر می‌کنم",

            r"تحلیل داخلی",

            r"فرآیند فکر کردن",


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



        # -----------------------------
        # None
        # -----------------------------

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



        # -----------------------------
        # Empty
        # -----------------------------


        if not output.strip():

            return {

                "valid": False,

                "retry": True,

                "reason": "EMPTY_OUTPUT",

                "errors": [

                    "Output is empty."

                ]

            }



        # -----------------------------
        # Forbidden patterns
        # -----------------------------


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



        # -----------------------------
        # Minimum length
        # -----------------------------


        if len(output.strip()) < 20:


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



validator = Validator()