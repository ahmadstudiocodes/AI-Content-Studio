class Planner:

    def create_plan(self, goal):

        return {

            "goal": goal,

            "steps": [],

            "status": "created"

        }


planner = Planner()