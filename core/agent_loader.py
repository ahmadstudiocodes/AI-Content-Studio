from pathlib import Path
import importlib
import inspect

from agents.base_agent import BaseAgent
from core.registry import registry
from providers.local_provider import LocalProvider


class AgentLoader:

    def __init__(self):

        self.provider = LocalProvider()

    def load(self):

        agents_path = Path("agents")

        if not agents_path.exists():

            print("[AGENT LOADER] Agents folder not found.")
            return

        loaded = 0

        registry.clear()

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

                    # فقط کلاس‌های تعریف شده در همین فایل
                    if obj.__module__ != module.__name__:
                        continue

                    # فقط Agentها
                    if not issubclass(obj, BaseAgent):
                        continue

                    # خود BaseAgent
                    if obj is BaseAgent:
                        continue

                    # کلاس Abstract
                    if inspect.isabstract(obj):
                        continue

                    try:

                        agent = obj(self.provider)

                    except TypeError:

                        agent = obj()

                    registry.register(
                        agent.name,
                        agent
                    )

                    loaded += 1

                    print(
                        f"[AGENT LOADER] Loaded: {agent.name}"
                    )

            except Exception as e:

                print(
                    f"[AGENT LOADER] Failed: {module_name} ({e})"
                )

        print(
            f"[AGENT LOADER] Total Agents: {loaded}"
        )


agent_loader = AgentLoader()