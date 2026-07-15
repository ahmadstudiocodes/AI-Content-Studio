from agents.base.base_llm_agent import BaseLLMAgent



class SEOAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional SEO Agent


    Responsibilities:

    - Keyword analysis
    - SEO optimization
    - Title generation
    - Description writing
    - Content improvement
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="seo",

            description=
            "Professional SEO Optimization Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS SEO Agent.

Your responsibility is SEO optimization.

Focus on:

- Keyword research
- Search intent analysis
- Content optimization
- Titles
- Descriptions
- Ranking improvement


Never:

- Write complete articles
- Create scripts
- Generate images

"""

        )



        self.priority = 85



        self.domains = [

            "seo",

            "marketing",

            "optimization"

        ]



        self.capabilities = [

            "keyword_research",

            "seo_analysis",

            "title_generation",

            "content_optimization"

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

            "seo",

            "سئو",

            "keyword",

            "کلمه کلیدی",

            "رتبه",

            "گوگل",

            "بهینه سازی",

            "عنوان"

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



Required Output:


# Search Intent


# Target Keywords


# Related Keywords


# SEO Title Suggestions


# Meta Description


# Content Improvement


# Ranking Recommendations



Rules:

- Answer in Persian.
- Focus on practical SEO.
- Separate keywords from suggestions.

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