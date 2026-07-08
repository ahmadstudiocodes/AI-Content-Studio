class AgentScorer:


    def score(self, agent, command):

        score = 0


        # priority
        score += getattr(agent, "priority", 0)


        # capability/domain matching
        try:

            if hasattr(agent, "domains"):

                for domain in agent.domains:

                    if domain.lower() in command.raw.lower():

                        score += 50


        except Exception:
            pass



        # capability matching
        try:

            if hasattr(agent, "capabilities"):

                for capability in agent.capabilities:

                    if capability.lower() in command.raw.lower():

                        score += 20


        except Exception:
            pass



        return score