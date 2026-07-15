from agents.base.base_llm_agent import BaseLLMAgent



class VideoPlannerAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Video Planning Agent


    Responsibilities:

    - Video structure
    - Scene planning
    - Shot breakdown
    - Production workflow
    - Timeline design
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="video_planner",

            description=
            "Professional Video Planning Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Video Planner Agent.

Your responsibility is planning video production.

Focus on:

- Video structure
- Scene design
- Shot planning
- Timing
- Production workflow
- Audience retention


Never:

- Write final scripts
- Generate images
- Perform SEO analysis

"""

        )



        self.priority = 85



        self.domains = [

            "video",

            "production",

            "planning"

        ]



        self.capabilities = [

            "video_planning",

            "scene_design",

            "shot_list",

            "production_workflow"

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

            "video",

            "ویدیو",

            "ویدئو",

            "ساخت فیلم",

            "سناریوی تصویری",

            "shot",

            "scene",

            "سکانس"

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


# Video Goal


# Target Audience


# Video Structure


# Scene Breakdown


# Shot List


# Timeline


# Required Assets


# Production Notes



Rules:

- Answer in Persian.
- Make production practical.
- Think like a professional video producer.

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