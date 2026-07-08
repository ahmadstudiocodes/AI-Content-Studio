from pathlib import Path
import importlib
import inspect

from core.registry import registry
from agents.base_agent import BaseAgent


class AgentLoader:


    def load(self):

        agents_path = Path("agents")


        if not agents_path.exists():
            return



        for file in agents_path.glob("*_agent.py"):


            module_name = file.stem


            module = importlib.import_module(
                f"agents.{module_name}"
            )



            for name, obj in inspect.getmembers(
                module,
                inspect.isclass
            ):


                if (
                    issubclass(obj, BaseAgent)
                    and obj != BaseAgent
                ):

                    agent = obj()


                    registry.register(
                        agent.name,
                        agent
                    )


                    print(
                        f"[AUTO REGISTRY] Loaded: {agent.name}"
                    )



agent_loader = AgentLoader()