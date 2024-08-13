
from mem0 import Memory as mem0Memory
from src.memory.base import Memory

import os

class Mem0Memory(Memory):
    def __init__(self, api_key=None, base_url='https://api.openai.com/v1', model="gpt-4o-mini", **kwargs):
        self.model = model
        os.environ['OPENAI_API_KEY'] = api_key
        os.environ['OPENAI_BASE_URL'] = base_url
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "chat",
                    "path": "db",
                }
            }
        }
        self.memory = mem0Memory.from_config(config)
        self.user_id = 1

    def add_memories(self, query, user_id):
        """添加记忆"""
        self.memory.add(query, user_id=user_id)
    
    def get_memories(self, user_id):
        memories = self.memory.get_all(user_id=user_id)
        return [m['memory'] for m in memories]

    def search_memories(self, query, user_id):
        memories = self.memory.search(query, user_id=user_id)
        return [m['memory'] for m in memories]
