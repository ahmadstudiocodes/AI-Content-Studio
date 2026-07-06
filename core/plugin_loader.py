from pathlib import Path
import importlib


class PluginLoader:

    def __init__(self):

        self.plugins = []

    def load(self):

        path = Path("plugins")

        if not path.exists():

            return

        for file in path.glob("*.py"):

            if file.stem.startswith("_"):

                continue

            module = importlib.import_module(
                f"plugins.{file.stem}"
            )

            self.plugins.append(module)


plugin_loader = PluginLoader()