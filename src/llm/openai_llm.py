from src.llm.base import LLM
from openai import OpenAI

class OpenaiLLM(LLM):
    def __init__(self, api_key=None, base_url='https://api.openai.com/v1', model="gpt-4o-mini", prompt=None, **kwargs):
        self.model = model
        self.prompt = prompt
        self.message_history = []
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def __call__(self, text):

        self.message_history.append({"role": "user", "content": text})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_history
        )
        assistant_message = response.choices[0].message.content

        self.message_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message
