from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class RecoveryResult:

    recovered: bool

    data: Any = None

    attempts: int = 0



class RuntimeRecoveryManager:
    """
    Runtime recovery controller.
    """


    def recover(
        self,
        operation: Callable,
        retries: int = 1
    ) -> RecoveryResult:


        attempts = 0


        while attempts <= retries:

            try:

                result = operation()

                return RecoveryResult(
                    recovered=True,
                    data=result,
                    attempts=attempts + 1,
                )


            except Exception:

                attempts += 1



        return RecoveryResult(
            recovered=False,
            attempts=attempts,
        )



runtime_recovery_manager = (
    RuntimeRecoveryManager()
)