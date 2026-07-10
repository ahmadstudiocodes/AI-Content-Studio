from dataclasses import dataclass


@dataclass
class PromptObject:

    system: str = ""

    channel: str = ""

    context: str = ""

    rules: str = ""

    output_format: str = ""

    user_request: str = ""

    prompt: str = ""