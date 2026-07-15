from memory.models import MemoryItem
from memory.storage import storage



class MemoryService:

    """
    Arman StudioOS Memory Service

    Business layer between:

        Brain
          |
        Memory Service
          |
        Storage

    """


    # ==================================================

    def remember(
        self,
        category,
        key,
        value
    ):


        if not key:

            return False



        if value is None:

            return False



        try:


            item = MemoryItem(

                category or "general",

                str(key),

                str(value)

            )


            storage.save(
                item
            )


            return True



        except Exception as e:


            print(
                f"[MEMORY SERVICE] Save failed: {e}"
            )


            return False



    # ==================================================

    def recall(
        self,
        key,
        category=None
    ):


        try:


            results = storage.search(
                key
            )


            if category:


                results = [

                    item

                    for item in results

                    if getattr(
                        item,
                        "category",
                        None
                    ) == category

                ]



            return results



        except Exception as e:


            print(
                f"[MEMORY SERVICE] Recall failed: {e}"
            )


            return []



    # ==================================================

    def delete(
        self,
        key
    ):


        try:


            return storage.delete(
                key
            )


        except Exception as e:


            print(
                f"[MEMORY SERVICE] Delete failed: {e}"
            )


            return False



memory_service = MemoryService()