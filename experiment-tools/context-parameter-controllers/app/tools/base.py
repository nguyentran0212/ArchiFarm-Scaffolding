from abc import ABC, abstractmethod

class BaseTool(ABC):
    @classmethod
    @abstractmethod
    def get_operations(cls):
        pass