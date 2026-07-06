from agents.base_agent import BaseAgent

from brain.memory_brain import brain_memory


class MemoryAgent(BaseAgent):

    def execute(self,task):

        action=task.get("action")

        if action=="save":

            brain_memory.remember(

                task["key"],

                task["value"]

            )

            return "saved"

        if action=="load":

            return brain_memory.recall(

                task["key"]

            )

        return None