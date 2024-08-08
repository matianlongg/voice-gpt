from src.llm.base import LLM
from openai import OpenAI  # 假设你使用的是 OpenAI 的某个库

class OpenaiLLM(LLM):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def __call__(self, text):
        response = self.client.Completion.create(
            engine="davinci",
            prompt=text,
            max_tokens=150
        )
        return response.choices[0].text.strip()
