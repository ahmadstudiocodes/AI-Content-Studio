from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):

    def execute(self, goal):

        return {

            "goal": goal,

            "steps": [

                "Analyze",

                "Plan",

                "Execute"

            ]

        }