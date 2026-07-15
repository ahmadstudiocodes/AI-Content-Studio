# brain/self_critique.py


from datetime import datetime
from uuid import uuid4



class CritiqueResult:
    """
    Result of self critique process.
    """

    def __init__(
        self,
        agent,
        response
    ):

        self.id = str(
            uuid4()
        )

        self.agent = agent

        self.response = response

        self.score = None

        self.issues = []

        self.suggestions = []

        self.approved = False

        self.created_at = datetime.utcnow()



    def approve(
        self
    ):

        self.approved = True



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "agent":
                self.agent,

            "response":
                self.response,

            "score":
                self.score,

            "issues":
                self.issues,

            "suggestions":
                self.suggestions,

            "approved":
                self.approved,

            "created_at":
                self.created_at.isoformat()

        }





class SelfCritique:
    """
    Arman StudioOS

    Self Critique Engine.


    Responsibilities:

    - Analyze outputs
    - Detect problems
    - Improve responses
    - Quality control
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.history = []



    # =====================================================
    # Analyze
    # =====================================================


    def analyze(
        self,
        agent,
        response
    ):


        result = CritiqueResult(

            agent,

            response

        )


        self.history.append(
            result
        )


        return result



    # =====================================================
    # Evaluate
    # =====================================================


    def evaluate(
        self,
        result,
        score,
        issues=None,
        suggestions=None
    ):


        result.score = score

        result.issues = issues or []

        result.suggestions = suggestions or []



        if score >= 80:

            result.approve()



        return result



    # =====================================================
    # Approval
    # =====================================================


    def is_approved(
        self,
        result
    ):


        return result.approved



    # =====================================================
    # History
    # =====================================================


    def get_history(
        self
    ):


        return [

            item.to_dict()

            for item in self.history

        ]



    def count(
        self
    ):

        return len(
            self.history
        )



    def info(
        self
    ):

        return {

            "name":
                "SelfCritique",

            "version":
                self.VERSION,

            "reviews":
                self.count()

        }





# Global Instance

self_critique = SelfCritique()