import re


class ContextCompressor:

    """
    Smart Context Compressor

    Compresses previous Agent outputs
    based on the next target Agent.
    """

    DEFAULT_LIMIT = 1200

    TARGET_SECTIONS = {

        "course": [
            "Course Title",
            "Target Audience",
            "Learning Objectives",
            "Prerequisites",
            "Final Project",
            "Expected Skills"
        ],

        "script": [
            "Course Title",
            "Target Audience",
            "Learning Objectives",
            "Expected Skills"
        ],

        "thumbnail": [
            "Video Title",
            "Opening Hook",
            "Main Sections",
            "Thumbnail Concept"
        ],

        "publish": [
            "SEO Title",
            "SEO Description",
            "YouTube Tags",
            "Hashtags",
            "Pinned Comment"
        ]
    }

    TARGET_LIMITS = {

        "course": 1400,
        "script": 1000,
        "thumbnail": 700,
        "publish": 900

    }

    # -------------------------------------

    def compress(
        self,
        text,
        target="general"
    ):

        if not isinstance(text, str):
            return ""

        sections = self.TARGET_SECTIONS.get(
            target,
            []
        )

        output = []

        for section in sections:

            content = self.extract_section(
                text,
                section
            )

            if content:

                if len(content) > 350:
                    content = content[:350]

                output.append(content)

        if output:

            compressed = "\n\n".join(output)

            limit = self.TARGET_LIMITS.get(
                target,
                self.DEFAULT_LIMIT
            )

            return compressed[:limit]

        return text[:600]

    # -------------------------------------

    def extract_section(
        self,
        text,
        section
    ):

        pattern = rf"{re.escape(section)}.*?(?=\n#|\Z)"

        match = re.search(
            pattern,
            text,
            flags=re.S
        )

        if match:
            return match.group(0).strip()

        return None


context_compressor = ContextCompressor()