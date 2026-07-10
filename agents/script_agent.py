from agents.base.base_llm_agent import BaseLLMAgent


class ScriptAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="script",
            description="Professional YouTube Lesson Script Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Script Agent.

Your ONLY responsibility is writing complete lesson scripts.

You NEVER create:
- YouTube ideas
- Video titles
- SEO
- Thumbnails
- Content plans

Those belong to YouTubeAgent.

You ONLY write the final lesson script based on an existing topic or plan.
"""
        )

        self.version = "3.2"

        # پایین‌تر از YouTubeAgent
        self.priority = 25

        # عمداً youtube حذف شده
        self.domains = [
            "script",
            "lesson",
            "course",
            "training",
            "education",
            "narration"
        ]

        self.capabilities = [
            "lesson_script",
            "course_script",
            "training_script",
            "narration",
            "voiceover"
        ]

    def build_prompt(self, user_input):

        return f"""
You are Arman StudioOS Script Agent.

Write ONE complete YouTube lesson script.

Previous Context:

{user_input}

Rules:

- Do NOT generate YouTube ideas.
- Do NOT generate titles.
- Do NOT generate SEO.
- Do NOT generate thumbnails.
- Do NOT redesign the course.
- Write ONE complete lesson only.
- Focus on audience retention.
- Answer ONLY in Persian.

Return ONLY:

# Video Title

# Opening Hook

# Introduction

# Main Content

For every section include:

- Narration
- Visual Suggestion

# Call To Action

# Ending
"""