from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def __call__(self, text):
        """调用大语言模型并返回结果"""
        pass


class LLMFactory:
    @staticmethod
    def create_llm(llm_config: dict) -> LLM:
        """
        根据提供者名称创建对应的 LLM 实例。

        参数:
            llm_config (dict): 包含 LLM 配置的字典。

        返回:
            LLM 实例。
        """
        provider = llm_config["type"].lower()
        if provider == 'aliyun':
            from src.llm.aliyun_llm import AliyunLLM
            return AliyunLLM(**llm_config[provider])
        elif provider == 'openai':
            from src.llm.openai_llm import OpenaiLLM
            print(provider, llm_config[provider])
            return OpenaiLLM(**llm_config[provider])
        else:
            raise ValueError(f"未知的 LLM 提供者: {provider}")