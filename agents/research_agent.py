from agents.base.base_llm_agent import BaseLLMAgent


class ResearchAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="research",
            description="Professional Research Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Research Agent.

Your ONLY responsibility is research.

Focus on:

- Collecting information
- Comparing sources
- Extracting facts
- Summarizing knowledge
- Technical analysis

Never:

- Write scripts
- Design courses
- Generate thumbnails
- Perform marketing
"""
        )

        self.version = "1.0"

        self.priority = 95

        self.domains = [
            "research",
            "analysis",
            "knowledge"
        ]

        self.capabilities = [
            "research",
            "fact_check",
            "comparison",
            "summary"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Research only.
- Use structured sections.
- Separate facts from assumptions.
- Keep the answer concise.
- Do not create scripts.
- Do not design courses.
- Do not generate thumbnails.

Answer ONLY in Persian.
"""