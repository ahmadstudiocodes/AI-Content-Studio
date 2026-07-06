from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Task:

    id: str

    name: str

    payload: dict

    status: str

    created: str

    @classmethod
    def create(cls, name, payload):

        return cls(

            id=str(uuid.uuid4()),

            name=name,

            payload=payload,

            status="waiting",

            created=datetime.now().isoformat()

        )