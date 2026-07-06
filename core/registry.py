class AgentRegistry:

    def __init__(self):

        self._agents = {}

    def register(self, name, agent):

        self._agents[name.lower()] = agent

    def unregister(self, name):

        self._agents.pop(name.lower(), None)

    def get(self, name):

        return self._agents.get(name.lower())

    def exists(self, name):

        return name.lower() in self._agents

    def all(self):

        return self._agents

    def count(self):

        return len(self._agents)


registry = AgentRegistry()