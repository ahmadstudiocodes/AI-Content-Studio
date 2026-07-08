from providers.base_provider import BaseProvider
from ollama import Client
import re


class LocalProvider(BaseProvider):

    name = "local"

    def __init__(self, model="qwen3:4b"):

        self.model = model

        self.client = Client(
            host="http://127.0.0.1:11434"
        )

    def available(self):

        try:

            self.client.list()

            return True

        except Exception:

            return False

    def generate(self, prompt: str):

        print("DEBUG: Sending prompt to Ollama")

        print("=" * 40)
        print(prompt)
        print("=" * 40)

        response = self.client.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            think=False,

            options={

                "num_ctx": 4096,

                "temperature": 0.2,

                "num_predict": 2048

            }

        )

        print("DEBUG: Ollama response received")

        msg = response["message"]

        content = msg.get("content", "")

        if not content:
            content = msg.get("thinking", "")

        # حذف بلوک‌های <think>...</think>
        content = re.sub(
            r"<think>.*?</think>",
            "",
            content,
            flags=re.DOTALL,
        )

        # اگر مدل متن استدلال را بدون تگ داخل content فرستاده باشد
        if "</think>" in content:
            content = content.split("</think>")[-1]

        # حذف فاصله‌های اضافی
        content = content.strip()

        return content