from src.llm.base import LLM
from src.memory.base import Memory
from openai import OpenAI

import os

class OpenaiLLM(LLM):
    def __init__(self, api_key=None, base_url='https://api.openai.com/v1', model="gpt-4o-mini", prompt=None, memory: Memory=None, **kwargs):
        self.model = model
        self.prompt = prompt
        self.message_history = [{"role": "system", "content": self.prompt}]
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.memory = memory
        self.user_id = 1

    def __call__(self, text):
        prompt = text
        if self.memory:
            previous_memories = self.memory.search_memories(text, user_id=self.user_id)
            if previous_memories:
                prompt = f"用户输入: {text}\n 以前的记忆: {previous_memories}"
        self.message_history.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.message_history
        )
        assistant_message = response.choices[0].message.content

        self.message_history.append({"role": "assistant", "content": assistant_message})
        if self.memory:
            self.memory.add_memories(text, user_id=self.user_id)
        return assistant_message