class Plan:

    def __init__(self):

        self.agent = None

        self.provider = None

        self.steps = []

        self.status = "waiting"

    def complete(self):

        self.status = "completed"

    def __str__(self):

        return (
            f"Plan("
            f"agent={self.agent}, "
            f"provider={self.provider}, "
            f"steps={len(self.steps)}, "
            f"status={self.status})"
        )