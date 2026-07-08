class Task:

    def __init__(self):

        self.action = ""

        self.domain = ""

        self.target = ""

        self.arguments = []

        # Sprint 9
        self.payload = None

        self.priority = "normal"

        self.provider = "auto"

        self.need_memory = False

        self.status = "pending"

        self.result = None

    def __str__(self):

        return (
            f"Task("
            f"action={self.action}, "
            f"domain={self.domain}, "
            f"target={self.target}, "
            f"status={self.status})"
        )