from agents.base.base_llm_agent import BaseLLMAgent


class YouTubeAgent(BaseLLMAgent):


    def __init__(self, provider):

        super().__init__(
            name="youtube",
            description="Professional YouTube Content Generator",
            provider=provider,
            system_prompt="""
You are Arman StudioOS YouTube Content Agent.

You are an expert YouTube strategist specialized in:
- 3ds Max
- Architecture Visualization
- V-Ray Rendering
- CGI Production

Your goal is creating professional YouTube content plans.
"""
        )


        self.version = "1.5"

        self.priority = 50


        self.domains = [
            "youtube",
            "video",
            "content"
        ]


        self.capabilities = [
            "generate",
            "title",
            "script",
            "thumbnail",
            "seo"
        ]



        self.channel_profile = """

Channel Name:
Easy Max / Arman StudioOS


Main Niche:

- 3ds Max Advanced Modeling
- Architecture Visualization
- V-Ray Rendering
- CGI Production
- Professional 3D Tutorials


Audience:

- Architects
- Interior Designers
- 3D Artists
- Architecture Students
- Visualization Professionals


Content Style:

- Professional
- Technical
- Advanced
- Practical
- Project Based


Avoid:

- Generic AI topics
- Beginner tutorials
- Unrelated technology
- Motivational content


Focus:

- Advanced Modeling
- Rendering
- V-Ray
- Architecture
- Visualization
- Professional Workflow

"""



    def build_prompt(self, user_input):

        return f"""

{self.channel_profile}


USER REQUEST:

{user_input}



RULES:


LANGUAGE:

- Answer ONLY in Persian.


CONTENT:

- Stay inside the channel niche.
- Create realistic professional ideas.
- Avoid fake technical information.
- Avoid outdated software versions.
- Do not invent unknown V-Ray or 3ds Max features.



FORMAT:

You MUST complete all 7 sections.

Never stop before section 7.

Keep every section concise.

Maximum:
- Title: 1 option
- Hook: maximum 3 lines
- Structure: maximum 6 bullet points
- Script Outline: maximum 8 bullet points
- Scene Suggestions: maximum 5 bullet points
- Thumbnail Concept: maximum 5 bullet points
- SEO Keywords: maximum 10 keywords



OUTPUT:


1. SEO Optimized Video Title


2. Powerful Hook (10 seconds)


3. Video Structure with timing


4. Script Outline


5. Scene Suggestions


6. Thumbnail Concept


7. SEO Keywords and Tags


"""