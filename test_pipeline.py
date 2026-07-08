from core.execution_pipeline import pipeline
from core.registry import registry
from agents.thumbnail_agent import ThumbnailAgent


# Register Agent

thumbnail_agent = ThumbnailAgent()

registry.register(
    thumbnail_agent.name,
    thumbnail_agent
)



class TestCommand:

    raw = "create youtube course"

    action = "create"

    payload = "3ds max advanced modeling youtube course"


    class Intent:

        domain = "youtube"


    intent = Intent()


    target = "course"


    class Plan:

        status = "idle"


        def complete(self):

            self.status = "completed"


    plan = Plan()



print("===== PIPELINE TEST =====")


command = TestCommand()


result = pipeline.execute(command)


print("\nSTATUS:")
print(command.plan.status)


print("\nRESULT:")
print(result)


print("\n===== TEST FINISHED =====")