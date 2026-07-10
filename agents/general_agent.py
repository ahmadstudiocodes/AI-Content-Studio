from agents.base.base_llm_agent import BaseLLMAgent


class GeneralAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="general",
            description="General Purpose Assistant",
            provider=provider,
            system_prompt="""
You are Arman StudioOS General Agent.

You handle requests that do not belong to any specialized agent.

Focus on:

- General questions
- Explanations
- Brainstorming
- Problem solving
- Professional assistance

Never pretend to be a specialized agent when one is required.
"""
        )

        self.version = "1.0"

        self.priority = 10

        self.domains = [
            "general",
            "assistant"
        ]

        self.capabilities = [
            "general_chat",
            "brainstorm",
            "explanation",
            "problem_solving"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Give clear and practical answers.
- Be concise.
- If the request belongs to another specialized agent, state that.
- Answer ONLY in Persian.
"""