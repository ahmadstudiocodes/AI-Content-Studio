class RetryPromptBuilder:
    """
    Builds retry prompts based on validation
    and quality evaluation results.
    """

    @staticmethod
    def build(
        original_prompt: str,
        validation: dict = None,
        quality: dict = None
    ):

        problems = []

        if validation:

            for err in validation.get("errors", []):

                problems.append(err)

        if quality:

            for issue in quality.get("issues", []):

                problems.append(issue)

        if not problems:

            return original_prompt

        feedback = "\n".join(

            f"- {p}"

            for p in problems

        )

        return f"""

The previous answer was rejected.

Problems:

{feedback}

Rewrite the answer.

Rules:

- Fix every problem.
- Do NOT explain.
- Do NOT apologize.
- Return only the final answer.
- Follow all previous instructions.

-------------------------------------

{original_prompt}

"""