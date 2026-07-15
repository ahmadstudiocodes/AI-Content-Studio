from core.plan import Plan


class PlanStep:

    def __init__(self, name):

        self.name = name
        self.status = "waiting"
        self.result = None


class Planner:
    """
    Arman StudioOS Workflow Planner
    """

    WORKFLOWS = {

        "course": [

            "Research Topic",
            "Design Course Structure",
            "Create Lesson Plan",
            "Generate Lesson Scripts",
            "Create Thumbnails",
            "Prepare Publishing"

        ],

        "youtube": [

            "Analyze Topic",
            "Create Content",
            "Generate Thumbnail",
            "Prepare SEO"

        ],

        "architecture": [

            "Analyze Architecture Problem",
            "Create Design Strategy",
            "Generate Architecture Solution",
            "Review Result"

        ],

        "project": [

            "Analyze Requirements",
            "Create Strategy",
            "Execute Tasks",
            "Review Result"

        ],

        "research": [

            "Collect Information",
            "Analyze Data",
            "Create Research Report"

        ]

    }

    def create_plan(
        self,
        goal
    ):

        plan = Plan(goal)

        for task_name in self.detect_workflow(goal):

            plan.add_step(
                PlanStep(task_name)
            )

        return plan

    # ---------------------------------

    def detect_workflow(
        self,
        goal
    ):

        text = str(goal).lower()

        for keyword, tasks in self.WORKFLOWS.items():

            if keyword in text:

                return tasks

        return [

            "Analyze Goal",
            "Execute Main Task"

        ]

    # ---------------------------------

    def preview(
        self,
        goal
    ):

        tasks = self.detect_workflow(goal)

        return {

            "goal": goal,

            "steps": tasks,

            "total_tasks": len(tasks)

        }


planner = Planner()