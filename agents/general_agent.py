from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class GeneralAgent(BaseAgent):

    name = "general"

    def can_handle(self, command):

        cmd = command.lower()

        return cmd in [
            "سلام",
            "help",
            "provider"
        ]

    def handle(self, command):

        cmd = command.lower()

        if cmd == "سلام":

            provider = provider_manager.default()

            return provider.generate("سلام احمد 🌱")

        if cmd == "help":

            return (
                "\n"
                "Commands\n"
                "----------------\n"
                "help\n"
                "exit\n"
                "سلام\n"
                "provider\n"
            )

        if cmd == "provider":

            provider = provider_manager.default()

            return f"Current Provider : {provider.name}"

        return None