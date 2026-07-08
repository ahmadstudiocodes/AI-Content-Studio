from brain.executive_memory import executive_memory


class BrainDebugger:

    """
    Arman Brain Debugger
    """

    def print_reasoning(
        self,
        decision
    ):

        memory = executive_memory.snapshot()

        print("\n========== BRAIN ==========")

        print(
            f"Goal            : {decision.goal}"
        )

        print(
            f"Complexity      : {decision.complexity.value}"
        )

        print(
            f"Planner         : {decision.requires_planner}"
        )

        print(
            f"Memory          : {decision.requires_memory}"
        )

        print(
            f"Workflow        : {decision.requires_workflow}"
        )

        print(
            f"Execution       : {decision.execution.value}"
        )

        print("--------------------------------")

        print(
            f"Memory Goal     : {memory['goal']}"
        )

        print(
            f"Current Step    : {memory['current_step']}"
        )

        print(
            f"Current Workflow: {memory['current_workflow']}"
        )

        print(
            f"Running Tasks   : {memory['running_tasks']}"
        )

        print(
            f"Completed Tasks : {memory['completed_tasks']}"
        )

        print(
            f"Last Agent      : {memory['last_agent']}"
        )

        print(
            f"Last Provider   : {memory['last_provider']}"
        )

        print(
            f"Last Result     : {memory['last_result']}"
        )

        print("===========================\n")


brain_debugger = BrainDebugger()