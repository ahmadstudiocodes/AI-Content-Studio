class BaseProvider:

    name = "base"

    def available(self) -> bool:
        return False

    def generate(self, prompt: str) -> str:
        raise NotImplementedError