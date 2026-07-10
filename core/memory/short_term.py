class ShortTermMemory:

    def __init__(self, limit=20):

        self.limit = limit
        self.memory = []

    def add(self, role, content):

        self.memory.append({
            "role": role,
            "content": content
        })

        if len(self.memory) > self.limit:
            self.memory.pop(0)

    def get(self):

        return self.memory

    def clear(self):

        self.memory.clear()