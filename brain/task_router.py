from brain.executive_memory import executive_memory
from brain.context_compressor import context_compressor

from core.dispatcher import dispatcher


class TaskRouter:

    """
    Arman StudioOS Workflow Task Router

    Flow:

        Workflow
            ↓
        Task Router
            ↓
        Context Compression
            ↓
        Internal Command
            ↓
        Dispatcher
            ↓
        Agent Selection
            ↓
        Agent Execution
            ↓
        Output
    """

    def route(
        self,
        task,
        original_command,
        context=None
    ):

        task_name = task.name

        executive_memory.add_task(task)

        command = self.create_command(
            task_name,
            original_command,
            context
        )

        agent = dispatcher.route(command)

        if not agent:

            executive_memory.fail_task(task)

            raise Exception(
                f"No agent found for task: {task_name}"
            )

        payload = command.payload or command.raw

        self.debug_input(
            task,
            command,
            agent,
            payload
        )

        try:

            result = agent.run(payload)

        except Exception as e:

            executive_memory.fail_task(task)

            print(
                f"\nAgent Execution Failed: {agent.name}"
            )

            raise e

        self.debug_output(result)

        if not result:

            executive_memory.fail_task(task)

            raise Exception(
                f"{agent.name} returned empty output."
            )

        executive_memory.complete_task(task)

        return result

    # =====================================================
    # Debug Helpers
    # =====================================================

    def debug_input(
        self,
        task,
        command,
        agent,
        payload
    ):

        payload = str(payload)

        print("\n" + "=" * 80)
        print("AGENT EXECUTION DEBUG")
        print("=" * 80)

        print(f"Task Name      : {task.name}")
        print(f"Target         : {command.target}")
        print(f"Action         : {command.action}")
        print(f"Selected Agent : {agent.name}")
        print(f"Payload Length : {len(payload)} characters")

        print("\n--------------- PAYLOAD START ---------------\n")

        if len(payload) > 3000:

            print(payload[:3000])

            print("\n... PAYLOAD TRUNCATED ...")

        else:

            print(payload)

        print("\n---------------- PAYLOAD END ----------------")
        print("=" * 80)

    def debug_output(
        self,
        result
    ):

        print("\n" + "=" * 80)
        print("AGENT RESULT DEBUG")
        print("=" * 80)

        if result:

            result = str(result)

            print(
                f"Result Length : {len(result)} characters"
            )

            if len(result) > 2000:

                print(result[:2000])

                print("\n... RESULT TRUNCATED ...")

            else:

                print(result)

        else:

            print("EMPTY RESULT")

        print("=" * 80 + "\n")

    # =====================================================
    # Internal Command Builder
    # =====================================================

    def create_command(
        self,
        task_name,
        original_command,
        context=None
    ):

        target = self.detect_target(task_name)

        domain = getattr(
            getattr(
                original_command,
                "intent",
                None
            ),
            "domain",
            "general"
        )

        class Intent:
            pass

        intent = Intent()
        intent.domain = domain

        class InternalCommand:
            pass

        cmd = InternalCommand()

        cmd.raw = task_name

        cmd.target = target

        lower = task_name.lower()

        if "lesson" in lower:
            cmd.action = "lesson_plan"

        elif "curriculum" in lower:
            cmd.action = "curriculum"

        elif "course" in lower:
            cmd.action = "course_structure"

        elif "research" in lower:
            cmd.action = "research"

        elif "thumbnail" in lower:
            cmd.action = "thumbnail"

        elif "script" in lower:
            cmd.action = "script"

        elif "publish" in lower:
            cmd.action = "publish"

        else:
            cmd.action = lower

        original_payload = getattr(
            original_command,
            "payload",
            ""
        )

        if context:

            compressed = context_compressor.compress(
                context,
                target
            )

            compressed = str(compressed)[:1200]

            cmd.payload = f"""
Task:
{cmd.action}

User Request:
{original_payload[:500]}

Previous Result:
{compressed}

Instructions:

- Generate ONLY the output required for this task.
- Do NOT repeat previous sections.
- Continue from previous result.
"""

        else:

            cmd.payload = original_payload[:800]

        cmd.intent = intent

        return cmd

    # =====================================================
    # Target Detection
    # =====================================================

    def detect_target(
        self,
        task_name
    ):

        text = task_name.lower()

        if (
            "youtube" in text
            or "content" in text
            or "video idea" in text
            or "video strategy" in text
            or "analyze topic" in text
        ):

            return "youtube"

        if "thumbnail" in text:

            return "thumbnail"

        if "script" in text:

            return "script"

        if (
            "lesson" in text
            or "curriculum" in text
        ):

            return "course"

        if "course" in text:

            return "course"

        if "research" in text:

            return "research"

        if (
            "publish" in text
            or "seo" in text
        ):

            return "publish"

        if (
            "architecture" in text
            or "system design" in text
            or "software" in text
        ):

            return "architecture"

        return "general"


task_router = TaskRouter()