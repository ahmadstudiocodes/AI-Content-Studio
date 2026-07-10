from agents.base.base_llm_agent import BaseLLMAgent


class ThumbnailAgent(BaseLLMAgent):

    def __init__(self, provider):

        super().__init__(
            name="thumbnail",
            description="Workflow YouTube Thumbnail Agent",
            provider=provider,
            system_prompt="""
You are Arman StudioOS Thumbnail Agent.

Your ONLY responsibility is creating professional YouTube thumbnails.

Never:
- write scripts
- perform research
- redesign courses
- answer general questions

Only create thumbnail concepts.
"""
        )

        self.version = "2.2"

        self.priority = 80

        self.domains = [
            "youtube",
            "thumbnail",
            "cover",
            "image"
        ]

        self.capabilities = [
            "thumbnail",
            "thumbnail_design",
            "image_prompt",
            "youtube_cover"
        ]

    def build_prompt(self, user_input):

        user_input = user_input.strip()

        # -----------------------------
        # Direct Command
        # -----------------------------

        if "Course Title:" not in user_input \
           and "Workflow" not in user_input \
           and "Research" not in user_input:

            return f"""
You are an expert YouTube Thumbnail Designer.

USER TOPIC

{user_input}

Your task is ONLY creating a thumbnail.

Return ONLY the following sections.

# Thumbnail Concept

- Main Idea
- Emotional Trigger

# AI Image Prompt

Create ONE highly detailed prompt including:

- photorealistic
- cinematic lighting
- dramatic composition
- realistic materials
- depth of field
- 8K
- ultra detailed

# Thumbnail Text

Rules

- Persian
- Maximum 5 words
- Very high CTR

# Composition

- Main Subject
- Text Position
- Focus Point
- Background

# Camera Angle

# Lighting

# Color Palette

Write EVERYTHING in Persian except the AI image prompt.
"""

        # -----------------------------
        # Workflow Mode
        # -----------------------------

        return f"""
You are the Thumbnail Agent inside Arman StudioOS.

Previous Workflow Output

{user_input}

Your responsibility is ONLY creating the thumbnail.

Do NOT rewrite previous steps.

Return ONLY

# Thumbnail Concept

# AI Image Prompt

# Thumbnail Text

# Composition

# Camera Angle

# Lighting

# Color Palette
"""