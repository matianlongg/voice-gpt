from abc import ABC, abstractmethod

class ILLM(ABC):
    @abstractmethod
    def __call__(self, text):
        raise NotImplementedError("Subclasses must implement this method")
