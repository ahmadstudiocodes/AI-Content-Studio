from core.intent import Intent


class IntentEngine:

    def analyze(self, command):

        intent = Intent()

        intent.action = command.action

        architecture = [
            "plan",
            "floorplan",
            "villa",
            "house",
            "architecture",
            "render"
        ]

        youtube = [
            "youtube",
            "shorts",
            "video",
            "script"
        ]

        finance = [
            "finance",
            "money",
            "income"
        ]

        if command.target in architecture:

            intent.domain = "architecture"

        elif command.target in youtube:

            intent.domain = "youtube"

        elif command.target in finance:

            intent.domain = "finance"

        else:

            intent.domain = "general"

        return intent


intent_engine = IntentEngine()