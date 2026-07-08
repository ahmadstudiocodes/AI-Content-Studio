from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class ArchitectureAgent(BaseAgent):

    name = "architecture"

    def can_handle(self, command):

        return (
            command.intent.domain == "architecture"
            and command.action in [
                "generate",
                "plan",
                "render",
                "design"
            ]
        )

    def execute(self, command):

        provider = provider_manager.default()

        prompt = f"""
You are Arman StudioOS Architecture Agent.

User Request:
Action: {command.action}
Target: {command.target}
Arguments: {' '.join(command.args)}

Generate a professional architectural response.
"""

        response = provider.generate(prompt)

        return response