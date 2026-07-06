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

            return

        self.action = parts[0].lower()

        self.target = parts[1].lower() if len(parts) >= 2 else ""

        self.args = parts[2:]

        self.intent = None