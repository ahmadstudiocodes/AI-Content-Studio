from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Any


@dataclass
class FailoverResult:

    success: bool

    provider: str | None = None

    data: Any = None



class RuntimeFailoverManager:
    """
    Provider failover controller.
    """


    def execute(
        self,
        providers: List[tuple[str, Callable]],
    ) -> FailoverResult:


        for name, provider in providers:

            try:

                result = provider()


                return FailoverResult(
                    success=True,
                    provider=name,
                    data=result,
                )


            except Exception:

                continue



        return FailoverResult(
            success=False
        )



runtime_failover_manager = RuntimeFailoverManager()