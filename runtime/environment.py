from __future__ import annotations

from enum import Enum


class RuntimeEnvironment(Enum):

    DEVELOPMENT = "development"

    TESTING = "testing"

    PRODUCTION = "production"



class EnvironmentManager:
    """
    Runtime environment manager.
    """


    def __init__(
        self,
        environment: RuntimeEnvironment =
            RuntimeEnvironment.DEVELOPMENT
    ):

        self.environment = environment



    def is_production(self):

        return (
            self.environment
            ==
            RuntimeEnvironment.PRODUCTION
        )



    def current(self):

        return self.environment.value



runtime_environment = EnvironmentManager()