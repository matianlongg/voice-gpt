from abc import ABC, abstractmethod

class IRecognition(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_audio_frame(self, frame):
        pass