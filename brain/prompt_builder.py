class PromptBuilder:

    def __init__(self):

        self.system = ""

        self.context = ""

    def build(self, user_prompt):

        return f"""

SYSTEM

{self.system}

CONTEXT

{self.context}

USER

{user_prompt}

"""


prompt_builder = PromptBuilder()