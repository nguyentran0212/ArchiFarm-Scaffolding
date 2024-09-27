from .base import BaseTool
from typing import Dict, Any, List

class ComputeTool(BaseTool):
    def create_model(self, layers: List[int], activation: str) -> Dict[str, Any]:
        return {
            "model_type": "Neural Network",
            "layers": layers,
            "activation": activation,
            "created": True
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        return self.create_model(**kwargs)