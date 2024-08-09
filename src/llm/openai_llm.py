from src.llm.base import LLM
from openai import OpenAI

class OpenaiLLM(LLM):
    def __init__(self, api_key=None, base_url='https://api.openai.com/v1', model="gpt-4o-mini", prompt=None, **kwargs):
        self.model = model
        self.prompt = prompt
        print(api_key, base_url)
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def __call__(self, text):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                # {"role": "system", "content": self.prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
