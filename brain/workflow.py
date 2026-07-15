import json
import time

from brain.task_router import task_router
from brain.executive_memory import executive_memory
from brain.context_compressor import context_compressor
from brain.memory_injector import memory_injector
from brain.workflow_history import workflow_history
from brain.memory_cleanup import memory_cleanup


class WorkflowExecutor:

    """
    Arman StudioOS Workflow Executor

    Executes multi-agent workflows
    and maintains compressed context
    between agents.
    """

    MAX_CONTEXT_LENGTH = 800

    def execute(
        self,
        plan,
        command
    ):

        executive_memory.set_workflow(
            plan.goal
        )

        workflow_history.start(
            workflow_id=str(int(time.time())),
            goal=plan.goal
        )

        plan.status = "running"

        results = []

        workflow_outputs = {}

        context = ""

        if not getattr(
            plan,
            "steps",
            None
        ):

            workflow_history.finish()

            plan.status = "completed"

            return self.build_output(
                plan,
                results,
                workflow_outputs
            )

        for task in plan.steps:

            executive_memory.set_step(
                task.name
            )

            task.status = "running"

            start_time = time.time()

            try:

                injected_context = memory_injector.inject(
                    task=command,
                    compressed_context=context
                )

                agent_result = task_router.route(
                    task,
                    command,
                    injected_context
                )

                elapsed = round(
                    time.time() - start_time,
                    2
                )

                target = self.detect_context_target(
                    task.name
                )

                if isinstance(agent_result, dict):

                    text = (
                        agent_result.get("output")
                        or str(agent_result)
                    )

                else:

                    text = str(agent_result)

                compressed_context = (
                    context_compressor.compress(
                        text,
                        target
                    )
                    or ""
                )

                compressed_context = compressed_context[:600]

                context = compressed_context

                workflow_outputs[
                    task.name
                ] = {

                    "summary": compressed_context,

                    "result": agent_result

                }

                workflow_history.add_step(
                    agent=task.name,
                    task=command,
                    output=agent_result,
                    duration=elapsed,
                    status="success"
                )

                executive_memory.set(
                    "last_output",
                    agent_result
                )

                executive_memory.set(
                    "workflow_summary",
                    compressed_context
                )

                task.status = "completed"

                task.result = agent_result

                results.append(

                    {

                        "task": task.name,

                        "status": "completed",

                        "time": elapsed

                    }

                )

            except Exception as e:

                elapsed = round(
                    time.time() - start_time,
                    2
                )

                workflow_history.add_step(
                    agent=task.name,
                    task=command,
                    output=str(e),
                    duration=elapsed,
                    status="failed"
                )

                task.status = "failed"

                task.result = str(e)

                results.append(

                    {

                        "task": task.name,

                        "status": "failed",

                        "time": elapsed,

                        "error": str(e)

                    }

                )

                plan.status = "failed"

                break

        if plan.status != "failed":

            plan.complete()

        workflow_history.finish()

        memory_cleanup.cleanup()

        executive_memory.set_step(
            "Finished"
        )

        return self.build_output(
            plan,
            results,
            workflow_outputs
        )

    # ==================================================

    def detect_context_target(
        self,
        task_name
    ):

        text = task_name.lower()

        if "thumbnail" in text:
            return "thumbnail"

        if "script" in text:
            return "script"

        if (
            "course" in text
            or
            "lesson" in text
        ):
            return "course"

        if (
            "publish" in text
            or
            "seo" in text
        ):
            return "publish"

        if "research" in text:
            return "research"

        return "general"

    # ==================================================

    def build_output(
        self,
        plan,
        results,
        outputs
    ):

        return json.dumps(

            {

                "workflow": plan.goal,

                "status": plan.status,

                "tasks": results,

                "outputs": outputs

            },

            indent=2,

            ensure_ascii=False,

            default=str

        )


workflow_executor = WorkflowExecutor()