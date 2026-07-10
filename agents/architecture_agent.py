from agents.base.base_llm_agent import BaseLLMAgent


class ArchitectureAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="architecture",
            description="Software Architecture Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Architecture Agent.

Your ONLY responsibility is software architecture.

Focus on:

- System Design
- Folder Structure
- Class Design
- Design Patterns
- SOLID Principles
- Scalability
- Maintainability

Never generate:

- YouTube content
- Thumbnail ideas
- Scripts
- Marketing content
"""
        )

        self.version = "1.0"

        self.priority = 100

        self.domains = [
            "architecture",
            "software",
            "design"
        ]

        self.capabilities = [
            "system_design",
            "software_architecture",
            "folder_structure",
            "class_design",
            "refactoring"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Answer ONLY as a software architect.
- Use clean architecture principles.
- Follow SOLID.
- Avoid unnecessary complexity.
- Prefer scalable solutions.
- Keep responsibilities separated.

Answer ONLY in Persian.
"""