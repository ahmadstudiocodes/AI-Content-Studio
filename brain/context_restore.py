# brain/context_restore.py

from copy import deepcopy

from brain.executive_memory import executive_memory
from brain.workflow_history import workflow_history


class ContextRestore:
    """
    Arman StudioOS Context Restore

    Restores workflow state after interruption,
    crash or application restart.

    Responsibilities
    ----------------
    • Restore Executive Memory
    • Restore Workflow History
    • Restore last workflow state
    • Restore previous output
    • Restore constraints
    """

    def restore(
        self,
        memory_snapshot=None,
        history_snapshot=None
    ):
        """
        Restore workflow context.

        Parameters
        ----------
        memory_snapshot : dict
            Executive Memory snapshot.

        history_snapshot : dict
            Workflow History snapshot.
        """

        if memory_snapshot:
            self.restore_memory(
                memory_snapshot
            )

        if history_snapshot:
            self.restore_history(
                history_snapshot
            )

        return {
            "memory": executive_memory.snapshot(),
            "history": workflow_history.get_history()
        }

    def restore_memory(
        self,
        snapshot
    ):
        """
        Restore Executive Memory.
        """

        if not isinstance(snapshot, dict):
            return

        executive_memory.clear()

        for key, value in snapshot.items():

            executive_memory.set(
                key,
                deepcopy(value)
            )

    def restore_history(
        self,
        snapshot
    ):
        """
        Restore Workflow History.
        """

        if not isinstance(snapshot, dict):
            return

        workflow_history.clear()

        workflow_history.workflow = deepcopy(snapshot)

    def restore_last_output(self):
        """
        Restore latest Agent output.
        """

        history = workflow_history.get_history()

        steps = history.get(
            "steps",
            []
        )

        if not steps:
            return None

        last = steps[-1]

        output = last.get("output")

        if output is not None:
            executive_memory.set(
                "last_output",
                output
            )

        return output

    def restore_goal(self):
        """
        Restore workflow goal.
        """

        history = workflow_history.get_history()

        goal = history.get("goal")

        if goal:

            executive_memory.set(
                "goal",
                goal
            )

        return goal

    def restore_constraints(self):
        """
        Restore workflow constraints.
        """

        memory = executive_memory.snapshot()

        constraints = memory.get(
            "constraints",
            []
        )

        executive_memory.set(
            "constraints",
            constraints
        )

        return constraints

    def restore_everything(
        self,
        memory_snapshot=None,
        history_snapshot=None
    ):
        """
        Full workflow restore.
        """

        self.restore(
            memory_snapshot,
            history_snapshot
        )

        self.restore_goal()
        self.restore_last_output()
        self.restore_constraints()

        return {
            "memory": executive_memory.snapshot(),
            "history": workflow_history.get_history()
        }


context_restore = ContextRestore()