from core.provider import Provider


class ClaudeProvider(Provider):

    name = "Claude"

    def __init__(self, client):

        self.client = client

    def generate(self, prompt):

        return self.client.generate(prompt)