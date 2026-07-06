from core.plan import Plan


class Planner:

    def create(self, task):

        plan = Plan()

        plan.provider = task.provider

        if task.domain == "youtube":

            plan.agent = "youtube"

        elif task.domain == "architecture":

            plan.agent = "architecture"

        elif task.domain == "finance":

            plan.agent = "finance"

        else:

            plan.agent = "general"

        plan.steps.append("execute")

        return plan


planner = Planner()