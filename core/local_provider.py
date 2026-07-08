import time
import requests


class LocalProvider:
    """
    Local LLM Provider for Arman StudioOS

    Sends prompts to local Ollama server.
    """


    def __init__(
        self,
        model: str = "qwen3:4b",
        host: str = "http://localhost:11434"
    ):

        self.model = model
        self.host = host.rstrip("/")


    def generate(
        self,
        prompt: str,
        temperature: float = 0.2
    ) -> str:

        url = f"{self.host}/api/generate"


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": temperature

            }

        }


        start_time = time.time()


        try:

            response = requests.post(

                url,

                json=payload,

                timeout=300

            )


            response.raise_for_status()


            data = response.json()


            result = data.get(
                "response",
                ""
            ).strip()


            elapsed = time.time() - start_time


            print(
                f"[LOCAL PROVIDER] Generation time: {elapsed:.2f}s"
            )


            return result



        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Cannot connect to Ollama. Make sure Ollama is running."
            )


        except requests.exceptions.Timeout:

            elapsed = time.time() - start_time


            print(
                f"[LOCAL PROVIDER] Timeout after: {elapsed:.2f}s"
            )


            raise RuntimeError(
                "Ollama request timed out."
            )


        except Exception as e:

            raise RuntimeError(
                f"LocalProvider Error: {e}"
            )



local_provider = LocalProvider()