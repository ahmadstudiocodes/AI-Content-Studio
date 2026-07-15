# brain/shared_agent_memory.py


from datetime import datetime
from uuid import uuid4
from copy import deepcopy



class MemoryEntry:
    """
    Shared memory item between agents.
    """

    def __init__(
        self,
        key,
        value,
        owner=None,
        category="general"
    ):

        self.id = str(
            uuid4()
        )

        self.key = key

        self.value = value

        self.owner = owner

        self.category = category

        self.created_at = datetime.utcnow()

        self.updated_at = self.created_at



    def update(
        self,
        value
    ):

        self.value = value

        self.updated_at = datetime.utcnow()



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "key":
                self.key,

            "value":
                self.value,

            "owner":
                self.owner,

            "category":
                self.category,

            "created_at":
                self.created_at.isoformat(),

            "updated_at":
                self.updated_at.isoformat()

        }





class SharedAgentMemory:
    """
    Arman StudioOS

    Shared Memory Layer for Agents.


    Responsibilities:

    - Store shared knowledge
    - Retrieve information
    - Update memories
    - Share agent results
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.memory = {}



    # =====================================================
    # Store
    # =====================================================


    def store(
        self,
        key,
        value,
        owner=None,
        category="general"
    ):

        entry = MemoryEntry(

            key,

            value,

            owner,

            category

        )


        self.memory[key] = entry


        return entry



    # =====================================================
    # Update
    # =====================================================


    def update(
        self,
        key,
        value
    ):


        entry = self.memory.get(
            key
        )


        if not entry:

            return False



        entry.update(
            value
        )


        return True



    # =====================================================
    # Retrieve
    # =====================================================


    def get(
        self,
        key,
        default=None
    ):


        entry = self.memory.get(
            key
        )


        if not entry:

            return default



        return entry.value



    # =====================================================
    # Remove
    # =====================================================


    def remove(
        self,
        key
    ):


        if key in self.memory:

            del self.memory[key]

            return True


        return False



    # =====================================================
    # Search
    # =====================================================


    def search(
        self,
        keyword
    ):


        results = []


        for entry in self.memory.values():


            if keyword.lower() in str(
                entry.value
            ).lower():

                results.append(
                    entry.to_dict()
                )


        return results



    # =====================================================
    # Snapshot
    # =====================================================


    def snapshot(
        self
    ):


        return {

            key:
                deepcopy(
                    entry.to_dict()
                )

            for key, entry in self.memory.items()

        }



    # =====================================================
    # Management
    # =====================================================


    def clear(
        self
    ):

        self.memory.clear()



    def count(
        self
    ):

        return len(
            self.memory
        )



    def info(
        self
    ):

        return {

            "name":
                "SharedAgentMemory",

            "version":
                self.VERSION,

            "items":
                self.count()

        }





# Global Instance

shared_agent_memory = SharedAgentMemory()