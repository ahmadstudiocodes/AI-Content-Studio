from agents.base.base_llm_agent import BaseLLMAgent


class ScriptWriterAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Script Writer Agent

    Responsibilities:

    - Video scripts
    - Story structure
    - Hooks
    - Narration
    - Content flow
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="script_writer",

            description=
            "Professional Script Writing Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Script Writer Agent.

Your responsibility is creating professional scripts.

Focus on:

- Storytelling
- Audience retention
- Strong hooks
- Clear structure
- Engaging narration


Never:

- Perform deep research
- Design thumbnails
- Optimize SEO keywords

"""

        )



        self.priority = 90



        self.domains = [

            "script",

            "story",

            "content"

        ]



        self.capabilities = [

            "script_writing",

            "storytelling",

            "video_structure",

            "hook_generation"

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

            "script",

            "سناریو",

            "اسکریپت",

            "متن ویدیو",

            "داستان",

            "هوک",

            "hook"

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


# عنوان


# Hook اولیه


# مقدمه


# بدنه اصلی


# نقاط حفظ مخاطب


# پایان بندی


# CTA



Write in Persian.

"""



    # =====================================================
    # Post Process
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