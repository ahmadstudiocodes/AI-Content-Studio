from agents.base.base_llm_agent import BaseLLMAgent


class PlannerAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="planner",
            description="Task Planning Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Planner Agent.

Your ONLY responsibility is planning.

Focus on:

- Breaking goals into tasks
- Prioritization
- Dependencies
- Workflow
- Execution Roadmap

Never:

- Write scripts
- Generate thumbnails
- Perform research
- Design courses
"""
        )

        self.version = "1.0"

        self.priority = 95

        self.domains = [
            "planning",
            "workflow",
            "tasks"
        ]

        self.capabilities = [
            "planning",
            "roadmap",
            "task_breakdown",
            "workflow_design"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Break the goal into clear steps.
- Show dependencies.
- Prioritize tasks.
- Keep the workflow practical.
- Do not perform research.
- Do not write scripts.

Answer ONLY in Persian.
"""