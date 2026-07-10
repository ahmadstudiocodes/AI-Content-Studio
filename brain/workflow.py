import json

from brain.task_router import task_router
from brain.executive_memory import executive_memory


class WorkflowExecutor:

    """
    Arman Workflow Executor
    """

    def execute(
        self,
        plan,
        command
    ):

        executive_memory.set_workflow(
            plan.goal
        )

        plan.status = "running"

        results = []

        # Context passed between agents
        context = None

        for task in plan.steps:

            executive_memory.set_step(
                task.name
            )

            task.status = "running"

            try:

                result = task_router.route(
                    task,
                    command,
                    context
                )

                # Save output for next Agent
                context = result

                task.status = "completed"

                task.result = result

            except Exception as e:

                task.status = "failed"

                task.result = str(e)

                results.append({

                    "task": task.name,

                    "status": "failed",

                    "error": str(e)

                })

                plan.status = "failed"

                break

            results.append({

                "task": task.name,

                "status": task.status

            })

        if plan.status != "failed":

            plan.complete()

        executive_memory.set_step(
            "Finished"
        )

        return json.dumps(

            {

                "workflow": plan.goal,

                "status": plan.status,

                "tasks": results,

                "final_result": context

            },

            indent=2,

            ensure_ascii=False

        )


workflow_executor = WorkflowExecutor()