from agents.thumbnail_agent import ThumbnailAgent


class TestCommand:

    payload = "Modern Luxury House"

    class Intent:

        domain = "youtube"


    intent = Intent()

    target = "thumbnail"



print("===== THUMBNAIL AGENT TEST =====")


agent = ThumbnailAgent()


print("\n[AGENT INFO]")
print("Name:", agent.name)
print("Version:", agent.version)


command = TestCommand()


print("\n[CAN HANDLE TEST]")

print(
    agent.can_handle(command)
)


print("\n[EXECUTION TEST]")


import time

print("Sending request to agent...")

start = time.time()

result = agent.execute(command)

end = time.time()

print("Time:", end - start)


print(result)


print("\n===== TEST FINISHED =====")