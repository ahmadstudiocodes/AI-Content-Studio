from abc import ABC, abstractmethod

from agents.state import AgentState

from agents.task_result import TaskResult


class BaseAgent(ABC):

    def __init__(self):

        self.state = AgentState.IDLE

        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, task):

        pass

    def run(self, task):

        self.state = AgentState.RUNNING

        try:

            result = self.execute(task)

            self.state = AgentState.SUCCESS

            return TaskResult(

                success=True,

                output=result

            )

        except Exception as e:

            self.state = AgentState.FAILED

            return TaskResult(

                success=False,

                error=str(e)

            )