from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Root base class for all Arman StudioOS agents.
    """

    def __init__(
        self,
        name="base",
        description="",
    ):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, user_input):
        """
        Execute the agent.
        """
        pass

    def info(self):
        return {
            "name": self.name,
            "description": self.description,
        }