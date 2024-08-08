from abc import ABC, abstractmethod

class IAudioPlayer(ABC):
    @abstractmethod
    def play(self, audio_data):
        pass
    
    @abstractmethod
    def cancel_play():
        pass
    
    @abstractmethod
    def feed_finish():
        pass
    
    @abstractmethod
    def start_play():
        pass