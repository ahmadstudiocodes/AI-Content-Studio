from agents.base.base_llm_agent import BaseLLMAgent



class ArticleAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Article Writer Agent


    Responsibilities:

    - Long form writing
    - Blog articles
    - Educational content
    - Technical articles
    - Structured documents
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="article",

            description=
            "Professional Article Writing Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Article Agent.

Your responsibility is writing professional articles.

Focus on:

- Clear structure
- Deep explanation
- Technical accuracy
- Reader engagement
- Educational value


Never:

- Write video scripts
- Create thumbnails
- Perform SEO strategy only

"""

        )



        self.priority = 85



        self.domains = [

            "article",

            "writing",

            "education"

        ]



        self.capabilities = [

            "article_writing",

            "long_form_content",

            "technical_writing",

            "documentation"

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

            "article",

            "مقاله",

            "بلاگ",

            "وبلاگ",

            "مطلب",

            "گزارش",

            "تحلیل مقاله"

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


# عنوان مقاله


# مقدمه


# بخش اول


# بخش دوم


# بخش سوم


# تحلیل و بررسی


# نتیجه گیری



Rules:

- Write in Persian.
- Maintain professional tone.
- Use clear headings.
- Explain concepts deeply.

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