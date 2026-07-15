from datetime import datetime


class ExecutiveMemory:

    """
    Arman StudioOS Executive Memory

    Stores:

    - Current Goal
    - Current Workflow
    - Current Step
    - Running Tasks
    - Completed Tasks
    - Failed Tasks
    - Last Execution
    """


    def __init__(self):

        self.reset()



    # ---------------------------------
    # Reset
    # ---------------------------------

    def reset(self):

        self.goal = None

        self.current_step = None

        self.current_workflow = None


        self.running_tasks = []

        self.completed_tasks = []

        self.failed_tasks = []


        self.last_agent = None

        self.last_provider = None

        self.last_result = None

        self.last_execution_time = None



    # ---------------------------------
    # Goal
    # ---------------------------------

    def set_goal(
        self,
        goal
    ):

        self.goal = goal



    # ---------------------------------
    # Workflow
    # ---------------------------------

    def set_workflow(
        self,
        workflow
    ):

        self.current_workflow = workflow



    # ---------------------------------
    # Step
    # ---------------------------------

    def set_step(
        self,
        step
    ):

        self.current_step = step



    # ---------------------------------
    # Tasks
    # ---------------------------------

    def add_task(
        self,
        task
    ):


        if not self.contains_task(
            task,
            self.running_tasks
        ):

            self.running_tasks.append(
                task
            )



    def complete_task(
        self,
        task
    ):


        self.remove_task(
            task,
            self.running_tasks
        )


        if not self.contains_task(
            task,
            self.completed_tasks
        ):

            self.completed_tasks.append(
                task
            )



    def fail_task(
        self,
        task
    ):


        self.remove_task(
            task,
            self.running_tasks
        )


        if not self.contains_task(
            task,
            self.failed_tasks
        ):

            self.failed_tasks.append(
                task
            )



    def remove_task(
        self,
        task,
        collection
    ):


        for item in collection[:]:

            if self.task_equal(
                item,
                task
            ):

                collection.remove(
                    item
                )



    def contains_task(
        self,
        task,
        collection
    ):


        return any(

            self.task_equal(
                item,
                task
            )

            for item in collection

        )



    def task_equal(
        self,
        a,
        b
    ):


        return (

            getattr(a, "name", None)

            ==

            getattr(b, "name", None)

        )



    # ---------------------------------
    # Execution
    # ---------------------------------

    def remember_execution(

        self,

        agent,

        provider,

        result

    ):


        self.last_agent = agent

        self.last_provider = provider


        if result:

            self.last_result = str(result)[:3000]

        else:

            self.last_result = None



        self.last_execution_time = (
            datetime.now()
            .isoformat()
        )



    # ---------------------------------
    # Snapshot
    # ---------------------------------

    def snapshot(self):


        return {


            "goal": self.goal,


            "current_step": self.current_step,


            "current_workflow": self.current_workflow,



            "running_tasks": [

                getattr(
                    t,
                    "name",
                    str(t)
                )

                for t in self.running_tasks

            ],



            "completed_tasks": [

                getattr(
                    t,
                    "name",
                    str(t)
                )

                for t in self.completed_tasks

            ],



            "failed_tasks": [

                getattr(
                    t,
                    "name",
                    str(t)
                )

                for t in self.failed_tasks

            ],



            "last_agent": self.last_agent,


            "last_provider": self.last_provider,


            "last_result": self.last_result,


            "last_execution_time":
                self.last_execution_time


        }



    # ---------------------------------
    # Backward Compatibility
    # ---------------------------------

    def state(self):

        return self.snapshot()



executive_memory = ExecutiveMemory()