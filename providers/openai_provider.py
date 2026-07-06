from core.provider import Provider


class OpenAIProvider(Provider):

    name = "OpenAI"

    def __init__(self, client):

        self.client = client

    def generate(self, prompt):

        return self.client.generate(prompt)