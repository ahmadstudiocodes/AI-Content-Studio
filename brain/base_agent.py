from abc import ABC, abstractmethod
from datetime import datetime
import time
import uuid
import traceback


class BaseAgent(ABC):
    """
    Arman StudioOS
    Enterprise Agent Framework

    Root abstract class for all agents.

    All professional agents must inherit
    from this class.

    Example:

        class ResearchAgent(BaseAgent):

            def run(self, context):
                pass

    """

    VERSION = "1.0.0"


    def __init__(
        self,
        name="base",
        description="",
        version=None,
        capabilities=None,
        tools=None,
        config=None,
    ):

        # ==========================
        # Identity
        # ==========================

        self.agent_id = str(uuid.uuid4())

        self.name = name

        self.description = description

        self.version = version or self.VERSION


        # ==========================
        # Metadata
        # ==========================

        self.metadata = {
            "created_at": datetime.utcnow(),
            "framework": "Arman StudioOS",
            "type": self.__class__.__name__,
        }


        # ==========================
        # Runtime State
        # ==========================

        self.enabled = True

        self.status = "initialized"

        self.created_at = datetime.utcnow()

        self.last_run = None


        # ==========================
        # Configuration
        # ==========================

        self.config = config or {}


        # ==========================
        # Capabilities
        # ==========================

        self.capabilities = capabilities or []


        # ==========================
        # Tools
        # ==========================

        self.tools = tools or []


        # ==========================
        # Context
        # ==========================

        self.context = None


        # ==========================
        # Memory
        # ==========================

        self.memory = None


        # ==========================
        # Hooks
        # ==========================

        self.hooks = {
            "before_run": [],
            "after_run": [],
            "on_error": [],
        }


        # ==========================
        # Statistics
        # ==========================

        self.stats = {

            "total_runs": 0,

            "successful_runs": 0,

            "failed_runs": 0,

            "total_execution_time": 0,

        }


        # ==========================
        # Initialize
        # ==========================

        self.initialize()


    # =====================================================
    # Lifecycle
    # =====================================================

    def initialize(self):
        """
        Agent initialization lifecycle.
        """

        self.status = "ready"


    def before_run(self, context=None):
        """
        Called before execution.
        """

        self.context = context


    def after_run(self, result):
        """
        Called after successful execution.
        """

        return result


    def cleanup(self):
        """
        Cleanup resources.
        """

        pass


    def reset(self):
        """
        Reset runtime state.
        """

        self.context = None

        self.status = "ready"


    # =====================================================
    # Main Execution
    # =====================================================

    @abstractmethod
    def run(self, input_data):
        """
        Main agent execution.

        Must be implemented
        by child agents.
        """

        pass


    def execute(self, input_data, context=None):
        """
        Enterprise execution wrapper.

        Handles:

        - lifecycle
        - statistics
        - errors
        - timing
        """

        if not self.enabled:

            raise RuntimeError(
                f"Agent {self.name} is disabled"
            )


        start = time.time()


        try:

            self.before_run(context)


            self.status = "running"


            result = self.run(input_data)


            result = self.after_run(result)


            self.stats["successful_runs"] += 1


            self.status = "completed"


            return result


        except Exception as error:


            self.stats["failed_runs"] += 1


            self.status = "error"


            self.handle_error(error)


            raise


        finally:


            duration = time.time() - start


            self.stats["total_runs"] += 1


            self.stats["total_execution_time"] += duration


            self.last_run = datetime.utcnow()

    # =====================================================
    # Error Handling
    # =====================================================

    def handle_error(self, error):
        """
        Centralized error handling.

        Sends errors to registered hooks.
        """

        error_data = {

            "agent": self.name,

            "agent_id": self.agent_id,

            "error": str(error),

            "type": error.__class__.__name__,

            "traceback": traceback.format_exc(),

            "time": datetime.utcnow(),

        }


        for hook in self.hooks["on_error"]:

            try:

                hook(error_data)

            except Exception:

                pass



    # =====================================================
    # Hook System
    # =====================================================

    def add_hook(self, event, callback):
        """
        Register lifecycle hooks.

        Supported:

        before_run
        after_run
        on_error
        """

        if event not in self.hooks:

            raise ValueError(
                f"Unsupported hook event: {event}"
            )


        self.hooks[event].append(callback)



    def remove_hook(self, event, callback):
        """
        Remove registered hook.
        """

        if event in self.hooks:

            if callback in self.hooks[event]:

                self.hooks[event].remove(callback)



    def trigger_hook(self, event, data=None):
        """
        Execute hooks manually.
        """

        if event not in self.hooks:

            return


        for callback in self.hooks[event]:

            try:

                callback(data)

            except Exception:

                pass



    # =====================================================
    # Capability System
    # =====================================================

    def add_capability(self, capability):
        """
        Add new agent capability.
        """

        if capability not in self.capabilities:

            self.capabilities.append(capability)



    def remove_capability(self, capability):
        """
        Remove capability.
        """

        if capability in self.capabilities:

            self.capabilities.remove(capability)



    def has_capability(self, capability):
        """
        Check capability availability.
        """

        return capability in self.capabilities



    def list_capabilities(self):
        """
        Return all capabilities.
        """

        return self.capabilities.copy()



    # =====================================================
    # Tool Management
    # =====================================================

    def add_tool(self, tool):
        """
        Attach tool to agent.
        """

        if tool not in self.tools:

            self.tools.append(tool)



    def remove_tool(self, tool):
        """
        Remove tool.
        """

        if tool in self.tools:

            self.tools.remove(tool)



    def has_tool(self, tool_name):
        """
        Check tool availability.
        """

        for tool in self.tools:

            if getattr(tool, "name", None) == tool_name:

                return True


        return False



    def get_tool(self, tool_name):
        """
        Retrieve tool instance.
        """

        for tool in self.tools:

            if getattr(tool, "name", None) == tool_name:

                return tool


        return None



    # =====================================================
    # Context & Memory
    # =====================================================

    def set_context(self, context):
        """
        Inject execution context.
        """

        self.context = context



    def set_memory(self, memory):
        """
        Attach memory manager.
        """

        self.memory = memory



    def remember(self, key, value):
        """
        Store information using memory layer.

        Compatible with future Memory System.
        """

        if self.memory:

            return self.memory.store(
                key,
                value
            )


        return False



    def recall(self, key):
        """
        Retrieve information from memory.
        """

        if self.memory:

            return self.memory.retrieve(
                key
            )


        return None



    # =====================================================
    # Configuration
    # =====================================================

    def update_config(self, key, value):
        """
        Update runtime configuration.
        """

        self.config[key] = value



    def get_config(self, key, default=None):
        """
        Read configuration value.
        """

        return self.config.get(
            key,
            default
        )
    # =====================================================
    # Agent Control
    # =====================================================

    def enable(self):
        """
        Enable agent execution.
        """

        self.enabled = True

        self.status = "ready"



    def disable(self):
        """
        Disable agent execution.
        """

        self.enabled = False

        self.status = "disabled"



    def is_enabled(self):
        """
        Check agent availability.
        """

        return self.enabled



    # =====================================================
    # Health Monitoring
    # =====================================================

    def health(self):
        """
        Return agent health status.

        Used by Runtime,
        Diagnostics and Monitoring.
        """

        return {

            "agent_id": self.agent_id,

            "name": self.name,

            "status": self.status,

            "enabled": self.enabled,

            "last_run": self.last_run,

            "statistics": self.stats,

        }



    # =====================================================
    # Information & Serialization
    # =====================================================

    def info(self):
        """
        Return complete agent information.
        """

        return {

            "id": self.agent_id,

            "name": self.name,

            "description": self.description,

            "version": self.version,

            "capabilities": self.capabilities,

            "tools": [

                getattr(
                    tool,
                    "name",
                    str(tool)
                )

                for tool in self.tools

            ],

            "status": self.status,

            "enabled": self.enabled,

        }



    def serialize(self):
        """
        Convert agent state into
        serializable dictionary.

        Used by:

        - Persistence
        - Debugging
        - API Layer
        """

        return {

            "agent_id": self.agent_id,

            "name": self.name,

            "version": self.version,

            "description": self.description,

            "config": self.config,

            "capabilities": self.capabilities,

            "status": self.status,

            "stats": self.stats,

            "created_at": self.created_at.isoformat(),

            "last_run":

                self.last_run.isoformat()

                if self.last_run

                else None,

        }



    # =====================================================
    # Debug Utilities
    # =====================================================

    def __repr__(self):
        """
        Developer friendly representation.
        """

        return (

            f"<Agent "

            f"{self.name} "

            f"v{self.version} "

            f"status={self.status}>"

        )