from abc import ABC, abstractmethod

class AudioInput(ABC):
    @abstractmethod
    def start(self):
        """启动音频输入流"""
        pass

    @abstractmethod
    def stop(self):
        """停止音频输入流"""
        pass

    @abstractmethod
    def is_working(self):
        """检查音频输入流当前是否处于活动状态"""
        pass