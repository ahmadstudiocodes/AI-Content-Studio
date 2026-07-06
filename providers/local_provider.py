from providers.base_provider import BaseProvider


class LocalProvider(BaseProvider):

    name = "local"

    def available(self):
        return True

    def generate(self, prompt: str):

        return f"[LOCAL PROVIDER] {prompt}"