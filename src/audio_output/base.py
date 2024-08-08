from abc import ABC, abstractmethod

class AudioOutput(ABC):
    @abstractmethod
    def play(self, audio_data):
        """播放音频数据"""
        pass
    
    @abstractmethod
    def cancel_play(self):
        """取消播放"""
        pass
    
    @abstractmethod
    def feed_finish(self):
        """结束播放"""
        pass
    
    @abstractmethod
    def start_play(self):
        """开始播放"""
        pass
