from memory.service import memory_service


class MemoryBrain:

    def remember(self,key,value):

        memory_service.remember(

            "general",

            key,

            value

        )

    def recall(self,key):

        return memory_service.recall(key)


brain_memory=MemoryBrain()