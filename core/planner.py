from core.plan import Plan


class Planner:

    """
    Arman StudioOS Planner

    Creates execution plans
    from reasoning tasks.
    """



    def create(
        self,
        task
    ):


        plan = Plan(

            goal=getattr(
                task,
                "goal",
                getattr(
                    task,
                    "name",
                    "unknown"
                )
            )

        )



        plan.provider = getattr(
            task,
            "provider",
            None
        )



        domain = getattr(
            task,
            "domain",
            "general"
        )



        if domain == "youtube":

            plan.agent = "youtube"



        elif domain == "architecture":

            plan.agent = "architecture"



        elif domain == "finance":

            plan.agent = "finance"



        else:

            plan.agent = "general"



        # ---------------------------------
        # Create executable task
        # ---------------------------------

        class PlanStep:

            def __init__(
                self,
                name
            ):

                self.name = name

                self.status = "waiting"

                self.result = None



        plan.steps.append(

            PlanStep(
                "execute"
            )

        )



        return plan



planner = Planner()