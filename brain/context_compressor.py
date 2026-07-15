import re


class ContextCompressor:

    """
    Arman StudioOS Smart Context Compressor

    Compresses previous agent outputs
    before passing context to next agents.
    """

    DEFAULT_LIMIT = 1000


    TARGET_LIMITS = {

        "course": 1200,
        "script": 900,
        "thumbnail": 700,
        "publish": 900,
        "youtube": 1000,
        "research": 1200,
        "architecture": 1000,
        "general": 800

    }


    TARGET_SECTIONS = {


        "course": [

            "Video Title",
            "Learning Objectives",
            "Main Content",
            "Final Project",
            "Expected Skills"

        ],


        "script": [

            "Video Title",
            "Opening Hook",
            "Introduction",
            "Main Content",
            "Call To Action",
            "Ending"

        ],


        "thumbnail": [

            "Video Title",
            "Opening Hook",
            "Thumbnail Concept",
            "Composition"

        ],


        "publish": [

            "SEO Title",
            "SEO Description",
            "YouTube Tags",
            "Hashtags",
            "Pinned Comment"

        ],


        "youtube": [

            "Video Title",
            "Hook",
            "Strategy",
            "Audience",
            "Structure"

        ]

    }


    # ==================================================

    def compress(
        self,
        text,
        target="general"
    ):


        if text is None:

            return ""


        if not isinstance(text, str):

            text = str(text)


        text = self.clean_text(text)


        if not text:

            return ""


        sections = self.TARGET_SECTIONS.get(
            target,
            []
        )


        collected = []


        for section in sections:

            extracted = self.extract_section(
                text,
                section
            )

            if extracted:

                collected.append(extracted)



        if not collected:

            collected = self.smart_fallback(
                text
            )


        compressed = self.remove_duplicates(
            "\n\n".join(collected)
        )


        limit = self.TARGET_LIMITS.get(
            target,
            self.DEFAULT_LIMIT
        )


        return compressed[:limit]



    # ==================================================

    def extract_section(
        self,
        text,
        section
    ):


        pattern = (

            rf"(?:^|\n)"
            rf"[#*\-\s]*"
            rf"{re.escape(section)}"
            rf"\s*:?\s*\n?"
            rf"(.*?)(?=\n[#*\-\s]*[A-Za-z\u0600-\u06FF ]+\s*:?\s*\n|\Z)"

        )


        match = re.search(
            pattern,
            text,
            flags=re.S | re.I
        )


        if not match:

            return None



        body = match.group(1).strip()


        if not body:

            return None



        body = body[:400]


        return (
            f"{section}\n{body}"
        )



    # ==================================================

    def smart_fallback(
        self,
        text
    ):


        lines = []


        blocked = {

            "copyright",
            "references",
            "منبع",
            "محدودیت",
            "کپی رایت"

        }



        for line in text.splitlines():


            line = line.strip()



            if not line:

                continue



            if any(

                word.lower() in line.lower()

                for word in blocked

            ):

                continue



            lines.append(line)



        return lines[:25]



    # ==================================================

    def remove_duplicates(
        self,
        text
    ):


        seen = set()

        output = []



        for line in text.splitlines():


            clean = line.strip()



            if not clean:

                continue



            key = clean.lower()



            if key in seen:

                continue



            seen.add(key)


            output.append(clean)



        return "\n".join(output)



    # ==================================================

    def clean_text(
        self,
        text
    ):


        text = text.strip()


        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )


        return text



context_compressor = ContextCompressor()