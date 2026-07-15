from agents.base.base_llm_agent import BaseLLMAgent



class SummarizerAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Summarization Agent


    Responsibilities:

    - Content summarization
    - Key point extraction
    - Information compression
    - Context reduction
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="summarizer",

            description=
            "Professional Content Summarization Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Summarizer Agent.

Your responsibility is summarizing information.

Focus on:

- Extracting important points
- Removing unnecessary details
- Preserving core meaning
- Creating concise summaries
- Organizing knowledge


Never:

- Add new information
- Change facts
- Write creative content

"""

        )


        self.priority = 70



        self.domains = [

            "summary",

            "knowledge",

            "compression"

        ]



        self.capabilities = [

            "summarization",

            "key_points",

            "content_compression",

            "knowledge_extraction"

        ]



    # =====================================================
    # Capability
    # =====================================================


    def has_capability(
        self,
        capability
    ):

        return capability in self.capabilities



    # =====================================================
    # Dispatcher
    # =====================================================


    def can_handle(
        self,
        user_input
    ):


        text = str(
            user_input
        ).lower()



        keywords = [

            "summary",

            "summarize",

            "خلاصه",

            "جمع بندی",

            "مختصر",

            "نکات اصلی"

        ]



        return any(

            key in text

            for key in keywords

        )



    # =====================================================
    # Prompt Builder
    # =====================================================


    def build_prompt(
        self,
        user_input
    ):


        return f"""

{self.system_prompt}


USER REQUEST:

{user_input}



Required Structure:


# خلاصه کلی


# نکات کلیدی


# اطلاعات مهم


# نتیجه گیری


# موارد قابل استفاده



Rules:

- Answer in Persian.
- Preserve important facts.
- Remove repetition.
- Keep structure clear.

"""



    # =====================================================
    # Post Processing
    # =====================================================


    def postprocess(
        self,
        response,
        user_input=None
    ):


        return super().postprocess(
            response,
            user_input
        )