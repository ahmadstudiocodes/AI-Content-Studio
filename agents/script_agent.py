class ScriptAgent:

    def generate(self, topic):

        return {
            "topic": topic,
            "title": "",
            "script": "",
            "status": "draft"
        }


script_agent = ScriptAgent()