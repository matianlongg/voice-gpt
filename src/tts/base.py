from abc import ABC, abstractmethod

class ITTS(ABC):
    @abstractmethod
    def interrupt(self):
        pass
    
    @abstractmethod
    def call_synthesizer(self, text: str):
        pass
    
    @abstractmethod
    def streaming_complete(self):
        pass