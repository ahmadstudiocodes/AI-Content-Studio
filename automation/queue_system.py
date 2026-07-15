# automation/queue_system.py


from datetime import datetime
from uuid import uuid4



class QueueJob:
    """
    Represents queued task.
    """

    def __init__(
        self,
        name,
        task,
        priority=50
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.task = task

        self.priority = priority

        self.status = "queued"

        self.result = None

        self.created_at = datetime.utcnow()



    def start(
        self
    ):

        self.status = "running"



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

            "name":
                self.name,

            "priority":
                self.priority,

            "status":
                self.status,

            "result":
                self.result,

            "created_at":
                self.created_at.isoformat()

        }





class QueueSystem:
    """
    Arman StudioOS

    Enterprise Task Queue.


    Responsibilities:

    - Add jobs
    - Prioritize jobs
    - Execute jobs
    - Track history
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.jobs = []



    # =====================================================
    # Add Job
    # =====================================================


    def push(
        self,
        name,
        task,
        priority=50
    ):


        job = QueueJob(

            name,

            task,

            priority

        )


        self.jobs.append(
            job
        )


        self.sort()


        return job



    # =====================================================
    # Priority Sort
    # =====================================================


    def sort(
        self
    ):

        self.jobs.sort(

            key=lambda x: x.priority,

            reverse=True

        )



    # =====================================================
    # Get Next
    # =====================================================


    def pop(
        self
    ):


        for job in self.jobs:


            if job.status == "queued":

                return job



        return None



    # =====================================================
    # Execute
    # =====================================================


    def execute(
        self,
        job
    ):


        try:

            job.start()


            result = job.task()


            job.complete(

                result

            )


        except Exception as error:


            job.fail(

                error

            )


        return job



    # =====================================================
    # Queue Status
    # =====================================================


    def pending(
        self
    ):


        return [

            job.to_dict()

            for job in self.jobs

            if job.status == "queued"

        ]



    def history(
        self
    ):


        return [

            job.to_dict()

            for job in self.jobs

        ]



    def count(
        self
    ):

        return len(
            self.jobs
        )



    def clear(
        self
    ):

        self.jobs.clear()



    def info(
        self
    ):

        return {

            "name":
                "QueueSystem",

            "version":
                self.VERSION,

            "jobs":
                self.count()

        }





# Global Instance

queue_system = QueueSystem()