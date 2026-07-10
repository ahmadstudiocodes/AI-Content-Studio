class Command:

    def __init__(self, raw):

        raw = str(raw).strip()

        if raw.lower().startswith("arman>"):
            raw = raw[6:].strip()

        self.raw = raw

        parts = self.raw.split()

        if not parts:

            self.action = ""
            self.target = ""
            self.args = []

            self.payload = ""

            self.intent = None
            self.task = None
            self.plan = None
            self.workflow = None
            self.agent = None

            return

        self.action = parts[0].lower()

        self.target = (
            parts[1].lower()
            if len(parts) > 1
            else ""
        )

        self.args = parts[2:]

        self.payload = " ".join(self.args)

        # Filled by Router
        self.intent = None
        self.task = None
        self.plan = None
        self.workflow = None
        self.agent = None

    @property
    def text(self):

        return self.payload

    def __repr__(self):

        return (
            f"Command("
            f"action={self.action}, "
            f"target={self.target}, "
            f"payload={self.payload})"
        )