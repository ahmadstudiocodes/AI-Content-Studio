from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryItem:

    category: str

    key: str

    value: str

    created: str = datetime.now().isoformat()