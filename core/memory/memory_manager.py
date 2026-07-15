from core.memory.short_term import ShortTermMemory
from core.memory.long_term import LongTermMemory
from datetime import datetime


class MemoryManager:

    """
    Arman StudioOS Memory Manager

    Coordinates:

    - Short Term Memory
    - Long Term Memory

    Provides unified memory interface.
    """



    def __init__(self):

        self.short_term = ShortTermMemory()

        self.long_term = LongTermMemory()



    # ==================================================

    def remember(
        self,
        role,
        content
    ):


        if content is None:

            return



        content = str(content).strip()



        if not content:

            return



        role = str(
            role or "unknown"
        )



        memory_item = {

            "role": role,

            "content": content,

            "timestamp":
                datetime.now().isoformat()

        }



        self.short_term.add(

            role,

            content

        )



        self.long_term.add(

            role,

            content

        )



    # ==================================================

    def recall(
        self,
        limit=None
    ):


        data = []


        data.extend(

            self.short_term.get()

        )


        data.extend(

            self.long_term.get()

        )



        if limit:

            return data[-limit:]



        return data



    # ==================================================

    def clear(
        self
    ):


        self.short_term.clear()

        self.long_term.clear()



    # ==================================================

    def clear_short_term(
        self
    ):


        self.short_term.clear()



    # ==================================================

    def clear_long_term(
        self
    ):


        self.long_term.clear()



    # ==================================================

    def snapshot(
        self
    ):


        return {

            "short_term":

                self.short_term.get(),


            "long_term":

                self.long_term.get()

        }