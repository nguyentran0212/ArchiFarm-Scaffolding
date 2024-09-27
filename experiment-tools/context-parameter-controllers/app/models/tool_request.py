from pydantic import BaseModel
from typing import Dict, Any

class ToolRequest(BaseModel):
    toolID: str
    op: str
    kwargs: Dict[str, Any]