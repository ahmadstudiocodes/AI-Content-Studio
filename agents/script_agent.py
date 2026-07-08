from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class ScriptAgent(BaseAgent):

    name = "script"

    version = "1.0"

    description = "AI YouTube Script Generator"

    def can_handle(self, command):

        return (
            command.intent.domain == "youtube"
            and command.target == "script"
        )

    def execute(self, command):

        provider = provider_manager.default()

        prompt = f"""
You are Arman StudioOS Script Agent.

Create a professional YouTube video script.

Topic:
{command.payload}

Generate:

1. Video Title
2. Opening Hook (first 10 seconds)
3. Full narration script
4. Scene by scene breakdown
5. Visual suggestions
6. Ending call to action

Answer in Persian.
"""

        return provider.generate(prompt)