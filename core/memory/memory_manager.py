class MemoryManager:
    """
    Coordinates all memory systems.
    """

    def __init__(self):

        self.short_term = None
        self.long_term = None

    def remember(self, role, content):

        if self.short_term:
            self.short_term.add(role, content)

        if self.long_term:
            self.long_term.add(role, content)

    def recall(self):

        data = []

        if self.short_term:
            data.extend(self.short_term.get())

        if self.long_term:
            data.extend(self.long_term.get())

        return data

    def clear(self):

        if self.short_term:
            self.short_term.clear()

        if self.long_term:
            self.long_term.clear()