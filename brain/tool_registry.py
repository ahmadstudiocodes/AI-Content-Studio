# brain/tool_registry.py

from datetime import datetime
from copy import deepcopy



class ToolRegistry:
    """
    Arman StudioOS

    Enterprise Tool Registry

    Central registry for all tools
    available to agents.

    Responsibilities
    ----------------

    - Register tools
    - Remove tools
    - Tool discovery
    - Metadata storage
    - Agent-tool mapping

    Future:

    - Plugin integration
    - Dynamic loading
    - Permission system
    """



    VERSION = "1.0.0"



    def __init__(self):

        self.tools = {}

        self.created_at = datetime.utcnow()



    # =====================================================
    # Registration
    # =====================================================


    def register(
        self,
        name,
        tool,
        description="",
        metadata=None
    ):
        """
        Register new tool.
        """

        self.tools[name] = {

            "instance": tool,

            "description":
                description,

            "metadata":
                metadata or {},

            "agents": [],

        }


        return tool



    def unregister(
        self,
        name
    ):
        """
        Remove tool.
        """

        if name in self.tools:

            del self.tools[name]

            return True


        return False



    def exists(
        self,
        name
    ):
        """
        Check tool existence.
        """

        return name in self.tools



    # =====================================================
    # Lookup
    # =====================================================


    def get(
        self,
        name
    ):
        """
        Return tool instance.
        """

        item = self.tools.get(
            name
        )


        if item is None:

            return None


        return item["instance"]



    def list_tools(self):
        """
        Return tool names.
        """

        return sorted(
            self.tools.keys()
        )



    def count(self):

        return len(
            self.tools
        )
    
    # =====================================================
    # Agent Mapping
    # =====================================================


    def attach_agent(
        self,
        tool_name,
        agent_name
    ):
        """
        Attach tool to agent.
        """

        if tool_name not in self.tools:

            return False


        agents = self.tools[tool_name]["agents"]


        if agent_name not in agents:

            agents.append(
                agent_name
            )


        return True



    def detach_agent(
        self,
        tool_name,
        agent_name
    ):
        """
        Remove tool from agent.
        """

        if tool_name not in self.tools:

            return False


        agents = self.tools[tool_name]["agents"]


        if agent_name in agents:

            agents.remove(
                agent_name
            )


            return True


        return False



    def get_agents(
        self,
        tool_name
    ):
        """
        Return agents using tool.
        """

        if tool_name not in self.tools:

            return []


        return self.tools[tool_name]["agents"].copy()



    # =====================================================
    # Metadata
    # =====================================================


    def metadata(
        self,
        name
    ):
        """
        Return tool metadata.
        """

        item = self.tools.get(
            name
        )


        if item is None:

            return None


        result = deepcopy(
            item
        )


        result.pop(
            "instance",
            None
        )


        return result



    # =====================================================
    # Snapshot
    # =====================================================


    def snapshot(self):
        """
        Create safe registry snapshot.
        """

        result = {}


        for name, data in self.tools.items():

            result[name] = {

                "description":
                    data["description"],


                "metadata":
                    deepcopy(
                        data["metadata"]
                    ),


                "agents":
                    data["agents"].copy(),

            }


        return result



    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Export registry state.
        """

        return {

            "version":
                self.VERSION,


            "created_at":
                self.created_at.isoformat(),


            "count":
                self.count(),


            "tools":
                self.snapshot(),

        }



    # =====================================================
    # Management
    # =====================================================


    def clear(self):
        """
        Remove all tools.
        """

        self.tools.clear()



    def health(self):
        """
        Registry health.
        """

        return {

            "status":
                "healthy",


            "tools":
                self.count(),

        }



    # =====================================================
    # Debug
    # =====================================================


    def info(self):
        """
        Registry information.
        """

        return {

            "name":
                "ToolRegistry",


            "version":
                self.VERSION,


            "count":
                self.count(),


            "tools":
                self.list_tools(),

        }



    def __repr__(self):

        return (

            f"<ToolRegistry "

            f"tools={self.count()} "

            f"version={self.VERSION}>"

        )



# =========================================================
# Global Instance
# =========================================================

tool_registry = ToolRegistry()