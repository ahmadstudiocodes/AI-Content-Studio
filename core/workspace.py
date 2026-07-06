from pathlib import Path


class Workspace:

    def __init__(self):

        self.root = Path.cwd()

    def path(self, *parts):

        return self.root.joinpath(*parts)

    def exists(self, *parts):

        return self.path(*parts).exists()


workspace = Workspace()