class ContextManager:

    """
    Arman StudioOS Context Manager

    Manages conversation context
    shared between agents.
    """



    def __init__(
        self,
        max_history=10
    ):

        self.max_history = max_history

        self.history = []



    # ==================================================

    def add(
        self,
        role,
        content
    ):


        if content is None:

            return



        item = {

            "role": str(role or "unknown"),

            "content": str(content)

        }



        self.history.append(
            item
        )



        self.trim()



    # ==================================================

    def trim(
        self
    ):


        while len(self.history) > self.max_history:

            self.history.pop(0)



    # ==================================================

    def get(
        self
    ):


        return list(
            self.history
        )



    # ==================================================

    def clear(
        self
    ):


        self.history = []



    # ==================================================

    def build(
        self
    ):


        if not self.history:

            return ""



        context = []



        for item in self.history:


            role = item.get(
                "role",
                "unknown"
            )


            content = item.get(
                "content",
                ""
            )


            context.append(

                f"{role.upper()}:\n{content}"

            )



        return "\n\n".join(
            context
        )



    # ==================================================

    def snapshot(
        self
    ):


        return {

            "history": self.get(),

            "size": len(self.history)

        }