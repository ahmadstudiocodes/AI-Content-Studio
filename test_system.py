from core.validator import Validator
from core.output_cleaner import OutputCleaner
from core.prompt_builder import PromptBuilder
from core.retry_engine import RetryEngine


print("===== ARMAN SYSTEM TEST =====")


# ==================================================
# Validator
# ==================================================

validator = Validator()

good_output = """
Professional YouTube thumbnail for Modern Luxury House
"""

good_result = validator.validate(
    output=good_output,
    task="generate thumbnail",
    topic="Modern Luxury House"
)

print("\n[VALIDATOR GOOD TEST]")
print(good_result)


bad_output = """
<think>
hidden reasoning
</think>

final answer
"""

bad_result = validator.validate(
    output=bad_output,
    task="generate thumbnail",
    topic="Modern Luxury House"
)

print("\n[VALIDATOR BAD TEST]")
print(bad_result)


# ==================================================
# Output Cleaner
# ==================================================

dirty_output = """
<think>
reasoning
</think>

Thinking:

Final Thumbnail
"""

clean_result = OutputCleaner.clean(dirty_output)

print("\n[CLEANER TEST]")
print(repr(clean_result))


# ==================================================
# Prompt Builder
# ==================================================

builder = PromptBuilder()

prompt = builder.build(
    task="generate thumbnail",
    topic="Modern Luxury House",
    agent_rules="Create professional YouTube thumbnail only."
)

print("\n[PROMPT BUILDER TEST]")
print("Prompt length:", len(prompt))


# ==================================================
# Retry Engine
# ==================================================

print("\n[RETRY ENGINE TEST]")

counter = {
    "attempt": 0
}


def fake_worker():

    counter["attempt"] += 1

    if counter["attempt"] == 1:

        return """
<think>
reasoning
</think>
"""

    if counter["attempt"] == 2:

        return """
Random text without topic
"""

    return """
Professional YouTube thumbnail for Modern Luxury House
"""


retry = RetryEngine(max_retries=3)

retry_result = retry.execute(
    worker=fake_worker,
    validator=validator,
    task="generate thumbnail",
    topic="Modern Luxury House"
)

print(retry_result)


# ==================================================
# Validator Reason Test
# ==================================================

print("\n[VALIDATOR REASON TEST]")

tests = [

    ("", "EMPTY"),

    ("<think>abc</think>", "FORBIDDEN"),

    ("hello world", "TOPIC"),

    ("Modern Luxury House", "VALID")

]

for text, name in tests:

    result = validator.validate(
        output=text,
        task="generate thumbnail",
        topic="Modern Luxury House"
    )

    print(f"{name}:")
    print(result)


print("\n===== TEST FINISHED =====")