import json
import re


class OutputCleaner:

    @staticmethod
    def clean(output):

        # ----------------------------------
        # Dictionary
        # ----------------------------------

        if isinstance(output, dict):

            return json.dumps(

                output,

                ensure_ascii=False,

                indent=2

            )

        # ----------------------------------
        # List / Tuple
        # ----------------------------------

        if isinstance(

            output,

            (list, tuple)

        ):

            return json.dumps(

                output,

                ensure_ascii=False,

                indent=2

            )

        # ----------------------------------
        # Other Objects
        # ----------------------------------

        if not isinstance(

            output,

            str

        ):

            output = str(output)

        # ----------------------------------
        # Remove Markdown Blocks
        # ----------------------------------

        output = re.sub(

            r"```.*?```",

            "",

            output,

            flags=re.DOTALL

        )

        # ----------------------------------
        # Remove Extra Empty Lines
        # ----------------------------------

        output = re.sub(

            r"\n\s*\n\s*\n+",

            "\n\n",

            output

        )

        return output.strip()