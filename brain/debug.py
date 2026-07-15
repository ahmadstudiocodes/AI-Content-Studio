from brain.executive_memory import executive_memory


class BrainDebugger:

    """
    Arman StudioOS Brain Debugger

    Shows reasoning decisions
    and current executive memory state.
    """



    def print_reasoning(
        self,
        decision
    ):


        memory = executive_memory.snapshot()


        print("\n========== ARMAN BRAIN ==========")



        print(
            f"Goal            : {getattr(decision, 'goal', None)}"
        )


        print(
            f"Complexity      : {self.safe_value(decision, 'complexity')}"
        )


        print(
            f"Planner         : {getattr(decision, 'requires_planner', False)}"
        )


        print(
            f"Memory          : {getattr(decision, 'requires_memory', False)}"
        )


        print(
            f"Workflow        : {getattr(decision, 'requires_workflow', False)}"
        )


        print(
            f"Execution       : {self.safe_value(decision, 'execution')}"
        )



        print("--------------------------------")



        print(
            f"Memory Goal     : {memory.get('goal')}"
        )


        print(
            f"Current Step    : {memory.get('current_step')}"
        )


        print(
            f"Workflow        : {memory.get('current_workflow')}"
        )


        print(
            f"Running Tasks   : {memory.get('running_tasks')}"
        )


        print(
            f"Completed Tasks : {memory.get('completed_tasks')}"
        )


        print(
            f"Failed Tasks    : {memory.get('failed_tasks')}"
        )


        print(
            f"Last Agent      : {memory.get('last_agent')}"
        )


        print(
            f"Last Provider   : {memory.get('last_provider')}"
        )


        result = memory.get(
            "last_result"
        )


        if result and len(str(result)) > 500:

            result = (
                str(result)[:500]
                +
                "\n...TRUNCATED..."
            )


        print(
            f"Last Result     : {result}"
        )


        print(
            f"Execution Time  : {memory.get('last_execution_time')}"
        )


        print(
            "================================\n"
        )



    # ==================================================

    def safe_value(
        self,
        obj,
        attribute
    ):


        value = getattr(
            obj,
            attribute,
            None
        )


        if value is None:

            return None


        return getattr(
            value,
            "value",
            str(value)
        )



brain_debugger = BrainDebugger()