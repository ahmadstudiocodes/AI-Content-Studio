from agents.agent_manager import agent_manager


class Dispatcher:

    def dispatch(self,

                 agent_name,

                 task):

        agent = agent_manager.get(agent_name)

        if agent is None:

            return None

        return agent.run(task)


dispatcher = Dispatcher()