from agents.base.base_llm_agent import BaseLLMAgent


class PublishingAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="publish",
            description="Workflow Publishing Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Publishing Agent.

Prepare ONLY YouTube publishing assets.

Never:
- Rewrite scripts
- Create thumbnails
- Redesign courses
"""
        )

        self.version = "2.1"

        self.priority = 70

        self.domains = [
            "youtube",
            "publishing",
            "marketing"
        ]

        self.capabilities = [
            "publishing",
            "seo",
            "youtube_metadata"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

Previous Context:

{user_input}

Rules:

- Do NOT rewrite the script.
- Do NOT redesign the course.
- Do NOT create thumbnails.
- Keep the output concise.
- SEO optimized.
- High CTR.

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


publishing_agent = None