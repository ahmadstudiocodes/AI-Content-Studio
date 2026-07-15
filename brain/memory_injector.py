# brain/memory_injector.py

from copy import deepcopy

from brain.executive_memory import executive_memory
from brain.context_compressor import context_compressor


class MemoryInjector:
    """
    Arman StudioOS Memory Injector

    Builds the final context that is sent to every Agent.

    Responsibilities
    ----------------
    • Read Executive Memory
    • Extract only relevant information
    • Merge workflow summary
    • Inject previous outputs
    • Preserve constraints
    • Keep context size under limits
    """

    MAX_HISTORY = 5
    MAX_CONTEXT_LENGTH = 2000

    def inject(
        self,
        task,
        memory=None,
        compressed_context=None
    ):
        """
        Main entry point.

        Returns a clean context package
        ready for any Agent.
        """

        if memory is None:
            memory = executive_memory.snapshot()

        relevant_memory = self.extract_relevant_memory(
            task,
            memory
        )

        workflow_summary = compressed_context

        if workflow_summary is None:
            workflow_summary = context_compressor.compress(
                memory
            )

        context = {
            "task": task,
            "goal": memory.get("goal"),
            "workflow_summary": workflow_summary,
            "previous_output": memory.get("last_output"),
            "important_memory": relevant_memory,
            "constraints": deepcopy(
                memory.get("constraints", [])
            ),
            "history": deepcopy(
                memory.get("history", [])
            )[-self.MAX_HISTORY:]
        }

        return self.clean_context(context)

    def build_prompt(
        self,
        context
    ):
        """
        Converts injected context into a prompt string.

        Useful for LLM based Agents.
        """

        lines = []

        if context.get("goal"):
            lines.append(
                f"GOAL:\n{context['goal']}\n"
            )

        if context.get("workflow_summary"):
            lines.append(
                "WORKFLOW SUMMARY:\n"
                f"{context['workflow_summary']}\n"
            )

        if context.get("important_memory"):
            lines.append(
                "IMPORTANT MEMORY:\n"
                f"{context['important_memory']}\n"
            )

        if context.get("constraints"):
            lines.append("CONSTRAINTS:")

            for item in context["constraints"]:
                lines.append(f"- {item}")

            lines.append("")

        if context.get("previous_output"):
            lines.append(
                "PREVIOUS OUTPUT:\n"
                f"{context['previous_output']}\n"
            )

        if context.get("history"):
            lines.append("RECENT HISTORY:")

            for step in context["history"]:
                lines.append(f"- {step}")

            lines.append("")

        lines.append("CURRENT TASK:")
        lines.append(str(context["task"]))

        return "\n".join(lines)

    def extract_relevant_memory(
        self,
        task,
        memory
    ):
        """
        Extract only memory relevant to the current task.

        Current implementation keeps important
        workflow information.

        Can later be upgraded with semantic search.
        """

        relevant = {}

        keys = [
            "project",
            "goal",
            "decisions",
            "important_notes",
            "artifacts",
            "variables"
        ]

        for key in keys:
            if key in memory:
                relevant[key] = deepcopy(memory[key])

        return relevant

    def clean_context(
        self,
        context
    ):
        """
        Remove empty fields and trim long values.
        """

        cleaned = {}

        for key, value in context.items():

            if value is None:
                continue

            if value == "":
                continue

            if value == []:
                continue

            if value == {}:
                continue

            if isinstance(value, str):
                value = value.strip()

                if len(value) > self.MAX_CONTEXT_LENGTH:
                    value = (
                        value[: self.MAX_CONTEXT_LENGTH]
                        + "\n..."
                    )

            cleaned[key] = value

        return cleaned


memory_injector = MemoryInjector()