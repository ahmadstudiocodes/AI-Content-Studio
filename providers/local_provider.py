import requests
import time


class LocalProvider:

    """
    Local LLM Provider for Arman StudioOS

    Optimized for agent execution.
    """

    def __init__(
        self,
        model="qwen3:4b",
        host="http://localhost:11434"
    ):

        self.name = "local"
        self.type = "llm"

        self.model = model
        self.host = host

    def available(self):

        try:

            response = requests.get(
                self.host,
                timeout=5
            )

            return response.status_code == 200

        except Exception:

            return False

    def generate(
        self,
        prompt,
        think=False,
        temperature=0.3,
        max_tokens=2500
    ):

        url = f"{self.host}/api/chat"

        payload = {

            "model": self.model,

            "messages": [

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            "stream": False,

            "think": think,

            "options": {

                "num_predict": max_tokens,

                "temperature": temperature,

                "top_p": 0.85,

                "top_k": 40,

                "repeat_penalty": 1.12

            }

        }

        start_time = time.time()

        try:

            print(
                "[LOCAL PROVIDER] Sending request"
            )

            response = requests.post(

                url,

                json=payload,

                timeout=360

            )

            response.raise_for_status()

            data = response.json()

            elapsed = time.time() - start_time

            print(
                f"[LOCAL PROVIDER] Generation time: {elapsed:.2f}s"
            )

            text = (

                data
                .get("message", {})
                .get("content", "")

            )

            if not text:

                text = data.get(
                    "response",
                    ""
                )

            if not text:

                print(
                    "[LOCAL PROVIDER] Empty response"
                )

                return ""

            # Remove Qwen thinking blocks

            if "<think>" in text:

                text = text.split(
                    "<think>",
                    1
                )[0]

            if "</think>" in text:

                text = text.split(
                    "</think>",
                    1
                )[-1]

            return text.strip()

        except Exception as e:

            print(
                "[LOCAL PROVIDER ERROR]",
                e
            )

            return ""