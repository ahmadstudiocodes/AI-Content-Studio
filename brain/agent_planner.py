# brain/agent_planner.py


from datetime import datetime
from uuid import uuid4



class PlanStep:
    """
    Single step inside agent plan.
    """

    def __init__(
        self,
        name,
        agent,
        objective,
        order
    ):

        self.id = str(
            uuid4()
        )

        self.name = name

        self.agent = agent

        self.objective = objective

        self.order = order

        self.status = "pending"



    def complete(
        self
    ):

        self.status = "completed"



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "name":
                self.name,

            "agent":
                self.agent,

            "objective":
                self.objective,

            "order":
                self.order,

            "status":
                self.status

        }





class AgentPlan:
    """
    Multi agent execution plan.
    """

    def __init__(
        self,
        goal
    ):

        self.id = str(
            uuid4()
        )

        self.goal = goal

        self.steps = []

        self.created_at = datetime.utcnow()



    def add_step(
        self,
        step
    ):

        self.steps.append(
            step
        )



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "goal":
                self.goal,

            "steps":

                [

                    step.to_dict()

                    for step in self.steps

                ],

            "created_at":
                self.created_at.isoformat()

        }





class AgentPlanner:
    """
    Arman StudioOS

    Agent Planning Engine.


    Responsibilities:

    - Create plans
    - Break goals
    - Assign workflow steps
    - Track planning
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.plans = {}



    # =====================================================
    # Create Plan
    # =====================================================


    def create_plan(
        self,
        goal
    ):


        plan = AgentPlan(
            goal
        )


        self.plans[plan.id] = plan


        return plan



    # =====================================================
    # Add Step
    # =====================================================


    def add_step(
        self,
        plan_id,
        name,
        agent,
        objective
    ):


        plan = self.plans.get(
            plan_id
        )


        if not plan:

            return False



        step = PlanStep(

            name,

            agent,

            objective,

            len(plan.steps)+1

        )


        plan.add_step(
            step
        )


        return step



    # =====================================================
    # Complete Step
    # =====================================================


    def complete_step(
        self,
        plan_id,
        step_id
    ):


        plan = self.plans.get(
            plan_id
        )


        if not plan:

            return False



        for step in plan.steps:

            if step.id == step_id:

                step.complete()

                return True



        return False



    # =====================================================
    # Retrieve
    # =====================================================


    def get(
        self,
        plan_id
    ):


        plan = self.plans.get(
            plan_id
        )


        if plan:

            return plan.to_dict()


        return None



    def list_plans(
        self
    ):

        return [

            plan.to_dict()

            for plan in self.plans.values()

        ]



    def count(
        self
    ):

        return len(
            self.plans
        )



    def info(
        self
    ):

        return {

            "name":
                "AgentPlanner",

            "version":
                self.VERSION,

            "plans":
                self.count()

        }





# Global Instance

agent_planner = AgentPlanner()