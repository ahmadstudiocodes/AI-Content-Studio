from datetime import datetime
import uuid



class Task:

    """
    Arman StudioOS Task

    Represents one executable workflow step.

    Contains:

    - Action
    - Domain
    - Target
    - Payload
    - Execution State

    """



    STATUSES = {

        "pending",

        "running",

        "completed",

        "failed"

    }



    def __init__(
        self
    ):


        self.id = str(
            uuid.uuid4()
        )


        self.name = ""


        self.action = ""


        self.domain = ""


        self.target = ""


        self.goal = ""


        self.arguments = []



        # Sprint 9

        self.payload = None



        self.priority = "normal"



        self.provider = "auto"



        self.need_memory = False



        self.status = "pending"



        self.result = None



        self.created_at = (
            datetime.now()
            .isoformat()
        )



    # ==================================================

    def complete(
        self,
        result=None
    ):


        self.status = "completed"


        self.result = result



    # ==================================================

    def fail(
        self,
        error
    ):


        self.status = "failed"


        self.result = str(error)



    # ==================================================

    def __str__(
        self
    ):


        return (

            f"Task("

            f"id={self.id[:8]}, "

            f"name={self.name}, "

            f"action={self.action}, "

            f"domain={self.domain}, "

            f"target={self.target}, "

            f"status={self.status}"

            f")"

        )