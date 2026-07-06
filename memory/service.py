from memory.models import MemoryItem
from memory.storage import storage


class MemoryService:

    def remember(self,

                 category,

                 key,

                 value):

        item=MemoryItem(

            category,

            key,

            value

        )

        storage.save(item)

    def recall(self,key):

        return storage.search(key)


memory_service=MemoryService()