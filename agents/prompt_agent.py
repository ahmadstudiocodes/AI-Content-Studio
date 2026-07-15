from agents.base.base_llm_agent import BaseLLMAgent



class PromptAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Prompt Engineering Agent


    Responsibilities:

    - Prompt generation
    - Prompt optimization
    - AI instruction design
    - Model-specific prompts
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="prompt",

            description=
            "Professional Prompt Engineering Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Prompt Agent.

Your responsibility is designing
high quality AI prompts.

Focus on:

- Clear instructions
- Context engineering
- Output formatting
- Model optimization
- Creative direction


Never:

- Execute image generation
- Write complete articles
- Perform final editing

"""

        )



        self.priority = 80



        self.domains = [

            "prompt",

            "ai",

            "generation"

        ]



        self.capabilities = [

            "prompt_engineering",

            "prompt_optimization",

            "instruction_design",

            "model_prompting"

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

            "prompt",

            "پرامپت",

            "دستور",

            "متن تولید",

            "برای هوش مصنوعی",

            "بهینه سازی پرامپت"

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


# Goal


# Role


# Context


# Instructions


# Constraints


# Output Format


# Final Optimized Prompt



Rules:

- Answer in Persian.
- Make prompts precise.
- Remove ambiguity.
- Include useful constraints.

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