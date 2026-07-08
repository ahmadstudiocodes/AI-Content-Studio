class ExecutiveMemory:
    """
    Arman Executive Memory

    Stores:

    - Current Goal
    - Current Workflow
    - Current Step
    - Running Tasks
    - Completed Tasks
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

        self.last_agent = None

        self.last_provider = None

        self.last_result = None

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

        if task not in self.running_tasks:

            self.running_tasks.append(
                task
            )

    def complete_task(
        self,
        task
    ):

        if task in self.running_tasks:

            self.running_tasks.remove(
                task
            )

        if task not in self.completed_tasks:

            self.completed_tasks.append(
                task
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

        self.last_result = result

    # ---------------------------------
    # Snapshot
    # ---------------------------------

    def snapshot(self):

        return {

            "goal": self.goal,

            "current_step": self.current_step,

            "current_workflow": self.current_workflow,

            "running_tasks": [

                getattr(t, "name", str(t))

                for t in self.running_tasks

            ],

            "completed_tasks": [

                getattr(t, "name", str(t))

                for t in self.completed_tasks

            ],

            "last_agent": self.last_agent,

            "last_provider": self.last_provider,

            "last_result": self.last_result

        }

    # سازگاری با نسخه‌های قبلی

    def state(self):

        return self.snapshot()


executive_memory = ExecutiveMemory()