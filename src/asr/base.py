from abc import ABC, abstractmethod

class ASR(ABC):
    @abstractmethod
    def start(self):
        """启动语音识别"""
        pass

    @abstractmethod
    def stop(self):
        """停止语音识别"""
        pass

    @abstractmethod
    def send_audio_frame(self, frame):
        """发送音频帧进行识别"""
        pass
    
class ASRFactory:
    @staticmethod
    def create_asr(asr_config: dict, **kwargs) -> ASR:
        """
        根据提供者名称创建对应的 ASR 实例。

        参数:
            provider (str): ASR 提供者名称，如 'aliyun' 或 'openai'。
            kwargs: 传递给 ASR 实现的其他参数。

        返回:
            ASR 实例。
        """
        provider = asr_config["type"].lower()
        combined_config = {**asr_config[provider], **kwargs}
        print(combined_config)
        if provider == 'aliyun':
            from src.asr.aliyun_asr import AliyunASR
            return AliyunASR(**combined_config)
        elif provider == 'openai':
            from src.asr.openai_asr import OpenAIASR
            return OpenAIASR(**combined_config)
        else:
            raise ValueError(f"未知的 ASR 提供者: {provider}")