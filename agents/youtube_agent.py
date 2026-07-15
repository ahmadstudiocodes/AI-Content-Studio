from agents.base.base_llm_agent import BaseLLMAgent


class YouTubeAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="youtube",
            description="Professional YouTube Content Strategy Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS YouTube Strategy Agent.

Your ONLY responsibility is creating YouTube content strategies.

Specialized in:

- 3ds Max
- Architecture Visualization
- V-Ray Rendering
- CGI Production

Your tasks:

- Generate professional video ideas
- Create optimized titles
- Design hooks
- Build video structures
- Improve audience retention

You do NOT create:

- Full scripts
- Thumbnails
- SEO metadata
- Publishing assets
"""
        )


        self.version = "1.6"


        self.priority = 50


        self.domains = [

            "youtube",
            "content",
            "strategy"

        ]


        self.capabilities = [

            "content_strategy",
            "video_idea",
            "title",
            "hook",
            "structure"

        ]



        self.channel_profile = """

Channel Name:

Easy Max / Arman StudioOS


Main Niche:

- Advanced 3ds Max Modeling
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
- Rendering Workflow
- V-Ray
- Architecture
- Visualization

"""



    def build_prompt(
        self,
        user_input
    ):

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
- Avoid outdated software information.
- Do not invent unknown V-Ray or 3ds Max features.


OUTPUT:


1. Video Idea


2. SEO Optimized Title


3. Powerful Hook (10 seconds)


4. Video Structure With Timing


5. Audience Retention Strategy


6. Production Notes


Maximum:

- Title: 1 option
- Hook: maximum 3 lines
- Structure: maximum 6 bullet points
- Production Notes: maximum 5 bullet points


"""
