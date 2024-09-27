import random
import time
import uuid
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.tool_request import ToolRequest
from app.models.context_request import ContextRequest
from app.tools import tools

router = APIRouter()

cache = {}

@router.post("/context/set")
async def set_context(request: ContextRequest):
    context_id = str(uuid.uuid4())
    cache[context_id] = request.model_dump()
    # fake a random timeer to simulate the time it takes to set the context
    # randtom from 1 to 5 seconds
    time.sleep(random.uniform(1, 5))
    return {
        "id": context_id,
        "task": "Context set",
        "status": "success",
        "context": cache[context_id]
    }

@router.post("/context/reset/{context_id}")
async def reset_context(context_id: str):
    if context_id not in cache:
        raise HTTPException(status_code=404, detail="Context not found")
    
    context = cache.pop(context_id)
    # fake a random timeer to simulate the time it takes to reset the context
    # randtom from 1 to 5 seconds
    time.sleep(random.uniform(1, 5))
    return {
        "task": "Context reset",
        "status": "success",
        "context": context
    }

@router.put("/")
async def invoke_tool(request: ToolRequest):
    if request.toolID not in tools:
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = tools[request.toolID]
    if request.op not in tool.get_operations():
        raise HTTPException(status_code=404, detail="Operation not found")

    try:
        operation = getattr(tool, request.op)
        result = operation(**request.kwargs)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_tools() -> List[Dict[str, Any]]:
    return [
        {
            "toolID": tool_id,
            "operations": tool.get_operations()
        }
        for tool_id, tool in tools.items()
    ]