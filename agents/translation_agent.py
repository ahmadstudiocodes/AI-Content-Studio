from agents.base.base_llm_agent import BaseLLMAgent



class TranslationAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Translation Agent


    Responsibilities:

    - Content translation
    - Localization
    - Tone adaptation
    - Multilingual content
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="translation",

            description=
            "Professional Translation Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Translation Agent.

Your responsibility is professional translation.

Focus on:

- Meaning preservation
- Natural language
- Cultural adaptation
- Professional terminology
- Multiple languages


Never:

- Rewrite content unnecessarily
- Add unsupported information
- Change original meaning

"""

        )


        self.priority = 75



        self.domains = [

            "translation",

            "language",

            "localization"

        ]



        self.capabilities = [

            "translation",

            "localization",

            "language_adaptation",

            "multilingual_content"

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

            "translate",

            "translation",

            "ترجمه",

            "انگلیسی",

            "فارسی",

            "زبان",

            "english"

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


# Source Language


# Target Language


# Translation


# Terminology Notes


# Localization Suggestions



Rules:

- Preserve original meaning.
- Use natural language.
- Answer according to target audience.

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