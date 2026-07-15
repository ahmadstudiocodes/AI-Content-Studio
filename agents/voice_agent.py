from agents.base.base_llm_agent import BaseLLMAgent



class VoiceAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Voice Agent


    Responsibilities:

    - Voice script preparation
    - Narration design
    - TTS direction
    - Voice style planning
    - Audio content structure
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="voice",

            description=
            "Professional Voice and Narration Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Voice Agent.

Your responsibility is voice content design.

Focus on:

- Narration scripts
- Voice tone
- Emotional delivery
- Speaking rhythm
- TTS preparation
- Audio structure


Never:

- Generate images
- Write articles
- Perform SEO analysis

"""

        )



        self.priority = 75



        self.domains = [

            "voice",

            "audio",

            "narration"

        ]



        self.capabilities = [

            "voice_script",

            "narration",

            "tts_preparation",

            "audio_direction"

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

            "voice",

            "صدا",

            "گویندگی",

            "نریشن",

            "tts",

            "راوی",

            "خواندن متن"

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


# Voice Goal


# Audience


# Voice Style


# Emotional Tone


# Speaking Speed


# Narration Script


# TTS Settings Recommendation



Rules:

- Answer in Persian.
- Make narration natural.
- Consider audience retention.

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