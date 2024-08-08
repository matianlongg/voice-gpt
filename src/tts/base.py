from abc import ABC, abstractmethod

class TTS(ABC):
    @abstractmethod
    def interrupt(self):
        """打断语音合成"""
        pass
    
    @abstractmethod
    def call_synthesizer(self, text: str):
        """调用语音合成器合成给定文本的语音"""
        pass
    
    @abstractmethod
    def streaming_complete(self):
        """通知语音合成流已完成"""
        pass
    

class TTSFactory:
    @staticmethod
    def create_tts(provider: str, **kwargs) -> TTS:
        """
        根据提供者名称创建对应的 TTS 实例。

        参数:
            provider (str): TTS 提供者名称，如 'aliyun' 或 'openai'。
            kwargs: 传递给 TTS 实现的其他参数。

        返回:
            TTS 实例。
        """
        if provider.lower() == 'aliyun':
            from src.tts.aliyun_tts import AliyunTTS
            return AliyunTTS(**kwargs)
        else:
            raise ValueError(f"未知的 TTS 提供者: {provider}")