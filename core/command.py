class Command:

    def __init__(self, raw):

        self.raw = raw.strip()

        parts = self.raw.split()

        if not parts:

            self.action = ""
            self.target = ""
            self.args = []

            self.intent = None
            self.task = None
            self.plan = None
            self.payload = None

            return

        self.action = parts[0].lower()

        self.target = parts[1].lower() if len(parts) >= 2 else ""

        self.args = parts[2:]

        # برای Agentها
        self.payload = " ".join(self.args) if self.args else None

        # مراحل Pipeline
        self.intent = None
        self.task = None
        self.plan = None