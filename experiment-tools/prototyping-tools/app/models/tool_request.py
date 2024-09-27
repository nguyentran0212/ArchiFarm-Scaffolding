from pydantic import BaseModel
from typing import Dict, Any

class PrototypingRequest(BaseModel):
    toolID: str
    op: str
    kwargs: Dict[str, Any]

class PrototypingResponse(BaseModel):
    experiment_id: str
    experiment_status: str
    start_time: float
    end_time: float = -1

class AvailableToolsResponse(BaseModel):
    available_tools: list[str]