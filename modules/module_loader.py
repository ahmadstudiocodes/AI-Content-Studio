from pathlib import Path


class ModuleLoader:

    def __init__(self):

        self.modules = []

    def scan(self):

        path = Path("modules")

        if not path.exists():
            return []

        self.modules = [
            p.name
            for p in path.iterdir()
            if p.is_dir()
        ]

        return self.modules


loader = ModuleLoader()