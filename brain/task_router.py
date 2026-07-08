from core.dispatcher import dispatcher
from brain.executive_memory import executive_memory


class TaskRouter:

    """
    Workflow Task Router

    Task
        ↓
    Internal Command
        ↓
    Dispatcher
        ↓
    Agent
    """

    def route(
        self,
        task,
        original_command
    ):

        task_name = task.name

        print(
            f"[TASK ROUTER] {task_name}"
        )

        executive_memory.add_task(
            task
        )

        command = self.create_command(
            task_name,
            original_command
        )

        result = dispatcher.route(
            command
        )

        executive_memory.complete_task(
            task
        )

        return result

    # ---------------------------------

    def create_command(
        self,
        task_name,
        original_command
    ):

        target = self.detect_target(
            task_name
        )

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

        cmd.payload = original_command.payload

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

        return "unknown"


task_router = TaskRouter()