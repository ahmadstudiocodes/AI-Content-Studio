from agents.base.base_llm_agent import BaseLLMAgent


class PublishAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="publish",
            description="YouTube Publishing Assets Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Publish Agent.

Your ONLY responsibility is preparing YouTube publishing assets.

Focus on:

- SEO metadata
- Description
- Tags
- Hashtags
- Publishing strategy
- Audience engagement

Never:

- Rewrite scripts
- Create thumbnails
- Design courses
- Perform research
- Generate video ideas
"""
        )


        self.version = "2.2"


        self.priority = 70


        self.domains = [

            "publish",
            "publishing",
            "youtube",
            "seo"

        ]


        self.capabilities = [

            "publishing",
            "seo",
            "youtube_metadata",
            "tags",
            "description"

        ]



    def build_prompt(
        self,
        user_input
    ):

        return f"""
You are Arman StudioOS Publish Agent.


Previous Context:

{user_input}


Rules:

- Do NOT rewrite the script.
- Do NOT create thumbnail concepts.
- Do NOT redesign the course.
- Create SEO optimized publishing assets.
- Keep information practical.
- Use high CTR principles.


Return ONLY:


# SEO Title


# SEO Description


# YouTube Tags


# Hashtags


# Suggested Publish Time


# Pinned Comment


# Community Post


Answer ONLY in Persian.
"""