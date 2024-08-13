from abc import ABC, abstractmethod

class Memory(ABC):
    @abstractmethod
    def search_memories(self, query, user_id):
        """查询记忆"""
        pass
    
    @abstractmethod
    def get_memories(self, user_id):
        """获取记忆"""
        pass

    @abstractmethod
    def add_memories(self, query, user_id):
        """添加记忆"""
        pass

class MemoryFactory:
    @staticmethod
    def create_memory(memory_config: dict) -> Memory:
        """
        根据提供者名称创建对应的 memory 实例。

        参数:
            memory_config (dict): 包含 memory 配置的字典。

        返回:
            memory 实例。
        """
        provider = memory_config["type"].lower()
        try:
            if provider == 'mem0':
                from src.memory.mem0_memory import Mem0Memory
                return Mem0Memory(**memory_config[provider])
            else:
                raise ValueError(f"未知的 Memory 提供者: {provider}")
        except:
            return None