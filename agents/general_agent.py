from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class GeneralAgent(BaseAgent):

    name = "general"

    def can_handle(self, command):

        return command.action in [

            "سلام",
            "help",
            "provider",
            "task",
            "plan"

        ]

    def execute(self, command):

        if command.action == "سلام":

            provider = provider_manager.default()

            return provider.generate("سلام احمد 🌱")

        if command.action == "provider":

            provider = provider_manager.default()

            return f"Current Provider : {provider.name}"

        if command.action == "help":

            return (
                "\n"
                "Commands\n"
                "----------------\n"
                "help\n"
                "provider\n"
                "task\n"
                "plan\n"
                "exit\n"
            )

        if command.action == "task":

            return str(command.task)

       

        return None