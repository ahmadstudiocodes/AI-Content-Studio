class RetryPrompt:
    """
    Builds retry instructions for failed outputs.

    Used by Retry Engine when an Agent output
    does not pass validation.
    """


    def build(
        self,
        original_prompt: str,
        errors=None
    ):

        errors = errors or []


        if not errors:

            return original_prompt



        problems = "\n".join(

            f"- {error}"

            for error in errors

        )


        return f"""

Previous output failed validation.

Problems:

{problems}


Instructions:

- Rewrite the complete answer.
- Fix all listed problems.
- Do not explain changes.
- Do not apologize.
- Return only the final answer.
- Do not output reasoning.
- Do not output <think> tags.


Original Task:

{original_prompt}

""".strip()



retry_prompt = RetryPrompt()