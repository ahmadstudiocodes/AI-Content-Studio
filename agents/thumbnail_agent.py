from agents.base_agent import BaseAgent
from core.local_provider import local_provider


class ThumbnailAgent(BaseAgent):

    name = "thumbnail"

    version = "1.4.1"

    description = "AI YouTube Thumbnail Design Agent"


    priority = 80


    domains = [
        "youtube",
        "thumbnail",
        "image"
    ]


    capabilities = [
        "thumbnail_design",
        "image_prompt",
        "youtube_cover"
    ]


    def can_handle(self, command):

        return (
            command.action == "generate"
            and command.target == "thumbnail"
            and command.intent.domain in [
                "youtube",
                "thumbnail",
                "image"
            ]
        )


    def execute(self, command):

        prompt = f"""
You are Arman StudioOS Thumbnail Agent.

Task:
Design a professional YouTube thumbnail.

Topic:
{command.payload}


Language Rules:

- Answer only in natural Persian.
- Use simple Persian words.
- Avoid unusual creative words.
- Do not invent words.
- Keep architectural terms professional.


Generate exactly these sections:


1. Thumbnail Concept

Describe:
- ایده اصلی تصویر
- حس و پیام احساسی


2. AI Image Generation Prompt

Create one detailed image prompt.

Must include:

- ultra realistic architectural visualization
- modern architecture
- cinematic lighting
- camera angle
- architectural details
- materials
- environment
- realistic textures
- 8K quality


3. Thumbnail Text

Rules:

- Persian language
- Maximum 5 words
- High CTR
- Emotional and curiosity driven


4. Composition

Include:

- موضوع اصلی
- جایگاه متن
- پس زمینه
- ساختار بصری
- نقطه تمرکز


5. Camera Angle


6. Lighting Style


7. Color Palette


8. CTR Improvement Tips


Restrictions:

- No scripts.
- No channel ideas.
- No explanations.
- Only thumbnail design.

Answer in Persian.
"""


        return local_provider.generate(
            prompt,
            temperature=0.2
        )