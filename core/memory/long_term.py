from datetime import datetime


class LongTermMemory:

    """
    Arman StudioOS Long Term Memory

    Stores persistent knowledge
    collected during executions.

    Current storage:
        In-memory storage

    Future:
        Database / Vector Store
    """



    def __init__(self):

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



        self.memory.append(

            {

                "role":
                    str(role or "unknown"),


                "content":
                    content,


                "timestamp":
                    datetime.now().isoformat()

            }

        )



    # ==================================================

    def get(
        self
    ):


        return list(
            self.memory
        )



    # ==================================================

    def search(
        self,
        keyword
    ):


        if not keyword:

            return []



        keyword = str(
            keyword
        ).lower()



        results = []



        for item in self.memory:


            content = item.get(
                "content",
                ""
            ).lower()



            if keyword in content:

                results.append(
                    item
                )



        return results



    # ==================================================

    def clear(
        self
    ):


        self.memory = []



    # ==================================================

    def size(
        self
    ):


        return len(
            self.memory
        )