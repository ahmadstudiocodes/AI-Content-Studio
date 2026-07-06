from agents.base_agent import BaseAgent


class LLMAgent(BaseAgent):

    name = "LLM"

    description = "Large Language Model Agent"

    def __init__(self):

        self.provider = None

    def connect(self, provider):

        self.provider = provider

    def run(self, prompt):

        if self.provider is None:

            raise RuntimeError("LLM Provider Not Connected")

        return self.provider.generate(prompt)