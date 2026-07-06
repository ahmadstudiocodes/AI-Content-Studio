class Personality:

    def __init__(self):

        self.name = "Arman"

        self.owner = "Ahmad"

        self.language = "Persian"

        self.mode = "Professional"

    def introduce(self):

        return f"سلام {self.owner}، من {self.name} هستم."


personality = Personality()