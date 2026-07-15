from core.startup import startup

from core.execution_pipeline import pipeline
from agents.thumbnail_agent import ThumbnailAgent
from providers.local_provider import LocalProvider


# --------------------------------------------------
# Startup
# --------------------------------------------------

startup()


# --------------------------------------------------
# Test Command
# --------------------------------------------------

class TestCommand:

    raw = "create youtube course"

    action = "create"

    target = "course"

    payload = "3ds max advanced modeling youtube course"


    class Intent:

        domain = "youtube"

        priority = "normal"

        provider = "auto"

        need_memory = False


    intent = Intent()


    class Plan:

        def __init__(self):

            self.status = "idle"

        def complete(self):

            self.status = "completed"


    plan = Plan()


print("=" * 60)
print("PIPELINE TEST")
print("=" * 60)


command = TestCommand()

result = pipeline.execute(command)


print("\nSTATUS")
print(command.plan.status)

print("\nRESULT")
print(result)

print("\n" + "=" * 60)
print("TEST FINISHED")
print("=" * 60)