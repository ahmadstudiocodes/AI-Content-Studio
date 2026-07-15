from agents.base.base_llm_agent import BaseLLMAgent


class MemoryAgent(BaseLLMAgent):

    """
    Arman StudioOS Memory Agent

    Responsible for:

    - Extracting important memories
    - Summarizing information
    - Preparing clean memory entries

    Does NOT:
    
    - Execute workflows
    - Create content
    - Generate designs
    """



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="memory",

            description=
                "Conversation Memory Extraction Agent",

            provider=provider,


            system_prompt="""

You are Arman StudioOS Memory Agent.

Your ONLY responsibility is memory extraction.

Responsibilities:

- Extract important information
- Summarize conversations
- Identify reusable knowledge
- Remove unnecessary details
- Create structured memory entries


Never:

- Generate scripts
- Design courses
- Create thumbnails
- Perform research
- Answer normal user requests


Memory priority:

1. Long-term useful facts
2. Project decisions
3. User preferences
4. Important constraints


Ignore:

- Small talk
- Temporary details
- Repeated information

"""

        )



        self.version = "1.1"


        self.priority = 70


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



    # ==================================================

    def build_prompt(
        self,
        user_input
    ):


        return f"""

{self.system_prompt}


CONVERSATION:

{user_input}


OUTPUT FORMAT:


CATEGORY:

KEY:

MEMORY:

IMPORTANCE:


Rules:

- Extract only important information.
- Keep memory concise.
- Avoid duplicate information.
- Do not explain your reasoning.
- Answer ONLY in Persian.

"""