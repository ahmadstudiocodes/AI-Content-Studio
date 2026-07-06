import json
from pathlib import Path


class VersionManager:

    def __init__(self):
        self.file = Path("config/version.json")

    def get(self):

        if not self.file.exists():
            return "0.0.0"

        data = json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

        return data.get("version", "0.0.0")


version = VersionManager()