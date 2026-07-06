from agents.agent_manager import agent_manager


class Router:

    def dispatch(self,agent_name,data):

        agent=agent_manager.get(agent_name)

        if agent is None:

            return None

        return agent.run(data)


router=Router()