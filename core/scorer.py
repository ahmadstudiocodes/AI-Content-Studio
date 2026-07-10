class AgentScorer:

    """
    Scores agents based on:
    - priority
    - domain match
    - capability match
    - name match
    - target/action match
    """

    def score(self, agent, command):


        score = 0


        raw_text = ""

        try:

            raw_text = command.raw.lower()

        except Exception:

            pass



        # -----------------------------
        # Priority
        # -----------------------------

        score += getattr(
            agent,
            "priority",
            0
        )



        # -----------------------------
        # Agent name matching
        # -----------------------------

        try:

            name = agent.name.lower()

            if name in raw_text:

                score += 40


        except Exception:

            pass



        # -----------------------------
        # Domain matching
        # -----------------------------

        try:

            domains = getattr(
                agent,
                "domains",
                []
            )


            for domain in domains:

                if domain.lower() in raw_text:

                    score += 50


        except Exception:

            pass



        # -----------------------------
        # Capability matching
        # -----------------------------

        try:

            capabilities = getattr(
                agent,
                "capabilities",
                []
            )


            for capability in capabilities:

                if capability.lower() in raw_text:

                    score += 20


        except Exception:

            pass



        # -----------------------------
        # Target matching
        # -----------------------------

        try:

            target = command.target


            if target:

                if target.lower() in raw_text:

                    score += 30


        except Exception:

            pass



        # -----------------------------
        # Action matching
        # -----------------------------

        try:

            action = command.action


            if action:

                if action.lower() in raw_text:

                    score += 10


        except Exception:

            pass



        return score