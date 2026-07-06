from core.registry import registry


class Dispatcher:

    def route(self, command):

        for agent in registry.all().values():

            if agent.can_handle(command):

                return agent.handle(command)

        return f"Unknown Command : {command.raw}"


dispatcher = Dispatcher()