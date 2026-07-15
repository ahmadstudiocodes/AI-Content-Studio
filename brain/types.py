from dataclasses import dataclass
from enum import Enum



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