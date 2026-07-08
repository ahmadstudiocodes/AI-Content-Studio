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
            "script",
            "thumbnail"
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

        # اطلاعات خام Command را نیز نگه می‌داریم
        intent.target = command.target
        intent.payload = command.payload
        intent.args = command.args

        return intent


intent_engine = IntentEngine()