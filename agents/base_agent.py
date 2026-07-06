class BaseAgent:

    name = "base"

    def can_handle(self, command: str) -> bool:
        return False

    def handle(self, command: str):
        return None