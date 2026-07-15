import time
from datetime import datetime

from brain.base_agent import BaseAgent
from brain.agent_result import AgentResult

from core.context import ContextManager
from core.memory import MemoryManager
from core.output_guard import output_guard



class BaseLLMAgent(BaseAgent):
    """
    Arman StudioOS

    Enterprise LLM Agent Base Class

    Layer:

        BaseAgent
             |
             ↓
        BaseLLMAgent
             |
             ↓
        Specialized Agents


    Handles:

    - LLM Provider execution
    - Prompt building
    - Context management
    - Memory
    - Output cleaning
    - Execution tracking
    - Standard AgentResult output
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        name,
        description,
        provider,
        system_prompt="",
        config=None,
    ):

        super().__init__(
            name=name,
            description=description
        )


        self.provider = provider

        self.system_prompt = system_prompt

        self.config = config or {}



        # Context Layer

        self.context = ContextManager()



        # Memory Layer

        self.memory = MemoryManager()



        # Runtime

        self.last_execution_time = 0

        self.last_execution = None



    # =====================================================
    # Dispatcher
    # =====================================================


    def can_handle(
        self,
        user_input
    ):
        """
        Override in child agents.
        """

        return False



    # =====================================================
    # Public Execution API
    # =====================================================


    def run(
        self,
        user_input,
        context=None
    ):
        """
        Main Agent execution.
        """


        self.validate(
            user_input
        )



        start = time.time()



        try:


            self.context.add(
                "user",
                user_input
            )



            prompt = self.build_prompt(
                user_input
            )



            response = self.call_provider(
                prompt
            )



            cleaned = self.postprocess(
                response,
                user_input
            )



            if not cleaned:

                raise RuntimeError(
                    "Agent returned empty response."
                )



            self.context.add(
                "assistant",
                cleaned
            )



            self.memory.remember(
                "user",
                user_input
            )


            self.memory.remember(
                "assistant",
                cleaned
            )



            elapsed = (
                time.time()
                -
                start
            )


            self.last_execution_time = elapsed

            self.last_execution = datetime.utcnow()



            result = AgentResult.success_result(
                data=cleaned,
                message="Execution completed."
            )



            result.set_agent(
                self.name
            )


            result.set_execution_time(
                elapsed
            )



            return result



        except Exception as error:


            result = AgentResult.error_result(
                error
            )


            result.set_agent(
                self.name
            )


            return result



    # =====================================================
    # Validation
    # =====================================================


    def validate(
        self,
        user_input
    ):


        if not isinstance(
            user_input,
            str
        ):

            raise ValueError(
                "User input must be string."
            )



        if not user_input.strip():

            raise ValueError(
                "User input cannot be empty."
            )



    # =====================================================
    # Prompt Builder
    # =====================================================


    def build_prompt(
        self,
        user_input
    ):


        context = self.context.build()



        return f"""

{self.system_prompt}


CONTEXT:

{context}


USER REQUEST:

{user_input}

"""



    # =====================================================
    # Provider Layer
    # =====================================================


    def call_provider(
        self,
        prompt
    ):
        """
        Call LLM provider.

        This replaces execute()
        to protect Framework lifecycle.
        """

        return self.provider.generate(
            prompt
        )



    # =====================================================
    # Output Processing
    # =====================================================


    def postprocess(
        self,
        response,
        user_input=None
    ):

        return output_guard.clean(
            response
        )