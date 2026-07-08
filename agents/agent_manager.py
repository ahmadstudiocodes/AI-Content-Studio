from pathlib import Path
import importlib
import inspect

from agents.base_agent import BaseAgent
from core.registry import registry


class AgentManager:

    def __init__(self):

        self.agents = {}

        self.enabled_agents = [
            "thumbnail",
            "youtube",
            "architecture"
        ]

    def register(self, agent):

        name = agent.name.lower()

        self.agents[name] = agent

        registry.register(
            name,
            agent
        )

    def unregister(self, name):

        self.agents.pop(name.lower(), None)

        registry.unregister(name)

    def exists(self, name):

        return name.lower() in self.agents

    def discover(self):

        agents_path = Path(__file__).parent

        for file in agents_path.glob("*_agent.py"):

            module_name = file.stem

            try:

                module = importlib.import_module(
                    f"agents.{module_name}"
                )

                for _, obj in inspect.getmembers(
                    module,
                    inspect.isclass
                ):

                    if (
                        issubclass(obj, BaseAgent)
                        and obj is not BaseAgent
                    ):

                        agent = obj()

                        if agent.name in self.enabled_agents:

                            self.register(agent)

                            print(
                                f"[AGENT MANAGER] Loaded: {agent.name}"
                            )

            except Exception as e:

                print(
                    f"[AGENT MANAGER] Failed {module_name}: {e}"
                )

    def get(self, name):

        return self.agents.get(name.lower())

    def all(self):

        return self.agents

    def list(self):

        return list(self.agents.keys())

    def count(self):

        return len(self.agents)

    def clear(self):

        self.agents.clear()

    def status(self):

        return {
            "count": self.count(),
            "enabled": self.enabled_agents,
            "loaded": self.list()
        }


agent_manager = AgentManager()