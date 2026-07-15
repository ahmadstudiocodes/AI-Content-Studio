# brain/agent_result.py

from datetime import datetime
import uuid
from copy import deepcopy



class AgentResult:
    """
    Arman StudioOS

    Enterprise Agent Result

    Standard response container
    for every Agent execution.

    Responsibilities
    ----------------

    - Store output
    - Track execution status
    - Handle errors
    - Store metadata
    - Support serialization
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        success=True,
        data=None,
        message="",
        error=None,
        metadata=None,
    ):


        # Identity

        self.result_id = str(
            uuid.uuid4()
        )


        self.created_at = datetime.utcnow()



        # Status

        self.success = success


        self.status = (
            "success"
            if success
            else
            "failed"
        )



        # Data

        self.data = data



        # Message

        self.message = message



        # Error

        self.error = error



        # Metadata

        self.metadata = metadata or {}



        # Execution Info

        self.execution_time = 0


        self.agent_name = None


        self.trace_id = str(
            uuid.uuid4()
        )
    
    # =====================================================
    # Factory Methods
    # =====================================================


    @classmethod
    def success_result(
        cls,
        data=None,
        message="",
        metadata=None
    ):
        """
        Create successful result.
        """

        return cls(

            success=True,

            data=data,

            message=message,

            metadata=metadata

        )



    @classmethod
    def error_result(
        cls,
        error,
        message=""
    ):
        """
        Create failed result.
        """

        return cls(

            success=False,

            error=str(error),

            message=message

        )



    # =====================================================
    # Execution Tracking
    # =====================================================


    def set_agent(
        self,
        agent_name
    ):
        """
        Attach source agent.
        """

        self.agent_name = agent_name



    def set_execution_time(
        self,
        duration
    ):
        """
        Store execution duration.
        """

        self.execution_time = duration



    # =====================================================
    # Metadata
    # =====================================================


    def add_metadata(
        self,
        key,
        value
    ):
        """
        Add metadata field.
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
    # Status
    # =====================================================


    def is_success(self):
        """
        Check success state.
        """

        return self.success



    def is_failed(self):
        """
        Check failure state.
        """

        return not self.success



    # =====================================================
    # Serialization
    # =====================================================


    def serialize(self):
        """
        Convert result to dictionary.
        """

        return {

            "result_id":
                self.result_id,


            "status":
                self.status,


            "success":
                self.success,


            "data":
                self.data,


            "message":
                self.message,


            "error":
                self.error,


            "agent_name":
                self.agent_name,


            "execution_time":
                self.execution_time,


            "trace_id":
                self.trace_id,


            "metadata":
                deepcopy(
                    self.metadata
                ),


            "created_at":
                self.created_at.isoformat(),

        }



    # =====================================================
    # Debug
    # =====================================================


    def __repr__(self):

        return (

            f"<AgentResult "

            f"status={self.status} "

            f"agent={self.agent_name}>"

        )