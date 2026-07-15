class RetryPromptBuilder:
    """
    Builds a retry prompt when validation or
    quality evaluation fails.

    Instead of asking the LLM the same question again,
    we explain WHY the previous output failed.
    """

    def build(
        self,
        original_prompt: str,
        validation: dict,
        quality: dict
    ):

        # Safe handling
        validation = validation or {}
        quality = quality or {}

        validation_errors = validation.get(
            "errors",
            []
        )

        quality_issues = quality.get(
            "issues",
            []
        )

        validation_text = "\n".join(

            f"- {e}"

            for e in validation_errors

        )

        quality_text = "\n".join(

            f"- {q}"

            for q in quality_issues

        )

        prompt = f"""

Your previous answer failed validation.

==================================================
VALIDATION ERRORS
==================================================

{validation_text if validation_text else "None"}

==================================================
QUALITY ISSUES
==================================================

{quality_text if quality_text else "None"}

==================================================
ORIGINAL TASK
==================================================

{original_prompt}

==================================================
IMPORTANT
==================================================

Rewrite the ENTIRE answer.

Fix every issue listed above.

Do NOT explain.

Do NOT apologize.

Do NOT output reasoning.

Do NOT output thinking.

Do NOT output <think> tags.

Return ONLY the corrected final answer.

"""

        return prompt.strip()


retry_prompt_builder = RetryPromptBuilder()