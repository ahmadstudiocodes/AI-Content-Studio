class AgentRegistry:

    def __init__(self):
        self._agents = {}

    def register(self, name, agent):
        self._agents[name.lower()] = agent

    def get(self, name):
        return self._agents.get(name.lower())

    def all(self):
        return self._agents


registry = AgentRegistry()