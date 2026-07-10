from agents.base.base_llm_agent import BaseLLMAgent


class VideoAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="video",
            description="Professional Video Production Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Video Agent.

Your ONLY responsibility is video production.

Focus on:

- Video structure
- Scene planning
- Shot list
- B-Roll
- Camera movement
- Editing workflow

Never:

- Design thumbnails
- Write complete lesson scripts
- Perform research
- Design courses
"""
        )

        self.version = "1.0"

        self.priority = 85

        self.domains = [
            "video",
            "editing",
            "production"
        ]

        self.capabilities = [
            "video_plan",
            "shot_list",
            "scene_design",
            "editing_workflow"
        ]

    def build_prompt(self, user_input):

        return f"""
{self.system_prompt}

USER REQUEST:

{user_input}

Rules:

- Create a professional video production plan.
- Organize scenes logically.
- Include camera suggestions.
- Include editing suggestions.
- Do not write a full script.
- Keep the output practical.

Answer ONLY in Persian.
"""