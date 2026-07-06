from agents.base_agent import BaseAgent


class RuntimeAgent(BaseAgent):

    def execute(self, task):

        print("Running...")

        return task