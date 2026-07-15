from agents.base.base_llm_agent import BaseLLMAgent



class FactCheckerAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Fact Checking Agent


    Responsibilities:

    - Verify information
    - Analyze claims
    - Detect unsupported statements
    - Separate facts and assumptions
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="fact_checker",

            description=
            "Professional Fact Verification Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Fact Checker Agent.

Your responsibility is verifying information.

Focus on:

- Checking claims
- Finding inconsistencies
- Separating facts from opinions
- Evaluating reliability
- Identifying uncertainty


Never:

- Create unsupported facts
- Modify verified information
- Write creative content

"""

        )


        self.priority = 95



        self.domains = [

            "fact",

            "verification",

            "analysis"

        ]



        self.capabilities = [

            "fact_check",

            "claim_analysis",

            "verification",

            "source_evaluation"

        ]



    # =====================================================
    # Capability
    # =====================================================


    def has_capability(
        self,
        capability
    ):

        return capability in self.capabilities



    # =====================================================
    # Dispatcher
    # =====================================================


    def can_handle(
        self,
        user_input
    ):


        text = str(
            user_input
        ).lower()



        keywords = [

            "fact",

            "check",

            "بررسی صحت",

            "صحت",

            "راستی آزمایی",

            "واقعی",

            "منبع"

        ]



        return any(

            key in text

            for key in keywords

        )



    # =====================================================
    # Prompt Builder
    # =====================================================


    def build_prompt(
        self,
        user_input
    ):


        return f"""

{self.system_prompt}


USER REQUEST:

{user_input}



Required Structure:


# Claim Analysis


# Verified Facts


# Unverified Information


# Possible Errors


# Confidence Level


# Recommended Sources



Rules:

- Answer in Persian.
- Separate facts from assumptions.
- Do not invent evidence.
- Mention uncertainty clearly.

"""



    # =====================================================
    # Post Processing
    # =====================================================


    def postprocess(
        self,
        response,
        user_input=None
    ):


        return super().postprocess(
            response,
            user_input
        )