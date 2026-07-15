# automation/job_scheduler.py


from datetime import datetime, timedelta
from uuid import uuid4



class ScheduledJob:
    """
    Represents scheduled automation job.
    """

    def __init__(
        self,
        name,
        task,
        run_at,
        repeat=None
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.task = task

        self.run_at = run_at

        self.repeat = repeat

        self.status = "scheduled"

        self.last_run = None

        self.created_at = datetime.utcnow()



    def execute(
        self
    ):

        self.status = "running"

        self.last_run = datetime.utcnow()


        result = self.task()


        self.status = "completed"


        return result



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "name":
                self.name,

            "run_at":
                self.run_at.isoformat(),

            "repeat":
                self.repeat,

            "status":
                self.status,

            "last_run":
                self.last_run.isoformat()
                if self.last_run
                else None

        }





class JobScheduler:
    """
    Arman StudioOS

    Enterprise Job Scheduler.


    Responsibilities:

    - Schedule jobs
    - Check execution time
    - Trigger queued tasks
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.jobs = {}



    # =====================================================
    # Schedule
    # =====================================================


    def schedule(
        self,
        name,
        task,
        run_at,
        repeat=None
    ):


        job = ScheduledJob(

            name,

            task,

            run_at,

            repeat

        )


        self.jobs[job.id] = job


        return job



    # =====================================================
    # Run Due Jobs
    # =====================================================


    def run_due(
        self
    ):


        now = datetime.utcnow()

        results = []


        for job in self.jobs.values():


            if (

                job.status == "scheduled"

                and job.run_at <= now

            ):


                results.append(

                    job.execute()

                )



        return results



    # =====================================================
    # Cancel
    # =====================================================


    def cancel(
        self,
        job_id
    ):


        job = self.jobs.get(
            job_id
        )


        if not job:

            return False



        job.status = "cancelled"


        return True



    # =====================================================
    # Helpers
    # =====================================================


    def schedule_daily(
        self,
        name,
        task,
        hour=0
    ):


        run_time = datetime.utcnow().replace(

            hour=hour,

            minute=0,

            second=0,

            microsecond=0

        )


        if run_time < datetime.utcnow():

            run_time += timedelta(

                days=1

            )


        return self.schedule(

            name,

            task,

            run_time,

            repeat="daily"

        )



    def list_jobs(
        self
    ):


        return [

            job.to_dict()

            for job in self.jobs.values()

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
                "JobScheduler",

            "version":
                self.VERSION,

            "jobs":
                self.count()

        }





# Global Instance

job_scheduler = JobScheduler()