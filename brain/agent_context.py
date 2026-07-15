# brain/agent_context.py

from datetime import datetime
import uuid
from copy import deepcopy



class AgentContext:
    """
    Arman StudioOS

    Enterprise Agent Context

    Shared execution context
    between Agent, Workflow, Memory
    and Runtime.

    Responsibilities
    ----------------

    - Store execution data
    - Manage variables
    - Carry metadata
    - Share information
    - Support multi-agent workflows

    """



    VERSION = "1.0.0"



    def __init__(
        self,
        user_input=None,
        workflow_id=None,
        metadata=None,
        variables=None,
    ):


        # Identity

        self.context_id = str(
            uuid.uuid4()
        )


        self.created_at = datetime.utcnow()



        # Execution Data

        self.user_input = user_input


        self.workflow_id = workflow_id



        # Metadata

        self.metadata = metadata or {}



        # Runtime Variables

        self.variables = variables or {}



        # Memory Reference

        self.memory = None



        # Tool Reference

        self.tools = {}



        # Agent Communication

        self.messages = []



        # State

        self.status = "created"



    # =====================================================
    # Variables
    # =====================================================


    def set(
        self,
        key,
        value
    ):
        """
        Store context variable.
        """

        self.variables[key] = value



    def get(
        self,
        key,
        default=None
    ):
        """
        Retrieve variable.
        """

        return self.variables.get(
            key,
            default
        )



    def remove(
        self,
        key
    ):
        """
        Remove variable.
        """

        self.variables.pop(
            key,
            None
        )



    # =====================================================
    # Metadata
    # =====================================================


    def update_metadata(
        self,
        key,
        value
    ):
        """
        Update metadata.
        """

        self.metadata[key] = value



    def get_metadata(
        self,
        key,
        default=None
    ):
        """
        Read metadata.
        """

        return self.metadata.get(
            key,
            default
        )
    # =====================================================
    # Memory Management
    # =====================================================


    def attach_memory(
        self,
        memory
    ):
        """
        Attach memory system.
        """

        self.memory = memory



    def remember(
        self,
        key,
        value
    ):
        """
        Store data in memory layer.
        """

        if self.memory:

            return self.memory.store(
                key,
                value
            )


        return False



    def recall(
        self,
        key
    ):
        """
        Retrieve data from memory.
        """

        if self.memory:

            return self.memory.retrieve(
                key
            )


        return None



    # =====================================================
    # Tool Management
    # =====================================================


    def add_tool(
        self,
        name,
        tool
    ):
        """
        Attach tool to context.
        """

        self.tools[name] = tool



    def get_tool(
        self,
        name
    ):
        """
        Retrieve tool.
        """

        return self.tools.get(
            name
        )



    def remove_tool(
        self,
        name
    ):
        """
        Remove tool.
        """

        self.tools.pop(
            name,
            None
        )



    # =====================================================
    # Agent Communication
    # =====================================================


    def add_message(
        self,
        sender,
        message
    ):
        """
        Store agent communication.
        """

        self.messages.append({

            "sender": sender,

            "message": message,

            "time":
                datetime.utcnow(),

        })



    def get_messages(self):
        """
        Return communication history.
        """

        return deepcopy(
            self.messages
        )



    def clear_messages(self):
        """
        Clear messages.
        """

        self.messages.clear()



    # =====================================================
    # Context Operations
    # =====================================================


    def clone(self):
        """
        Create isolated copy.

        Useful for:

        - Parallel agents
        - Experiments
        - Branching workflows
        """

        new_context = AgentContext(

            user_input=self.user_input,

            workflow_id=self.workflow_id,

            metadata=deepcopy(
                self.metadata
            ),

            variables=deepcopy(
                self.variables
            ),

        )


        new_context.tools = deepcopy(
            self.tools
        )


        new_context.messages = deepcopy(
            self.messages
        )


        new_context.memory = self.memory


        return new_context



    # =====================================================
    # State Management
    # =====================================================


    def set_status(
        self,
        status
    ):
        """
        Update context status.
        """

        self.status = status



    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Export context state.
        """

        return {

            "context_id":
                self.context_id,


            "workflow_id":
                self.workflow_id,


            "user_input":
                self.user_input,


            "metadata":
                deepcopy(
                    self.metadata
                ),


            "variables":
                deepcopy(
                    self.variables
                ),


            "messages":
                deepcopy(
                    self.messages
                ),


            "status":
                self.status,


            "created_at":
                self.created_at.isoformat(),

        }



    # =====================================================
    # Health & Debug
    # =====================================================


    def health(self):
        """
        Context health status.
        """

        return {

            "id":
                self.context_id,


            "status":
                self.status,


            "variables":
                len(self.variables),


            "messages":
                len(self.messages),

        }



    def __repr__(self):

        return (

            f"<AgentContext "

            f"id={self.context_id[:8]} "

            f"status={self.status}>"

        )