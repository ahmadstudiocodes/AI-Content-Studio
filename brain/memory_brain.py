from memory.service import memory_service


class MemoryBrain:

    """
    Arman StudioOS Memory Brain

    Brain level interface
    for persistent memory operations.
    """



    DEFAULT_CATEGORY = "general"



    # ==================================================

    def remember(
        self,
        key,
        value,
        category=None
    ):


        try:


            memory_service.remember(

                category or self.DEFAULT_CATEGORY,

                key,

                value

            )


            return True



        except Exception as e:


            print(
                f"[MEMORY BRAIN] Remember failed: {e}"
            )


            return False



    # ==================================================

    def recall(
        self,
        key
    ):


        try:


            return memory_service.recall(
                key
            )


        except Exception as e:


            print(
                f"[MEMORY BRAIN] Recall failed: {e}"
            )


            return None



    # ==================================================

    def forget(
        self,
        key
    ):


        try:


            return memory_service.delete(
                key
            )


        except Exception as e:


            print(
                f"[MEMORY BRAIN] Delete failed: {e}"
            )


            return False



brain_memory = MemoryBrain()