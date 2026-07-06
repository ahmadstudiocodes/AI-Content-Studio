class ReasoningEngine:

    def think(self, question):

        return {

            "question": question,

            "status": "received",

            "next": "planner"

        }


reasoning = ReasoningEngine()