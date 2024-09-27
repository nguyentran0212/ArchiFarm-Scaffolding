from pydantic import BaseModel
from typing import Dict, Any

class ContextRequest(BaseModel):
    context: str
    environment: str
    op: str
    kwargs: Dict[str, Any]

sample_context_request = ContextRequest(
    context="development",
    environment="staging",
    op="initialize",
    kwargs={
        "key1": "value1",
        "key2": "value2"
    }
)

sample_context_request_dict = sample_context_request.dict()