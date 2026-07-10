import time

from agents.base_agent import BaseAgent
from core.context import ContextManager
from core.memory import MemoryManager


class BaseLLMAgent(BaseAgent):
    """
    Base class for all Arman StudioOS LLM Agents.
    """

    def __init__(
        self,
        name,
        description,
        provider,
        system_prompt="",
        config=None,
    ):

        super().__init__(name, description)

        self.provider = provider
        self.system_prompt = system_prompt
        self.config = config or {}

        self.context = ContextManager()
        self.memory = MemoryManager()

    # =====================================================
    # Dispatcher API
    # =====================================================

    def can_handle(self, user_input):
        return False

    # =====================================================
    # Public API
    # =====================================================

    def run(self, user_input):

        print("=" * 50)
        print(f"[{self.name.upper()}] START")
        print("=" * 50)

        self.validate(user_input)

        self.context.add("user", user_input)

        prompt = self.build_prompt(user_input)

        print("=" * 70)
        print("[FINAL PROMPT]")
        print(prompt)
        print("=" * 70)

        start = time.time()

        response = self.execute(prompt)

        elapsed = time.time() - start

        self.context.add("assistant", response)

        self.memory.remember("user", user_input)
        self.memory.remember("assistant", response)

        print(f"[{self.name}] Completed in {elapsed:.2f}s")

        return self.postprocess(response)

    # =====================================================
    # Validation
    # =====================================================

    def validate(self, user_input):

        if not isinstance(user_input, str):
            raise ValueError("User input must be a string.")

        if not user_input.strip():
            raise ValueError("User input cannot be empty.")

    # =====================================================
    # Prompt Builder
    # =====================================================

    def build_prompt(self, user_input):

        context = self.context.build()

        return f"""
{self.system_prompt}

CONTEXT:

{context}

USER REQUEST:

{user_input}
"""

    # =====================================================
    # LLM Execution
    # =====================================================

    def execute(self, prompt):

        return self.provider.generate(prompt)

    # =====================================================
    # Post Processing
    # =====================================================

    def postprocess(self, response):

        return response