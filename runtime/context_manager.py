from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Optional

from runtime.context import RuntimeContext


class RuntimeContextManager:
    """
    Runtime Context Lifecycle Manager

    Responsibilities:
    - Context creation
    - Context binding
    - Context stack management
    - Thread isolation
    - Cleanup
    """

    def __init__(self):

        self._local = threading.local()

    def _get_stack(self):

        if not hasattr(
            self._local,
            "stack",
        ):
            self._local.stack = []

        return self._local.stack

    def current(
        self,
    ) -> Optional[RuntimeContext]:

        stack = self._get_stack()

        if stack:
            return stack[-1]

        return None

    def push(
        self,
        context: RuntimeContext,
    ) -> RuntimeContext:

        stack = self._get_stack()

        stack.append(context)

        return context

    def pop(
        self,
    ) -> Optional[RuntimeContext]:

        stack = self._get_stack()

        if not stack:
            return None

        return stack.pop()

    def clear(
        self,
    ) -> None:

        stack = self._get_stack()

        stack.clear()

    def cleanup(
        self,
    ) -> None:
        """
        Release all runtime contexts for
        the current thread.
        """

        self.clear()

        if hasattr(
            self._local,
            "stack",
        ):
            del self._local.stack

    @property
    def depth(
        self,
    ) -> int:

        return len(
            self._get_stack()
        )

    @contextmanager
    def scope(
        self,
        context: RuntimeContext,
    ):

        self.push(context)

        try:

            yield context

        finally:

            self.pop()

            if self.depth == 0:
                self.cleanup()


runtime_context_manager = RuntimeContextManager()