from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# =====================================
# Brain Complexity
# =====================================

class Complexity(Enum):

    SIMPLE = "simple"

    COMPLEX = "complex"


# =====================================
# Execution Mode
# =====================================

class ExecutionMode(Enum):

    DIRECT = "direct"

    WORKFLOW = "workflow"


# =====================================
# Reasoning Result
# =====================================

@dataclass
class ReasoningResult:

    goal: str

    complexity: Complexity

    requires_memory: bool

    requires_planner: bool

    requires_workflow: bool

    execution: ExecutionMode


# =====================================
# Workflow Task
# =====================================

@dataclass
class Task:

    name: str

    status: str = "pending"

    result: Any = None


# =====================================
# Execution Plan
# =====================================

@dataclass
class ExecutionPlan:

    goal: str

    tasks: list = field(
        default_factory=list
    )

    status: str = "created"

    # Compatibility with older code
    @property
    def steps(self):

        return self.tasks

    def add_task(
        self,
        task
    ):

        self.tasks.append(task)

    def complete(self):

        self.status = "completed"