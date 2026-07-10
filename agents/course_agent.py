from agents.base.base_llm_agent import BaseLLMAgent


class CourseAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="course",
            description="Professional Course Design Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Course Agent.

Your ONLY responsibility is designing professional educational courses.

Focus on:

- Course Structure
- Learning Path
- Module Planning
- Lesson Sequence
- Learning Objectives
- Prerequisites

Never generate:

- Scripts
- Thumbnails
- SEO
- Research
- Marketing
"""
        )

        self.version = "1.0"

        self.priority = 90

        self.domains = [
            "education",
            "course",
            "training"
        ]

        self.capabilities = [
            "course_design",
            "curriculum",
            "lesson_plan",
            "learning_path"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Design a complete professional course.
- Organize content into logical modules.
- Define learning objectives.
- Include prerequisites when needed.
- Do not write lesson scripts.
- Do not create thumbnails.
- Do not perform research.

Answer ONLY in Persian.
"""