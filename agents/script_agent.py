from agents.base.base_llm_agent import BaseLLMAgent


class ScriptAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="script",
            description="Professional YouTube Lesson Script Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Script Agent.

Your ONLY responsibility:
Create professional lesson scripts from existing lesson plans.

You do NOT:
- create research
- create course structure
- create SEO
- create thumbnails
- create strategies

You only write the final teaching script.
"""
        )


        self.version = "3.4"

        self.priority = 40


        self.domains = [
            "script",
            "lesson",
            "training",
            "education",
            "narration"
        ]


        self.capabilities = [
            "lesson_script",
            "course_script",
            "voiceover",
            "narration"
        ]



    def build_prompt(
        self,
        user_input
    ):


        # Safety compression
        if len(user_input) > 3000:

            user_input = user_input[:3000]



        return f"""
You are Arman StudioOS Script Agent.


Create ONE professional YouTube lesson script.

Lesson information:

{user_input}


Requirements:

- Persian language only.
- Professional educational tone.
- Suitable for advanced 3D artists.
- Focus on practical teaching.
- Keep script around 800-1200 words.
- Do not generate unnecessary explanations.


Output format:


# Video Title


# Opening Hook


# Introduction


# Main Content


Section 1:

Narration:
...

Visual Suggestion:
...


Section 2:

Narration:
...

Visual Suggestion:
...


Section 3:

Narration:
...

Visual Suggestion:
...


# Call To Action


# Ending


Return ONLY the script.
"""