import json
from pathlib import Path


class Settings:

    def __init__(self):

        self.file = Path("config/settings.json")

    def load(self):

        if not self.file.exists():

            self.file.parent.mkdir(exist_ok=True)

            self.file.write_text(
                json.dumps(
                    {
                        "language": "fa",
                        "theme": "dark",
                        "version": "0.1.0"
                    },
                    indent=4
                ),
                encoding="utf-8"
            )

        return json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )


settings = Settings()