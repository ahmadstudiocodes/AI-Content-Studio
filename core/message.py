from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:

    sender: str

    receiver: str

    content: str

    created: str = datetime.now().isoformat()