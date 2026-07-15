from agents.base.base_llm_agent import BaseLLMAgent



class ThumbnailAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Thumbnail Agent


    Responsibilities:

    - Thumbnail concepts
    - CTR optimization
    - Visual direction
    - Image prompts
    - YouTube thumbnail strategy
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="thumbnail",

            description=
            "Professional YouTube Thumbnail Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Thumbnail Agent.

Your responsibility is creating
high-performing thumbnail concepts.

Focus on:

- Click Through Rate (CTR)
- Visual hierarchy
- Contrast
- Curiosity
- Audience psychology
- Professional composition


Never:

- Write full scripts
- Perform deep research
- Create final images

"""

        )


        self.priority = 90



        self.domains = [

            "thumbnail",

            "youtube",

            "visual_design"

        ]



        self.capabilities = [

            "thumbnail_design",

            "ctr_optimization",

            "image_prompt",

            "visual_strategy"

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

            "thumbnail",

            "کاور",

            "تامبنیل",

            "تصویر یوتیوب",

            "youtube thumbnail",

            "کاور ویدیو"

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


# Thumbnail Concept


# Main Visual


# Composition


# Text Placement


# Color Strategy


# CTR Psychology


# Image Generation Prompt


# Negative Prompt



Rules:

- Answer in Persian.
- Focus on professional YouTube thumbnails.
- Keep text minimal.
- Prioritize visual impact.

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