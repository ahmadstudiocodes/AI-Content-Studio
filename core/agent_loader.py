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
            return

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

                    # فقط کلاس‌هایی که داخل همین فایل تعریف شده‌اند
                    if obj.__module__ != module.__name__:
                        continue

                    # فقط Agentها
                    if not issubclass(obj, BaseAgent):
                        continue

                    # خود BaseAgent
                    if obj is BaseAgent:
                        continue

                    # خود BaseLLMAgent
                    if obj.__name__ == "BaseLLMAgent":
                        continue

                    # کلاس‌های Abstract
                    if inspect.isabstract(obj):

                        print(
                            f"[AUTO REGISTRY] Skipped abstract: {obj.__name__}"
                        )

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
                        f"[AUTO REGISTRY] Loaded: {agent.name}"
                    )

            except Exception as e:

                print(
                    f"[AUTO REGISTRY] Failed: {module_name} ({e})"
                )

        print(
            f"[AUTO REGISTRY] Total Agents: {loaded}"
        )

        print("\n========== REGISTERED AGENTS ==========")

        for name, agent in registry.all().items():

            print(
                f"{name:<15} -> {agent.__class__.__name__}"
            )

        print("=======================================\n")


agent_loader = AgentLoader()