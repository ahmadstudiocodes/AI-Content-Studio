from agents.base.base_llm_agent import BaseLLMAgent


class MemoryAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="memory",
            description="Conversation Memory Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Memory Agent.

Your ONLY responsibility is memory management.

Focus on:

- Extracting important information
- Summarizing conversations
- Keeping long-term knowledge
- Removing unnecessary details
- Producing clean memory entries

Never:

- Generate scripts
- Design courses
- Create thumbnails
- Perform research
"""
        )

        self.version = "1.0"

        self.priority = 95

        self.domains = [
            "memory",
            "conversation",
            "knowledge"
        ]

        self.capabilities = [
            "memory",
            "summarization",
            "knowledge_extraction",
            "conversation_memory"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

CONVERSATION:

{user_input}

Rules:

- Extract only important information.
- Ignore small talk.
- Produce structured memory.
- Remove duplicate information.
- Keep memories concise.

Answer ONLY in Persian.
"""