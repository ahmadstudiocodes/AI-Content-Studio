class AgentRegistry:

    def __init__(self):

        self.registry = {}

    def add(self, agent):

        self.registry[agent.name] = agent

    def get(self, name):

        return self.registry.get(name)

    def list(self):

        return list(self.registry.keys())


agent_registry = AgentRegistry()