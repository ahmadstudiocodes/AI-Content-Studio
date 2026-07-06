import json
from pathlib import Path


class ConfigService:

    def __init__(self):

        self.cache = {}

    def load(self, filename):

        file = Path("config") / filename

        if not file.exists():
            return {}

        if filename not in self.cache:

            self.cache[filename] = json.loads(
                file.read_text(encoding="utf-8")
            )

        return self.cache[filename]

    def save(self, filename, data):

        file = Path("config") / filename

        file.parent.mkdir(exist_ok=True)

        file.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        self.cache[filename] = data


config = ConfigService()