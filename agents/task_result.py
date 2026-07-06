from dataclasses import dataclass


@dataclass
class TaskResult:

    success: bool

    output: object = None

    error: str = ""