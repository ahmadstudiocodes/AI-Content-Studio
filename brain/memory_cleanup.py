# brain/memory_cleanup.py

import time
from copy import deepcopy

from brain.executive_memory import executive_memory


class MemoryCleanup:
    """
    Arman StudioOS Memory Cleanup

    Responsibilities
    ----------------
    • Remove expired memory (TTL)
    • Limit history size
    • Remove empty values
    • Reduce memory footprint
    """

    DEFAULT_TTL = 3600
    MAX_HISTORY = 50

    def cleanup(
        self,
        ttl=None
    ):
        """
        Execute all cleanup operations.
        """

        if ttl is None:
            ttl = self.DEFAULT_TTL

        self.remove_expired(ttl)
        self.trim_history()
        self.remove_empty()

    def remove_expired(
        self,
        ttl
    ):
        """
        Remove expired entries.
        """

        memory = executive_memory.snapshot()

        now = time.time()

        for key in list(memory.keys()):

            value = memory[key]

            if not isinstance(value, dict):
                continue

            timestamp = value.get("timestamp")

            if timestamp is None:
                continue

            if now - timestamp > ttl:
                executive_memory.delete(key)

    def trim_history(self):
        """
        Keep only recent history.
        """

        memory = executive_memory.snapshot()

        history = memory.get(
            "history",
            []
        )

        if len(history) > self.MAX_HISTORY:

            executive_memory.set(
                "history",
                history[-self.MAX_HISTORY:]
            )

    def remove_empty(self):
        """
        Remove empty values.
        """

        memory = executive_memory.snapshot()

        for key, value in list(memory.items()):

            if value in (
                None,
                "",
                [],
                {}
            ):
                executive_memory.delete(key)

    def compact(self):
        """
        Compact memory.
        """

        memory = deepcopy(
            executive_memory.snapshot()
        )

        compacted = {}

        for key, value in memory.items():

            if isinstance(value, str):
                value = value.strip()

            compacted[key] = value

        executive_memory.clear()

        for key, value in compacted.items():
            executive_memory.set(
                key,
                value
            )


memory_cleanup = MemoryCleanup()