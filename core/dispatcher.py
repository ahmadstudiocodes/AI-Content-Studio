from core.registry import registry
from core.scorer import AgentScorer


class Dispatcher:

    def __init__(self):

        self.scorer = AgentScorer()

    def route(self, command):

        agents = list(registry.all().values())

        if not agents:
            return f"No agents registered."

        candidates = []

        for agent in agents:

            try:

                score = self.scorer.score(
                    agent,
                    command
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
                    f"[DISPATCHER] {agent.name}: {e}"
                )

        if not candidates:

            return (
                f"Unknown Command : "
                f"{command.raw}"
            )

        candidates.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        score, agent = candidates[0]

        print(
            f"\n[DISPATCHER] Selected: {agent.name} ({score})\n"
        )

        return agent.run(command.payload or command.raw)


dispatcher = Dispatcher()