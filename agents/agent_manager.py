from pathlib import Path
import importlib
import inspect

from agents.base_agent import BaseAgent
from core.registry import registry
from providers.local_provider import LocalProvider


class AgentManager:

    def __init__(self):

        self.agents = {}

        self.provider = LocalProvider()

    def register(self, agent):

        name = agent.name.lower()

        self.agents[name] = agent

        registry.register(name, agent)

    def unregister(self, name):

        name = name.lower()

        self.agents.pop(name, None)

        registry.unregister(name)

    def discover(self):

        agents_path = Path(__file__).parent

        loaded = 0

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

                        try:
                            agent = obj(self.provider)
                        except TypeError:
                            agent = obj()

                        self.register(agent)

                        loaded += 1

                        print(
                            f"[AGENT MANAGER] Loaded: {agent.name}"
                        )

            except Exception as e:

                print(
                    f"[AGENT MANAGER] Failed {module_name}: {e}"
                )

        print(
            f"[AGENT MANAGER] Total: {loaded}"
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
            "loaded": self.list()
        }


agent_manager = AgentManager()