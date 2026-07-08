from core.registry import registry
from core.scorer import AgentScorer



class Dispatcher:


    def __init__(self):

        self.scorer = AgentScorer()



    def route(self, command):


        available_agents = registry.all().values()


        candidates = []



        for agent in available_agents:


            try:

                if agent.can_handle(command):

                    candidates.append(agent)


            except Exception:

                continue




        if not candidates:

            return f"Unknown Command : {command.raw}"





        ranked_agents = []



        for agent in candidates:


            score = self.scorer.score(
                agent,
                command
            )


            ranked_agents.append(
                (agent, score)
            )





        ranked_agents.sort(
            key=lambda x:x[1],
            reverse=True
        )



        selected_agent = ranked_agents[0][0]



        print(
            f"[DISPATCHER] Selected: {selected_agent.name}"
        )

        print(
            f"[DISPATCHER] Score: {ranked_agents[0][1]}"
        )



        return selected_agent.execute(command)




dispatcher = Dispatcher()