from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Callable



class HealthStatus(Enum):

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"



@dataclass
class ComponentHealth:

    name: str

    status: HealthStatus

    message: str = ""



class RuntimeHealthManager:
    """
    Runtime health monitoring.
    """


    def __init__(self):

        self.checks: Dict[
            str,
            Callable
        ] = {}



    def register_check(
        self,
        name: str,
        check: Callable
    ):

        self.checks[name] = check



    def check_health(self):

        results = []


        for name, check in self.checks.items():

            try:

                result = check()


                results.append(
                    ComponentHealth(
                        name=name,
                        status=(
                            HealthStatus.HEALTHY
                            if result
                            else HealthStatus.DEGRADED
                        ),
                    )
                )


            except Exception as exc:

                results.append(
                    ComponentHealth(
                        name=name,
                        status=HealthStatus.UNHEALTHY,
                        message=str(exc),
                    )
                )


        return results



runtime_health_manager = RuntimeHealthManager()