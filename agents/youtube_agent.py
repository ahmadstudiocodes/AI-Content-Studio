from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class YouTubeAgent(BaseAgent):

    name = "youtube"

    version = "1.1"

    description = "YouTube Content Generator"


    def can_handle(self, command):

        return (
            command.intent.domain == "youtube"
            and command.action == "generate"
            and command.target == "youtube"
        )


    def execute(self, command):

        provider = provider_manager.default()

        prompt = f"""
You are Arman StudioOS YouTube Content Agent.

User Request:
{command.payload}

Create a professional YouTube content package.

Include:

1. Video Title
2. Strong Hook for first 10 seconds
3. Video structure
4. Script outline
5. Scene suggestions
6. Thumbnail idea
7. SEO keywords

Answer in Persian.
"""

        return provider.generate(prompt)