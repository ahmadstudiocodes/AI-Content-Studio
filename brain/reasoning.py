from brain.types import (
    ReasoningResult,
    Complexity,
    ExecutionMode
)


class ReasoningEngine:

    """
    Brain Reasoning Engine

    Responsible for deciding how Arman
    should execute a user request.
    """

    COMPLEX_KEYWORDS = [

        "course",
        "series",
        "book",
        "project",
        "workflow",
        "multiple",
        "multi",
        "campaign",
        "pipeline",
        "system"

    ]

    def think(self, command):

        # --------------------------------
        # Build Clean Goal
        # --------------------------------

        parts = []

        if command.action:
            parts.append(command.action)

        if command.target:
            parts.append(command.target)

        payload = command.payload.strip()

        if (
            command.target
            and payload.lower().startswith(
                command.target.lower()
            )
        ):

            payload = payload[
                len(command.target):
            ].strip()

        if payload:
            parts.append(payload)

        text = " ".join(parts).lower()

        # --------------------------------
        # Complexity Detection
        # --------------------------------

        is_complex = any(

            keyword in text

            for keyword in self.COMPLEX_KEYWORDS

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


reasoning = ReasoningEngine()