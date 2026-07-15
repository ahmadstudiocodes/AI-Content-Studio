from datetime import datetime
import time
import traceback

from brain.base_agent import BaseAgent


class AgentManager:
    """
    Arman StudioOS

    Enterprise Agent Manager

    Responsible for:

    - Agent registration
    - Agent lifecycle
    - Agent execution
    - Agent monitoring
    - Agent statistics
    - Agent state management

    Future integrations:

    - Runtime
    - EventBus
    - Scheduler
    - PluginManager
    """


    VERSION = "1.0.0"



    def __init__(self):

        # Registered agents

        self.agents = {}


        # Execution history

        self.history = []


        # Errors

        self.errors = []


        # Manager state

        self.created_at = datetime.utcnow()

        self.status = "ready"



    # =====================================================
    # Registration
    # =====================================================


    def register(self, agent):
        """
        Register an agent.

        Agent must inherit from BaseAgent.
        """

        if not isinstance(agent, BaseAgent):

            raise TypeError(
                "Agent must inherit from BaseAgent"
            )


        self.agents[agent.name] = agent


        return agent



    def unregister(self, name):
        """
        Remove agent.
        """

        if name in self.agents:

            agent = self.agents[name]

            agent.cleanup()

            del self.agents[name]


            return True


        return False



    def exists(self, name):
        """
        Check agent existence.
        """

        return name in self.agents



    def get(self, name):
        """
        Get agent instance.
        """

        return self.agents.get(name)



    def list_agents(self):
        """
        Return registered agents.
        """

        return list(
            self.agents.keys()
        )



    def count(self):
        """
        Return number of agents.
        """

        return len(
            self.agents
        )



    # =====================================================
    # Lifecycle Management
    # =====================================================


    def enable_agent(self, name):
        """
        Enable specific agent.
        """

        agent = self.get(name)


        if not agent:

            return False


        agent.enable()


        return True



    def disable_agent(self, name):
        """
        Disable specific agent.
        """

        agent = self.get(name)


        if not agent:

            return False


        agent.disable()


        return True



    def reset_agent(self, name):
        """
        Reset agent state.
        """

        agent = self.get(name)


        if not agent:

            return False


        agent.reset()


        return True



    def shutdown_agent(self, name):
        """
        Shutdown agent.
        """

        agent = self.get(name)


        if not agent:

            return False


        agent.cleanup()

        agent.disable()


        return True
    # =====================================================
    # Agent Execution
    # =====================================================


    def execute(
        self,
        agent_name,
        input_data,
        context=None
    ):
        """
        Execute an agent.

        Provides centralized execution control.
        """

        agent = self.get(agent_name)


        if not agent:

            raise ValueError(
                f"Agent not found: {agent_name}"
            )


        start_time = time.time()


        execution_record = {

            "agent": agent_name,

            "start_time": datetime.utcnow(),

            "status": "running",

        }


        try:

            result = agent.execute(
                input_data,
                context
            )


            duration = (
                time.time()
                -
                start_time
            )


            execution_record.update({

                "status": "success",

                "duration": duration,

                "completed_at":
                    datetime.utcnow(),

            })


            self.history.append(
                execution_record
            )


            return result



        except Exception as error:


            duration = (
                time.time()
                -
                start_time
            )


            execution_record.update({

                "status": "failed",

                "duration": duration,

                "error": str(error),

                "traceback":
                    traceback.format_exc(),

            })


            self.errors.append(
                execution_record
            )


            self.history.append(
                execution_record
            )


            raise



    # =====================================================
    # Bulk Operations
    # =====================================================


    def execute_all(
        self,
        input_data,
        context=None
    ):
        """
        Execute all registered agents.
        """

        results = {}


        for name in self.agents:

            try:

                results[name] = self.execute(
                    name,
                    input_data,
                    context
                )


            except Exception as error:

                results[name] = {

                    "error": str(error)

                }


        return results



    # =====================================================
    # Health Monitoring
    # =====================================================


    def health(self, name=None):
        """
        Return health information.

        If name provided:
            returns single agent health

        Otherwise:
            returns all agents
        """


        if name:

            agent = self.get(name)


            if not agent:

                return None


            return agent.health()



        return {

            name:
                agent.health()

            for name, agent

            in self.agents.items()

        }



    # =====================================================
    # Statistics
    # =====================================================


    def statistics(self):
        """
        Return manager statistics.
        """

        return {

            "total_agents":
                len(self.agents),


            "total_executions":
                len(self.history),


            "total_errors":
                len(self.errors),


            "status":
                self.status,


        }



    def agent_statistics(self, name):
        """
        Return specific agent statistics.
        """

        agent = self.get(name)


        if not agent:

            return None


        return agent.stats



    # =====================================================
    # History
    # =====================================================


    def get_history(
        self,
        limit=None
    ):
        """
        Return execution history.
        """

        if limit:

            return self.history[-limit:]


        return self.history.copy()



    def clear_history(self):
        """
        Clear execution logs.
        """

        self.history.clear()



    def clear_errors(self):
        """
        Clear error logs.
        """

        self.errors.clear()
    
    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Export manager state.

        Used for:

        - Persistence
        - Debugging
        - API
        """

        return {

            "version": self.VERSION,

            "created_at":
                self.created_at.isoformat(),


            "status":
                self.status,


            "agents": [

                agent.serialize()

                for agent

                in self.agents.values()

            ],


            "statistics":
                self.statistics(),

        }



    # =====================================================
    # Manager Information
    # =====================================================


    def info(self):
        """
        Return manager information.
        """

        return {

            "name":
                "AgentManager",


            "version":
                self.VERSION,


            "status":
                self.status,


            "agent_count":
                len(self.agents),


            "agents":
                self.list_agents(),

        }



    # =====================================================
    # Runtime Control
    # =====================================================


    def enable_all(self):
        """
        Enable all agents.
        """

        for agent in self.agents.values():

            agent.enable()



    def disable_all(self):
        """
        Disable all agents.
        """

        for agent in self.agents.values():

            agent.disable()



    def reset_all(self):
        """
        Reset all agents.
        """

        for agent in self.agents.values():

            agent.reset()



    def shutdown_all(self):
        """
        Shutdown all agents.
        """

        for agent in self.agents.values():

            agent.cleanup()

            agent.disable()



    # =====================================================
    # Debug
    # =====================================================


    def __repr__(self):
        """
        Developer representation.
        """

        return (

            f"<AgentManager "

            f"agents={len(self.agents)} "

            f"status={self.status}>"

        )