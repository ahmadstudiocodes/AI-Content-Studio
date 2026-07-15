from agents.base.base_llm_agent import BaseLLMAgent

from brain.agent_result import AgentResult

from brain.research_cache import research_cache
from brain.research_manager import research_manager
from brain.source_validator import source_validator
from brain.fact_checker import fact_checker



class ResearchAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Research Agent


    Responsibilities:

    - Research
    - Analysis
    - Fact extraction
    - Knowledge summary
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="research",

            description=
            "Professional Research Agent",

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

            "research",

            "تحقیق",

            "بررسی",

            "تحلیل",

            "اطلاعات",

            "منبع",

            "مقایسه"

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


        cached = research_cache.get(
            user_input
        )



        if cached:


            return f"""

Previous research exists.


Topic:

{user_input}


Improve and verify previous knowledge.

"""



        return f"""

{self.system_prompt}


USER REQUEST:

{user_input}


Research Rules:

- Research only.
- Separate facts from assumptions.
- Use structured sections.
- Answer only in Persian.


Required Structure:


# خلاصه تحقیق


# نکات کلیدی


# اطلاعات مهم


# تحلیل


# منابع پیشنهادی

"""



    # =====================================================
    # Output Processing
    # =====================================================


    def postprocess(
        self,
        response,
        user_input=None
    ):


        cleaned = super().postprocess(
            response,
            user_input
        )



        if not cleaned:

            return ""



        package = research_manager.research(

            topic=
            user_input or "research"

        )



        package.summary = cleaned



        package = source_validator.validate(
            package
        )



        package = fact_checker.check(
            package
        )



        research_cache.save(
            package
        )



        return cleaned