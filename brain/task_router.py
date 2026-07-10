from core.dispatcher import dispatcher
from brain.executive_memory import executive_memory
from brain.context_compressor import context_compressor


class TaskRouter:

    """
    Workflow Task Router

    Workflow
        ↓
    Compress Context
        ↓
    Build Internal Command
        ↓
    Dispatcher
        ↓
    Agent
    """

    def route(
        self,
        task,
        original_command,
        context=None
    ):

        task_name = task.name

        print(
            f"[TASK ROUTER] {task_name}"
        )

        executive_memory.add_task(task)

        command = self.create_command(
            task_name,
            original_command,
            context
        )

        result = dispatcher.route(command)

        executive_memory.complete_task(task)

        return result

    # ---------------------------------

    def create_command(
        self,
        task_name,
        original_command,
        context=None
    ):

        target = self.detect_target(task_name)

        domain = getattr(
            original_command.intent,
            "domain",
            "general"
        )

        class Intent:
            pass

        intent = Intent()
        intent.domain = domain

        class Plan:

            def __init__(self):
                self.status = "idle"

            def complete(self):
                self.status = "completed"

        class InternalCommand:
            pass

        cmd = InternalCommand()

        cmd.raw = task_name
        cmd.action = task_name
        cmd.target = target

        # --------------------------
        # Smart Context Compression
        # --------------------------

        if context:

            compressed = context_compressor.compress(
                context,
                target
            )

            print(
                f"[CONTEXT] target={target} | size={len(compressed)} chars"
            )

            cmd.payload = f"""
Original User Request:

{original_command.payload[:800]}

Previous Agent Result:

{compressed}
"""

        else:

            print(
                "[CONTEXT] No previous context"
            )

            cmd.payload = original_command.payload[:800]

        cmd.intent = intent
        cmd.plan = Plan()

        return cmd

    # ---------------------------------

    def detect_target(
        self,
        task_name
    ):

        text = task_name.lower()

        if "thumbnail" in text:
            return "thumbnail"

        if "script" in text:
            return "script"

        if "lesson" in text:
            return "course"

        if "course" in text:
            return "course"

        if "research" in text:
            return "research"

        if "publish" in text:
            return "publish"

        return "general"


task_router = TaskRouter()