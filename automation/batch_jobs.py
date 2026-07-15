# automation/batch_jobs.py


from datetime import datetime
from uuid import uuid4



class BatchJob:
    """
    Represents batch execution group.
    """

    def __init__(
        self,
        name,
        jobs=None
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.jobs = jobs or []

        self.results = []

        self.status = "created"

        self.created_at = datetime.utcnow()



    def add(
        self,
        job
    ):

        self.jobs.append(
            job
        )



    def complete(
        self
    ):

        self.status = "completed"



    def fail(
        self,
        error
    ):

        self.status = "failed"

        self.results.append(

            {
                "error":
                    str(error)
            }

        )



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "name":
                self.name,

            "jobs":
                len(self.jobs),

            "results":
                self.results,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class BatchJobs:
    """
    Arman StudioOS

    Batch Processing Engine.


    Responsibilities:

    - Create batches
    - Execute groups
    - Track results
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.batches = {}



    # =====================================================
    # Create Batch
    # =====================================================


    def create(
        self,
        name
    ):


        batch = BatchJob(

            name

        )


        self.batches[batch.id] = batch


        return batch



    # =====================================================
    # Add Task
    # =====================================================


    def add_job(
        self,
        batch_id,
        job
    ):


        batch = self.batches.get(

            batch_id

        )


        if not batch:

            return False



        batch.add(

            job

        )


        return True



    # =====================================================
    # Execute Batch
    # =====================================================


    def execute(
        self,
        batch_id
    ):


        batch = self.batches.get(

            batch_id

        )


        if not batch:

            return None



        batch.status = "running"



        try:


            for job in batch.jobs:


                try:

                    result = job()


                    batch.results.append(

                        result

                    )


                except Exception as error:


                    batch.results.append(

                        {
                            "error":
                                str(error)
                        }

                    )



            batch.complete()



        except Exception as error:


            batch.fail(

                error

            )



        return batch



    # =====================================================
    # History
    # =====================================================


    def list_batches(
        self
    ):


        return [

            batch.to_dict()

            for batch in self.batches.values()

        ]



    def get(
        self,
        batch_id
    ):


        batch = self.batches.get(

            batch_id

        )


        if batch:

            return batch.to_dict()


        return None



    def count(
        self
    ):

        return len(

            self.batches

        )



    def clear(
        self
    ):

        self.batches.clear()



    def info(
        self
    ):

        return {

            "name":
                "BatchJobs",

            "version":
                self.VERSION,

            "batches":
                self.count()

        }





# Global Instance

batch_jobs = BatchJobs()