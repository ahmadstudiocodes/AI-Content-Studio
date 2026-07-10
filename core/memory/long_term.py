class LongTermMemory:

    def __init__(self):

        self.memory = []

    def add(self, role, content):

        self.memory.append({
            "role": role,
            "content": content
        })

    def get(self):

        return self.memory

    def clear(self):

        self.memory.clear()