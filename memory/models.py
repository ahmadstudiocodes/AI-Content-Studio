from dataclasses import dataclass, field
from datetime import datetime



@dataclass
class MemoryItem:

    """
    Arman StudioOS Memory Item

    Represents one stored memory entry.
    """

    category: str

    key: str

    value: str


    created: str = field(
        default_factory=lambda:
            datetime.now().isoformat()
    )



    def __post_init__(self):

        self.category = str(
            self.category or "general"
        )


        self.key = str(
            self.key
        )


        self.value = str(
            self.value
        )