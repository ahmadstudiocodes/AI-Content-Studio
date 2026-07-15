# brain/capability_manager.py

from datetime import datetime
from copy import deepcopy



class CapabilityManager:
    """
    Arman StudioOS

    Enterprise Capability Manager

    Responsible for:

    - Managing capabilities
    - Mapping agents to capabilities
    - Capability discovery
    - Agent selection support

    Future:

    - Dynamic capability loading
    - Plugin integration
    """



    VERSION = "1.0.0"



    def __init__(self):

        self.capabilities = {}

        self.created_at = datetime.utcnow()



    # =====================================================
    # Capability Registration
    # =====================================================


    def register(
        self,
        name,
        description="",
        metadata=None
    ):
        """
        Register new capability.
        """

        self.capabilities[name] = {

            "name": name,

            "description": description,

            "metadata": metadata or {},

            "agents": [],

        }


        return True



    def unregister(
        self,
        name
    ):
        """
        Remove capability.
        """

        self.capabilities.pop(
            name,
            None
        )



    def exists(
        self,
        name
    ):
        """
        Check capability.
        """

        return name in self.capabilities



    # =====================================================
    # Agent Mapping
    # =====================================================


    def attach(
        self,
        agent_name,
        capability
    ):
        """
        Attach capability to agent.
        """

        if capability not in self.capabilities:

            self.register(
                capability
            )


        agents = self.capabilities[capability]["agents"]


        if agent_name not in agents:

            agents.append(
                agent_name
            )


        return True



    def detach(
        self,
        agent_name,
        capability
    ):
        """
        Remove agent capability.
        """

        if capability not in self.capabilities:

            return False


        agents = self.capabilities[capability]["agents"]


        if agent_name in agents:

            agents.remove(
                agent_name
            )


            return True


        return False
    
    # =====================================================
    # Discovery
    # =====================================================


    def get_agents(
        self,
        capability
    ):
        """
        Return agents having capability.
        """

        if capability not in self.capabilities:

            return []


        return self.capabilities[capability]["agents"].copy()



    def find(
        self,
        capability
    ):
        """
        Alias for capability search.
        """

        return self.get_agents(
            capability
        )



    def list_capabilities(self):
        """
        Return all capabilities.
        """

        return sorted(
            self.capabilities.keys()
        )



    def count(self):
        """
        Return capability count.
        """

        return len(
            self.capabilities
        )



    # =====================================================
    # Metadata
    # =====================================================


    def metadata(
        self,
        capability
    ):
        """
        Return capability metadata.
        """

        item = self.capabilities.get(
            capability
        )


        if item is None:

            return None


        return deepcopy(
            item
        )



    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Export capability state.
        """

        return {

            "version":
                self.VERSION,


            "created_at":
                self.created_at.isoformat(),


            "count":
                self.count(),


            "capabilities":
                deepcopy(
                    self.capabilities
                ),

        }



    # =====================================================
    # Management
    # =====================================================


    def clear(self):
        """
        Remove all capabilities.
        """

        self.capabilities.clear()



    def health(self):
        """
        Capability manager health.
        """

        return {

            "status":
                "healthy",


            "capabilities":
                self.count(),

        }



    # =====================================================
    # Debug
    # =====================================================


    def info(self):
        """
        Return manager information.
        """

        return {

            "name":
                "CapabilityManager",


            "version":
                self.VERSION,


            "count":
                self.count(),


            "capabilities":
                self.list_capabilities(),

        }



    def __repr__(self):

        return (

            f"<CapabilityManager "

            f"capabilities={self.count()} "

            f"version={self.VERSION}>"

        )



# =========================================================
# Global Instance
# =========================================================

capability_manager = CapabilityManager()