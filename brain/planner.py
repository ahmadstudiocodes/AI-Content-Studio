from brain.types import (
    ExecutionPlan,
    Task
)


class Planner:


    def create_plan(self, goal):

        plan = ExecutionPlan(
            goal=goal
        )


        keywords = {

            "course": [
                "Research Topic",
                "Create Lessons",
                "Generate Scripts",
                "Create Thumbnails",
                "Prepare Publishing"
            ],


            "youtube": [
                "Analyze Topic",
                "Create Content",
                "Generate Thumbnail",
                "Prepare SEO"
            ],


            "project": [
                "Analyze Requirements",
                "Create Strategy",
                "Execute Tasks",
                "Review Result"
            ]

        }


        selected_tasks = [

            "Analyze Goal",
            "Execute Main Task"

        ]


        for key, tasks in keywords.items():

            if key in goal.lower():

                selected_tasks = tasks

                break



        for item in selected_tasks:

            plan.add_task(
                Task(
                    name=item
                )
            )


        return plan



planner = Planner()