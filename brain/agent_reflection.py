# brain/agent_reflection.py


from datetime import datetime
from uuid import uuid4



class ReflectionRecord:
    """
    Stores agent reflection result.
    """

    def __init__(
        self,
        agent,
        input_data,
        output_data
    ):

        self.id = str(
            uuid4()
        )

        self.agent = agent

        self.input = input_data

        self.output = output_data

        self.score = None

        self.strengths = []

        self.weaknesses = []

        self.improvements = []

        self.created_at = datetime.utcnow()



    def evaluate(
        self,
        score,
        strengths,
        weaknesses,
        improvements
    ):

        self.score = score

        self.strengths = strengths

        self.weaknesses = weaknesses

        self.improvements = improvements



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "agent":
                self.agent,

            "input":
                self.input,

            "output":
                self.output,

            "score":
                self.score,

            "strengths":
                self.strengths,

            "weaknesses":
                self.weaknesses,

            "improvements":
                self.improvements,

            "created_at":
                self.created_at.isoformat()

        }





class AgentReflection:
    """
    Arman StudioOS

    Agent Reflection Engine.


    Responsibilities:

    - Store reflections
    - Evaluate outputs
    - Track improvements
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.records = []



    # =====================================================
    # Create Reflection
    # =====================================================


    def create(
        self,
        agent,
        input_data,
        output_data
    ):


        record = ReflectionRecord(

            agent,

            input_data,

            output_data

        )


        self.records.append(
            record
        )


        return record



    # =====================================================
    # Evaluate
    # =====================================================


    def evaluate(
        self,
        record,
        score,
        strengths=None,
        weaknesses=None,
        improvements=None
    ):


        record.evaluate(

            score,

            strengths or [],

            weaknesses or [],

            improvements or []

        )


        return record



    # =====================================================
    # History
    # =====================================================


    def history(
        self
    ):

        return [

            record.to_dict()

            for record in self.records

        ]



    def latest(
        self
    ):

        if not self.records:

            return None


        return self.records[-1].to_dict()



    def count(
        self
    ):

        return len(
            self.records
        )



    def info(
        self
    ):

        return {

            "name":
                "AgentReflection",

            "version":
                self.VERSION,

            "records":
                self.count()

        }





# Global Instance

agent_reflection = AgentReflection()