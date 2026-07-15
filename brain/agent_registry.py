# brain/agent_registry.py

from copy import deepcopy
from datetime import datetime

from brain.base_agent import BaseAgent



class AgentRegistry:
    """
    Arman StudioOS

    Enterprise Agent Registry

    Central registry for all agents.

    Responsibilities
    ----------------

    - Register agents
    - Unregister agents
    - Agent discovery
    - Metadata storage
    - Capability search
    - Agent state tracking
    - Serialization

    Future:

    - Plugin loading
    - EventBus integration
    - Dynamic discovery
    """



    VERSION = "1.0.0"



    def __init__(self):

        self._agents = {}

        self.created_at = datetime.utcnow()



    # =====================================================
    # Registration
    # =====================================================


    def register(self, agent):
        """
        Register a BaseAgent instance.
        """

        if not isinstance(agent, BaseAgent):

            raise TypeError(
                "Agent must inherit from BaseAgent"
            )


        self._agents[agent.name] = {

            "instance": agent,

            "registered_at":
                datetime.utcnow(),

            "metadata":
                agent.info(),

        }


        return agent



    def unregister(self, name):
        """
        Remove agent from registry.
        """

        if name in self._agents:

            del self._agents[name]

            return True


        return False



    # =====================================================
    # Lookup
    # =====================================================


    def get(self, name):
        """
        Retrieve agent instance.
        """

        item = self._agents.get(name)


        if item is None:

            return None


        return item["instance"]



    def exists(self, name):
        """
        Check agent existence.
        """

        return name in self._agents



    def list_agents(self):
        """
        Return all agent names.
        """

        return sorted(
            self._agents.keys()
        )



    def count(self):
        """
        Return number of agents.
        """

        return len(
            self._agents
        )



    # =====================================================
    # Capability Search
    # =====================================================


    def find_by_capability(
        self,
        capability
    ):
        """
        Find agents by capability.
        """

        result = []


        for name, data in self._agents.items():

            agent = data["instance"]


            if agent.has_capability(
                capability
            ):

                result.append(agent)



        return result



    # =====================================================
    # Metadata
    # =====================================================


    def metadata(self, name):
        """
        Return agent metadata.
        """

        item = self._agents.get(name)


        if item is None:

            return None


        return deepcopy(
            item["metadata"]
        )



    def refresh_metadata(self, name):
        """
        Refresh stored metadata.
        """

        agent = self.get(name)


        if not agent:

            return False


        self._agents[name]["metadata"] = (
            agent.info()
        )


        return True



    # =====================================================
    # State
    # =====================================================


    def status(self, name):
        """
        Return agent status.
        """

        agent = self.get(name)


        if not agent:

            return None


        return {

            "name": agent.name,

            "enabled": agent.enabled,

            "status": agent.status,

            "last_run": agent.last_run,

        }

    # =====================================================
    # Snapshot
    # =====================================================


    def snapshot(self):
        """
        Create lightweight registry snapshot.

        Does not expose agent instances.
        """

        result = {}


        for name, data in self._agents.items():

            agent = data["instance"]


            result[name] = {

                "name":
                    agent.name,


                "description":
                    agent.description,


                "version":
                    agent.version,


                "capabilities":
                    deepcopy(
                        agent.capabilities
                    ),


                "status":
                    agent.status,


                "enabled":
                    agent.enabled,


            }


        return result



    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Export complete registry state.

        Used for:

        - Persistence
        - Debugging
        - Runtime
        """

        return {

            "version":
                self.VERSION,


            "created_at":
                self.created_at.isoformat(),


            "count":
                self.count(),


            "agents":

                self.snapshot(),

        }



    # =====================================================
    # Health
    # =====================================================


    def health(self):
        """
        Registry health status.
        """

        return {

            "status":
                "healthy",


            "agents":
                self.count(),


            "version":
                self.VERSION,


        }



    # =====================================================
    # Management
    # =====================================================


    def clear(self):
        """
        Remove all registered agents.
        """

        self._agents.clear()



    def reload_metadata(self):
        """
        Refresh metadata for all agents.
        """

        for name in self._agents:

            self.refresh_metadata(
                name
            )



    # =====================================================
    # Debug
    # =====================================================


    def info(self):
        """
        Registry information.
        """

        return {

            "name":
                "AgentRegistry",


            "version":
                self.VERSION,


            "agent_count":
                self.count(),


            "agents":
                self.list_agents(),

        }



    def __repr__(self):
        """
        Developer representation.
        """

        return (

            f"<AgentRegistry "

            f"agents={self.count()} "

            f"version={self.VERSION}>"

        )



# =========================================================
# Global Registry Instance
# =========================================================

agent_registry = AgentRegistry()    