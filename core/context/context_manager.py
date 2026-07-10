class ContextManager:
    """
    Manages conversation context between agents.
    """

    def __init__(self, max_history=10):

        self.max_history = max_history
        self.history = []

    def add(self, role, content):

        self.history.append({
            "role": role,
            "content": content
        })

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get(self):

        return self.history

    def clear(self):

        self.history.clear()

    def build(self):

        if not self.history:
            return ""

        context = []

        for item in self.history:

            context.append(
                f"{item['role'].upper()}:\n{item['content']}"
            )

        return "\n\n".join(context)