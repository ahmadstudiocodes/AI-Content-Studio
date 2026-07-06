from agents.base_agent import BaseAgent
from providers.provider_manager import provider_manager


class YouTubeAgent(BaseAgent):

    name = "youtube"

    def can_handle(self, command):

        return (
            command.intent.domain == "youtube"
            and command.action == "generate"
        )

    def execute(self, command):

        provider = provider_manager.default()

        return provider.generate(
            f"YouTube Agent Ready : {command.target}"
        )