# automation/cron_manager.py


from datetime import datetime, timedelta
from uuid import uuid4



class CronJob:
    """
    Represents cron based scheduled task.
    """

    def __init__(
        self,
        name,
        task,
        schedule
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.task = task

        self.schedule = schedule

        self.enabled = True

        self.last_run = None

        self.next_run = None

        self.created_at = datetime.utcnow()



    def calculate_next(
        self
    ):


        now = datetime.utcnow()


        if self.schedule == "daily":

            self.next_run = now + timedelta(

                days=1

            )


        elif self.schedule == "weekly":

            self.next_run = now + timedelta(

                weeks=1

            )


        elif self.schedule == "monthly":

            self.next_run = now + timedelta(

                days=30

            )


        return self.next_run



    def run(
        self
    ):


        if not self.enabled:

            return None



        result = self.task()


        self.last_run = datetime.utcnow()


        self.calculate_next()


        return result



    def enable(
        self
    ):

        self.enabled = True



    def disable(
        self
    ):

        self.enabled = False



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "name":
                self.name,

            "schedule":
                self.schedule,

            "enabled":
                self.enabled,

            "last_run":
                self.last_run.isoformat()
                if self.last_run
                else None,

            "next_run":
                self.next_run.isoformat()
                if self.next_run
                else None

        }





class CronManager:
    """
    Arman StudioOS

    Cron Automation Manager.


    Responsibilities:

    - Create cron jobs
    - Monitor schedules
    - Execute timed tasks
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.jobs = {}



    # =====================================================
    # Add Cron
    # =====================================================


    def add(
        self,
        name,
        task,
        schedule
    ):


        job = CronJob(

            name,

            task,

            schedule

        )


        job.calculate_next()


        self.jobs[job.id] = job


        return job



    # =====================================================
    # Check
    # =====================================================


    def run_pending(
        self
    ):


        now = datetime.utcnow()

        results = []



        for job in self.jobs.values():


            if (

                job.enabled

                and job.next_run

                and job.next_run <= now

            ):


                results.append(

                    job.run()

                )



        return results



    # =====================================================
    # Remove
    # =====================================================


    def remove(
        self,
        job_id
    ):


        if job_id in self.jobs:

            del self.jobs[job_id]

            return True



        return False



    # =====================================================
    # List
    # =====================================================


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
                "CronManager",

            "version":
                self.VERSION,

            "jobs":
                self.count()

        }





# Global Instance

cron_manager = CronManager()