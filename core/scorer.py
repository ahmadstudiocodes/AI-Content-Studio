class AgentScorer:

    """
    Arman StudioOS Agent Scorer

    Evaluates Agent fitness for a command.

    Factors:

    - priority
    - name
    - domain
    - capability
    - target
    - action

    Priority has limited influence.
    """



    def normalize(
        self,
        text
    ):


        if text is None:

            return ""


        if not isinstance(
            text,
            str
        ):

            text = str(text)



        text = text.lower()



        replacements = {


            "تامبنیل":
            "thumbnail",


            "کاور":
            "thumbnail",


            "تصویر شاخص":
            "thumbnail",


            "سناریو":
            "script",


            "نریشن":
            "script",


            "انتشار":
            "publish",


            "منتشر":
            "publish",


            "دوره":
            "course",


            "آموزش":
            "course"

        }



        for old, new in replacements.items():

            text = text.replace(
                old,
                new
            )



        return text.strip()



    # ==================================================

    def score(
        self,
        agent,
        command
    ):


        score = 0



        # ---------------------------------
        # Build Search Context
        # ---------------------------------


        parts = [

            getattr(
                command,
                "raw",
                ""
            ),


            getattr(
                command,
                "action",
                ""
            ),


            getattr(
                command,
                "target",
                ""

            )

        ]



        raw_text = self.normalize(

            " ".join(

                str(p)

                for p in parts

                if p

            )

        )



        # ---------------------------------
        # Priority
        # ---------------------------------


        priority = getattr(
            agent,
            "priority",
            0
        )


        try:

            priority = int(priority)

        except:

            priority = 0



        score += min(
            priority,
            20
        )



        # ---------------------------------
        # Agent Name
        # ---------------------------------


        name = self.normalize(

            getattr(
                agent,
                "name",
                ""

            )

        )



        if name and name in raw_text:

            score += 50



        # ---------------------------------
        # Domains
        # ---------------------------------


        domains = getattr(
            agent,
            "domains",
            []
        ) or []



        for domain in domains:


            if self.normalize(domain) in raw_text:

                score += 35

                break



        # ---------------------------------
        # Capabilities
        # ---------------------------------


        capabilities = getattr(
            agent,
            "capabilities",
            []
        ) or []



        hits = 0



        for capability in capabilities:


            if self.normalize(capability) in raw_text:

                hits += 1



        score += min(
            hits * 10,
            30
        )



        # ---------------------------------
        # Target
        # ---------------------------------


        target = self.normalize(

            getattr(
                command,
                "target",
                ""

            )

        )



        if target and target in raw_text:

            score += 20



        # ---------------------------------
        # Action
        # ---------------------------------


        action = self.normalize(

            getattr(
                command,
                "action",
                ""

            )

        )



        if action and action in raw_text:

            score += 15



        return score