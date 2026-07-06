from enum import Enum


class AgentState(Enum):

    IDLE = "idle"

    WAITING = "waiting"

    RUNNING = "running"

    SUCCESS = "success"

    FAILED = "failed"