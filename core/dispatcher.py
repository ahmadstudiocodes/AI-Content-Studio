from core.registry import registry
from core.scorer import AgentScorer


class Dispatcher:

    """
    Arman StudioOS Dispatcher

    Responsibility:

        Command
            ↓
        Agent Scoring
            ↓
        Agent Selection

    Dispatcher DOES NOT execute agents.
    """


    def __init__(self):

        self.scorer = AgentScorer()



    # ==================================================

    def route(
        self,
        command
    ):


        if command is None:

            print(
                "[DISPATCHER] Empty command."
            )

            return None



        agents = self.get_agents()



        if not agents:

            print(
                "[DISPATCHER] No agents registered."
            )

            return None



        candidates = []



        for agent in agents:


            try:


                score = self.scorer.score(
                    agent,
                    command
                )


                score = self.safe_score(
                    score
                )


                if score > 0:


                    candidates.append(

                        (
                            score,
                            agent

                        )

                    )



            except Exception as e:


                print(

                    f"[DISPATCHER] "
                    f"{self.agent_name(agent)}: {e}"

                )



        if not candidates:


            print(

                "[DISPATCHER] "
                f"No agent found for: "
                f"{getattr(command, 'raw', 'unknown')}"

            )


            return None



        candidates.sort(

            key=lambda item: item[0],

            reverse=True

        )



        score, agent = candidates[0]



        print(

            f"[DISPATCHER] Selected: "
            f"{self.agent_name(agent)} "
            f"({score})"

        )


        return agent



    # ==================================================

    def get_agents(
        self
    ):


        try:

            return list(
                registry.all().values()
            )


        except Exception as e:


            print(
                f"[DISPATCHER] Registry error: {e}"
            )


            return []



    # ==================================================

    def agent_name(
        self,
        agent
    ):


        return getattr(

            agent,

            "name",

            agent.__class__.__name__

        )



    # ==================================================

    def safe_score(
        self,
        score
    ):


        try:

            return float(score)

        except:

            return 0



dispatcher = Dispatcher()