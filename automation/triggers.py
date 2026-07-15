# automation/triggers.py


from datetime import datetime
from uuid import uuid4



class TriggerRule:
    """
    Represents automation trigger rule.
    """

    def __init__(
        self,
        event,
        action,
        condition=None
    ):

        self.id = str(
            uuid4()
        )

        self.event = event

        self.action = action

        self.condition = condition

        self.enabled = True

        self.created_at = datetime.utcnow()



    def matches(
        self,
        event_name,
        data=None
    ):


        if not self.enabled:

            return False


        if self.event != event_name:

            return False



        if self.condition:

            return self.condition(data)



        return True



    def execute(
        self,
        data=None
    ):

        return self.action(data)



    def disable(
        self
    ):

        self.enabled = False



    def enable(
        self
    ):

        self.enabled = True



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "event":
                self.event,

            "enabled":
                self.enabled,

            "created_at":
                self.created_at.isoformat()

        }





class TriggerManager:
    """
    Arman StudioOS

    Automation Trigger Engine.


    Responsibilities:

    - Register triggers
    - Listen events
    - Execute actions
    """



    VERSION = "1.0.0"



    def __init__(
        self
    ):

        self.triggers = []



    # =====================================================
    # Register
    # =====================================================


    def register(
        self,
        event,
        action,
        condition=None
    ):


        trigger = TriggerRule(

            event,

            action,

            condition

        )


        self.triggers.append(

            trigger

        )


        return trigger



    # =====================================================
    # Fire Event
    # =====================================================


    def fire(
        self,
        event,
        data=None
    ):


        results = []


        for trigger in self.triggers:


            if trigger.matches(

                event,

                data

            ):


                results.append(

                    trigger.execute(

                        data

                    )

                )


        return results



    # =====================================================
    # Management
    # =====================================================


    def remove(
        self,
        trigger_id
    ):


        for trigger in self.triggers:


            if trigger.id == trigger_id:


                self.triggers.remove(

                    trigger

                )

                return True



        return False



    def list_triggers(
        self
    ):


        return [

            trigger.to_dict()

            for trigger in self.triggers

        ]



    def count(
        self
    ):

        return len(

            self.triggers

        )



    def clear(
        self
    ):

        self.triggers.clear()



    def info(
        self
    ):

        return {

            "name":
                "TriggerManager",

            "version":
                self.VERSION,

            "triggers":
                self.count()

        }





# Global Instance

trigger_manager = TriggerManager()