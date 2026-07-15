from agents.base.base_llm_agent import BaseLLMAgent



class ImageAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Image Agent


    Responsibilities:

    - Image prompt creation
    - Visual analysis
    - Style direction
    - Image generation planning
    - Creative guidance
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="image",

            description=
            "Professional Image Generation Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Image Agent.

Your responsibility is image creation guidance.

Focus on:

- Visual concepts
- Image prompts
- Composition
- Lighting
- Materials
- Styles
- Camera direction


Never:

- Write articles
- Create video scripts
- Perform SEO optimization

"""

        )


        self.priority = 80



        self.domains = [

            "image",

            "visual",

            "creative"

        ]



        self.capabilities = [

            "image_prompt",

            "visual_analysis",

            "style_generation",

            "composition_design"

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

            "image",

            "تصویر",

            "عکس",

            "رندر",

            "render",

            "visual",

            "طراحی"

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


# Image Concept


# Subject


# Environment


# Style


# Camera


# Lighting


# Materials


# Color Palette


# Final Generation Prompt


# Negative Prompt



Rules:

- Answer in Persian.
- Make prompts detailed.
- Include visual specifications.
- Avoid vague descriptions.

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