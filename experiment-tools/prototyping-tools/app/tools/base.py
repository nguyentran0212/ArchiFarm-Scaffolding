from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        pass