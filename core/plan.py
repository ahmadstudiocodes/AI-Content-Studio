from datetime import datetime



class Plan:

    """
    Arman StudioOS Execution Plan

    Represents:

    - Goal
    - Agent assignment
    - Provider
    - Workflow steps
    - Execution status

    """


    STATUSES = {

        "waiting",

        "running",

        "completed",

        "failed"

    }



    def __init__(
        self,
        goal=None
    ):


        self.goal = goal


        self.agent = None

        self.provider = None


        self.steps = []


        self.status = "waiting"


        self.created_at = (
            datetime.now()
            .isoformat()
        )


        self.completed_at = None



    # ==================================================

    def add_step(
        self,
        step
    ):


        self.steps.append(
            step
        )



    # ==================================================

    def complete(
        self
    ):


        self.status = "completed"


        self.completed_at = (
            datetime.now()
            .isoformat()
        )



    # ==================================================

    def fail(
        self
    ):


        self.status = "failed"


        self.completed_at = (
            datetime.now()
            .isoformat()
        )



    # ==================================================

    def start(
        self
    ):


        self.status = "running"



    # ==================================================

    def __str__(
        self
    ):


        return (

            f"Plan("

            f"goal={self.goal}, "

            f"agent={self.agent}, "

            f"provider={self.provider}, "

            f"steps={len(self.steps)}, "

            f"status={self.status}"

            f")"

        )