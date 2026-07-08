from core.guard_prompt import GuardPrompt


class PromptBuilder:
    """
    Prompt Builder for Arman StudioOS

    Responsible for creating final prompts
    before sending them to LLM providers.
    """


    def __init__(self):
        pass


    def build(
        self,
        task: str,
        topic: str,
        agent_rules: str = "",
        context: str = ""
    ) -> str:


        guard = GuardPrompt.build(
            task=task,
            topic=topic,
            agent_rules=agent_rules
        )


        prompt = f"""
{guard}


==================================================
TASK EXECUTION
==================================================


User Request:

{task}


Main Topic:

{topic}


Additional Context:

{context}


==================================================
EXECUTION INSTRUCTIONS
==================================================


Execute the task now.

Remember:

- Follow Guard rules.
- Do not change the task.
- Do not add explanations.
- Return only final output.


==================================================
END PROMPT
==================================================

"""


        return prompt