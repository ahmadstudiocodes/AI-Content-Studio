from core.provider import Provider


class GeminiProvider(Provider):

    name = "Gemini"

    def __init__(self, client):

        self.client = client

    def generate(self, prompt):

        return self.client.generate(prompt)