from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def __call__(self, text):
        """调用大语言模型并返回结果"""
        pass


class LLMFactory:
    @staticmethod
    def create_llm(provider: str, **kwargs) -> LLM:
        """
        根据提供者名称创建对应的 LLM 实例。

        参数:
            provider (str): LLM 提供者名称，如 'aliyun' 或 'openai'。
            kwargs: 传递给 LLM 实现的其他参数。

        返回:
            LLM 实例。
        """
        if provider.lower() == 'aliyun':
            from src.llm.aliyun_llm import AliyunLLM
            return AliyunLLM(**kwargs)
        elif provider.lower() == 'openai':
            from src.llm.openai_llm import OpenaiLLM
            return OpenaiLLM(**kwargs)
        else:
            raise ValueError(f"未知的 LLM 提供者: {provider}")