import json

from brain.task_router import task_router
from brain.executive_memory import executive_memory


class WorkflowExecutor:

    """
    Arman Workflow Executor

    ExecutionPlan
          ↓
    Execute Tasks
          ↓
    Collect Results
          ↓
    Return Workflow Result
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

        for task in plan.steps:

            executive_memory.set_step(
                task.name
            )

            task.status = "running"

            try:

                result = task_router.route(
                    task,
                    command
                )

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

                "status": task.status,

                "result": result

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

                "tasks": results

            },

            indent=2,

            ensure_ascii=False

        )


workflow_executor = WorkflowExecutor()