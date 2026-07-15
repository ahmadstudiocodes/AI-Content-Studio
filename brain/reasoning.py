from brain.types import (
    ReasoningResult,
    Complexity,
    ExecutionMode
)


class ReasoningEngine:

    """
    Arman StudioOS Brain Reasoning Engine

    Decides execution strategy:

        User Command
              |
              ↓
        Complexity Analysis
              |
        ----------------
        |              |
      Direct       Workflow

    """


    COMPLEX_KEYWORDS = [

        "course",
        "series",
        "book",
        "project",
        "workflow",
        "campaign",
        "pipeline",

        "multiple",
        "multi step",
        "multi-step",

        "architecture",
        "system design",

        "generate all",
        "create plan",
        "complete strategy",

        "دوره",
        "سری",
        "پروژه",
        "کمپین",
        "فرایند",
        "روند"

    ]


    WORKFLOW_INDICATORS = [

        "then",
        "after",
        "next",
        "step",
        "مرحله",
        "بعد",
        "سپس"

    ]


    # ==================================================

    def think(
        self,
        command
    ):


        parts = []


        action = getattr(
            command,
            "action",
            ""
        )


        target = getattr(
            command,
            "target",
            ""
        )


        payload = getattr(
            command,
            "payload",
            ""
        )



        if action:

            parts.append(
                str(action)
            )



        if target:

            parts.append(
                str(target)
            )



        if payload:

            payload = str(payload).strip()



            if target and payload.lower().startswith(
                str(target).lower()
            ):

                payload = payload[
                    len(target):
                ].strip()



            parts.append(
                payload
            )



        text = self.normalize(
            " ".join(parts)
        )



        is_complex = self.detect_complexity(
            text
        )



        if is_complex:


            return ReasoningResult(

                goal=text,

                complexity=Complexity.COMPLEX,

                requires_memory=True,

                requires_planner=True,

                requires_workflow=True,

                execution=ExecutionMode.WORKFLOW

            )



        return ReasoningResult(

            goal=text,

            complexity=Complexity.SIMPLE,

            requires_memory=False,

            requires_planner=False,

            requires_workflow=False,

            execution=ExecutionMode.DIRECT

        )



    # ==================================================

    def detect_complexity(
        self,
        text
    ):


        keyword_match = any(

            keyword in text

            for keyword in self.COMPLEX_KEYWORDS

        )


        workflow_match = any(

            indicator in text

            for indicator in self.WORKFLOW_INDICATORS

        )


        return (
            keyword_match
            or workflow_match
        )



    # ==================================================

    def normalize(
        self,
        text
    ):


        text = text.lower()


        replacements = {

            "‌": "",
            "ي": "ی",
            "ك": "ک"

        }


        for old, new in replacements.items():

            text = text.replace(
                old,
                new
            )


        return text.strip()



reasoning = ReasoningEngine()