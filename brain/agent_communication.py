# brain/agent_communication.py


from datetime import datetime
from uuid import uuid4



class AgentMessage:
    """
    Standard message between agents.
    """

    def __init__(
        self,
        sender,
        receiver,
        content,
        message_type="request"
    ):

        self.id = str(
            uuid4()
        )

        self.sender = sender

        self.receiver = receiver

        self.content = content

        self.message_type = message_type

        self.created_at = datetime.utcnow()



    def to_dict(self):

        return {

            "id":
                self.id,

            "sender":
                self.sender,

            "receiver":
                self.receiver,

            "content":
                self.content,

            "type":
                self.message_type,

            "created_at":
                self.created_at.isoformat()

        }





class AgentCommunication:
    """
    Arman StudioOS

    Agent Communication Layer.


    Responsibilities:

    - Agent messaging
    - Request routing
    - Message history
    - Communication tracking
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):


        self.history = []



    # =====================================================
    # Send Message
    # =====================================================


    def send(
        self,
        sender,
        receiver,
        content,
        message_type="request"
    ):


        message = AgentMessage(

            sender,

            receiver,

            content,

            message_type

        )


        self.history.append(

            message

        )


        return message



    # =====================================================
    # Broadcast
    # =====================================================


    def broadcast(
        self,
        sender,
        receivers,
        content
    ):


        messages = []


        for receiver in receivers:

            messages.append(

                self.send(

                    sender,

                    receiver,

                    content,

                    "broadcast"

                )

            )


        return messages



    # =====================================================
    # History
    # =====================================================


    def get_history(
        self
    ):


        return [

            msg.to_dict()

            for msg in self.history

        ]



    def clear(
        self
    ):

        self.history.clear()



    # =====================================================
    # Statistics
    # =====================================================


    def count(
        self
    ):

        return len(
            self.history
        )



    def info(
        self
    ):

        return {

            "name":
                "AgentCommunication",

            "version":
                self.VERSION,

            "messages":
                self.count()

        }



# Global Instance

agent_communication = AgentCommunication()