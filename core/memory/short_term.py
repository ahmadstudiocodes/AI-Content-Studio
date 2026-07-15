from datetime import datetime


class ShortTermMemory:

    """
    Arman StudioOS Short Term Memory

    Stores recent interactions
    with limited history size.
    """



    def __init__(
        self,
        limit=20
    ):

        self.limit = max(
            1,
            limit
        )

        self.memory = []



    # ==================================================

    def add(
        self,
        role,
        content
    ):


        if content is None:

            return



        content = str(
            content
        ).strip()



        if not content:

            return



        item = {

            "role":
                str(role or "unknown"),


            "content":
                content,


            "timestamp":
                datetime.now().isoformat()

        }



        self.memory.append(
            item
        )



        self.trim()



    # ==================================================

    def trim(
        self
    ):


        while len(self.memory) > self.limit:

            self.memory.pop(0)



    # ==================================================

    def get(
        self
    ):


        return list(
            self.memory
        )



    # ==================================================

    def latest(
        self,
        count=5
    ):


        return self.memory[-count:]



    # ==================================================

    def clear(
        self
    ):


        self.memory = []