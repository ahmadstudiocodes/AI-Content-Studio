from core.dispatcher import dispatcher


class ExecutionPipeline:

    def execute(self, command):

        command.plan.status = "running"

        result = dispatcher.route(command)

        command.plan.complete()

        # فقط برای Debug
        if command.action == "plan":
            return str(command.plan)

        return result


pipeline = ExecutionPipeline()