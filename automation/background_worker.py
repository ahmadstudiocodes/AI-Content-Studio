# automation/background_worker.py


import time

from datetime import datetime
from uuid import uuid4



class WorkerStatus:
    """
    Worker execution status.
    """

    def __init__(
        self,
        name
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.running = False

        self.jobs_completed = 0

        self.jobs_failed = 0

        self.started_at = None

        self.last_job = None



    def start(
        self
    ):

        self.running = True

        self.started_at = datetime.utcnow()



    def stop(
        self
    ):

        self.running = False



    def success(
        self,
        job
    ):

        self.jobs_completed += 1

        self.last_job = job



    def failed(
        self,
        job
    ):

        self.jobs_failed += 1

        self.last_job = job



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "name":
                self.name,

            "running":
                self.running,

            "jobs_completed":
                self.jobs_completed,

            "jobs_failed":
                self.jobs_failed,

            "last_job":
                self.last_job

        }





class BackgroundWorker:
    """
    Arman StudioOS

    Background Job Worker.


    Responsibilities:

    - Consume queue
    - Execute jobs
    - Monitor execution
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        queue,
        name="worker-1"
    ):

        self.queue = queue

        self.status = WorkerStatus(

            name

        )

        self.active = False



    # =====================================================
    # Start Worker
    # =====================================================


    def start(
        self,
        interval=1
    ):


        self.active = True

        self.status.start()



        while self.active:


            job = self.queue.pop()



            if job:


                try:

                    self.queue.execute(

                        job

                    )


                    self.status.success(

                        job.name

                    )


                except Exception:


                    self.status.failed(

                        job.name

                    )


            else:


                time.sleep(

                    interval

                )



    # =====================================================
    # Single Cycle
    # =====================================================


    def run_once(
        self
    ):


        job = self.queue.pop()


        if not job:

            return None



        result = self.queue.execute(

            job

        )


        return result



    # =====================================================
    # Stop
    # =====================================================


    def stop(
        self
    ):


        self.active = False

        self.status.stop()



    # =====================================================
    # Info
    # =====================================================


    def info(
        self
    ):


        return {

            "name":
                "BackgroundWorker",

            "version":
                self.VERSION,

            "status":
                self.status.to_dict()

        }