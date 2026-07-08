from brain.reasoning import reasoning
from brain.planner import planner
from brain.debug import brain_debugger
from brain.executive_memory import executive_memory
from brain.workflow import workflow_executor

from core.dispatcher import dispatcher


class BrainController:

    """
    Arman Brain Controller

    Flow

    Command
        ↓
    Reasoning
        ↓
    Memory
        ↓
    Planner
        ↓
    Workflow / Dispatcher
        ↓
    Memory Update
    """

    def execute(
        self,
        command
    ):

        # --------------------------------
        # Reset Memory
        # --------------------------------

        executive_memory.reset()

        try:

            # --------------------------------
            # Step 1 : Reasoning
            # --------------------------------

            decision = reasoning.think(
                command
            )

            executive_memory.set_goal(
                decision.goal
            )

            executive_memory.set_step(
                "Reasoning"
            )

            brain_debugger.print_reasoning(
                decision
            )

            # --------------------------------
            # Step 2 : Planning
            # --------------------------------

            plan = None

            if decision.requires_planner:

                executive_memory.set_step(
                    "Planning"
                )

                plan = planner.create_plan(
                    decision.goal
                )

            # --------------------------------
            # Step 3 : Workflow
            # --------------------------------

            if (
                decision.requires_workflow
                and plan
            ):

                executive_memory.set_step(
                    "Workflow"
                )

                result = workflow_executor.execute(
                    plan,
                    command
                )

                executive_memory.remember_execution(

                    agent="workflow_executor",

                    provider="internal",

                    result="success"

                )

                return result

            # --------------------------------
            # Step 4 : Direct Execution
            # --------------------------------

            executive_memory.set_step(
                "Executing"
            )

            result = dispatcher.route(
                command
            )

            executive_memory.remember_execution(

                agent="dispatcher",

                provider="local",

                result="success"

            )

            return result

        except Exception as e:

            executive_memory.remember_execution(

                agent="brain",

                provider="internal",

                result="failed"

            )

            raise


controller = BrainController()