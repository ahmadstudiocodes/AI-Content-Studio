from core.guard_prompt import GuardPrompt
from core.prompt_object import PromptObject


class PromptBuilder:
    """
    Central Prompt Builder for Arman StudioOS

    Responsible for building a structured prompt
    that can later be retried, versioned and enriched
    with memory/context.
    """

    def build(
        self,
        task: str,
        topic: str,
        system_prompt: str = "",
        channel_profile: str = "",
        agent_rules: str = "",
        context: str = "",
        output_format: str = ""
    ) -> PromptObject:

        guard = GuardPrompt.build(

            task=task,

            topic=topic,

            agent_rules=agent_rules

        )

        final_prompt = f"""
{guard}

==================================================
SYSTEM
==================================================

{system_prompt}


==================================================
CHANNEL PROFILE
==================================================

{channel_profile}


==================================================
USER REQUEST
==================================================

Task:

{task}

Topic:

{topic}


==================================================
CONTEXT
==================================================

{context}


==================================================
RULES
==================================================

{agent_rules}


==================================================
OUTPUT FORMAT
==================================================

{output_format}


==================================================
EXECUTION
==================================================

Execute the task.

Return ONLY the final answer.

Do not explain.

"""

        return PromptObject(

            system=system_prompt,

            channel=channel_profile,

            context=context,

            rules=agent_rules,

            output_format=output_format,

            user_request=topic,

            prompt=final_prompt

        )


prompt_builder = PromptBuilder()