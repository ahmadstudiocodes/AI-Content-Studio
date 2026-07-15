"""
Arman StudioOS

Enterprise Hook Manager
"""

from __future__ import annotations

import traceback

from collections import defaultdict
from typing import Callable, Dict, List


# ============================================================
# Hook Types
# ============================================================

BEFORE = "before"

AFTER = "after"

ERROR = "error"

STARTUP = "startup"

SHUTDOWN = "shutdown"


# ============================================================
# Hook Manager
# ============================================================

class HookManager:

    def __init__(self):

        self._hooks: Dict[
            str,
            List[Callable]
        ] = defaultdict(list)

    # ========================================================

    def register(
        self,
        hook_type: str,
        callback: Callable
    ):

        self._hooks[
            hook_type
        ].append(
            callback
        )

    # ========================================================

    def unregister(
        self,
        hook_type: str,
        callback: Callable
    ):

        if callback in self._hooks[
            hook_type
        ]:

            self._hooks[
                hook_type
            ].remove(
                callback
            )

    # ========================================================

    def execute(
        self,
        hook_type: str,
        *args,
        **kwargs
    ):

        results = []

        for callback in self._hooks.get(
            hook_type,
            []
        ):

            try:

                results.append(

                    callback(
                        *args,
                        **kwargs
                    )

                )

            except Exception:

                traceback.print_exc()

        return results

    # ========================================================

    def clear(
        self,
        hook_type: str = None
    ):

        if hook_type is None:

            self._hooks.clear()

            return

        self._hooks[
            hook_type
        ].clear()

    # ========================================================

    def has_hooks(
        self,
        hook_type: str
    ):

        return (

            len(

                self._hooks.get(

                    hook_type,

                    []

                )

            )

            > 0

        )

    # ========================================================

    def count(
        self,
        hook_type: str = None
    ):

        if hook_type is None:

            return sum(

                len(v)

                for v

                in self._hooks.values()

            )

        return len(

            self._hooks.get(

                hook_type,

                []

            )

        )

    # ========================================================

    def registered_hooks(self):

        return {

            key: len(value)

            for key, value

            in self._hooks.items()

        }


# ============================================================
# Singleton
# ============================================================

hook_manager = HookManager()