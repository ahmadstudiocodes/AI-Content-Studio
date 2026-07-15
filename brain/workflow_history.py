# brain/workflow_history.py

import json
from copy import deepcopy
from datetime import datetime


class WorkflowHistory:
    """
    Arman StudioOS Workflow History

    Records every step executed during a workflow.

    Responsibilities
    ----------------
    • Start a workflow session
    • Record agent executions
    • Store outputs
    • Track execution time
    • Export workflow history
    • Clear history after completion
    """

    def __init__(self):
        self.clear()

    def start(
        self,
        workflow_id,
        goal=None
    ):
        """
        Start a new workflow.
        """

        self.workflow = {
            "workflow_id": workflow_id,
            "goal": goal,
            "started_at": self._timestamp(),
            "finished_at": None,
            "steps": []
        }

    def add_step(
        self,
        agent,
        task,
        output=None,
        duration=0.0,
        status="success",
        metadata=None
    ):
        """
        Add one executed workflow step.
        """

        if metadata is None:
            metadata = {}

        step = {
            "timestamp": self._timestamp(),
            "agent": agent,
            "task": task,
            "status": status,
            "duration": duration,
            "output": output,
            "metadata": deepcopy(metadata)
        }

        self.workflow["steps"].append(step)

    def last_step(self):
        """
        Return last executed step.
        """

        if not self.workflow["steps"]:
            return None

        return deepcopy(
            self.workflow["steps"][-1]
        )

    def get_history(self):
        """
        Return entire workflow history.
        """

        return deepcopy(self.workflow)

    def get_steps(self):
        """
        Return only workflow steps.
        """

        return deepcopy(
            self.workflow["steps"]
        )

    def finish(self):
        """
        Mark workflow as completed.
        """

        self.workflow["finished_at"] = self._timestamp()

    def export(self):
        """
        Export workflow history as JSON.
        """

        return json.dumps(
            self.workflow,
            indent=4,
            ensure_ascii=False
        )

    def save(
        self,
        filepath
    ):
        """
        Save workflow history to disk.
        """

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.workflow,
                f,
                indent=4,
                ensure_ascii=False
            )

    def load(
        self,
        filepath
    ):
        """
        Load workflow history from disk.
        """

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            self.workflow = json.load(f)

    def clear(self):
        """
        Reset workflow history.
        """

        self.workflow = {
            "workflow_id": None,
            "goal": None,
            "started_at": None,
            "finished_at": None,
            "steps": []
        }

    @staticmethod
    def _timestamp():
        """
        Current UTC timestamp.
        """

        return datetime.utcnow().isoformat() + "Z"


workflow_history = WorkflowHistory()