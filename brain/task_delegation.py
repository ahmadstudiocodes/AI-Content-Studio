# brain/task_delegation.py


from datetime import datetime
from uuid import uuid4



class DelegatedTask:
    """
    Represents delegated task.
    """

    def __init__(
        self,
        task,
        agent,
        priority=50
    ):

        self.id = str(
            uuid4()
        )

        self.task = task

        self.agent = agent

        self.priority = priority

        self.status = "pending"

        self.created_at = datetime.utcnow()

        self.result = None



    def complete(
        self,
        result
    ):

        self.status = "completed"

        self.result = result



    def fail(
        self,
        error
    ):

        self.status = "failed"

        self.result = {

            "error":
                str(error)

        }



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "task":
                self.task,

            "agent":
                self.agent,

            "priority":
                self.priority,

            "status":
                self.status,

            "result":
                self.result,

            "created_at":
                self.created_at.isoformat()

        }





class TaskDelegation:
    """
    Arman StudioOS

    Task Delegation Engine.


    Responsibilities:

    - Assign tasks
    - Select agents
    - Track execution
    - Manage priorities
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.tasks = []



    # =====================================================
    # Delegate
    # =====================================================


    def delegate(
        self,
        task,
        agent,
        priority=50
    ):


        delegated = DelegatedTask(

            task,

            agent,

            priority

        )


        self.tasks.append(
            delegated
        )


        return delegated



    # =====================================================
    # Execute
    # =====================================================


    def execute(
        self,
        delegated_task,
        executor
    ):

        try:

            result = executor(
                delegated_task.agent,
                delegated_task.task
            )


            delegated_task.complete(
                result
            )


        except Exception as error:


            delegated_task.fail(
                error
            )


        return delegated_task



    # =====================================================
    # Queue
    # =====================================================


    def pending(
        self
    ):


        return [

            task.to_dict()

            for task in self.tasks

            if task.status == "pending"

        ]



    # =====================================================
    # History
    # =====================================================


    def history(
        self
    ):

        return [

            task.to_dict()

            for task in self.tasks

        ]



    def count(
        self
    ):

        return len(
            self.tasks
        )



    def info(
        self
    ):

        return {

            "name":
                "TaskDelegation",

            "version":
                self.VERSION,

            "tasks":
                self.count()

        }





# Global Instance

task_delegation = TaskDelegation()