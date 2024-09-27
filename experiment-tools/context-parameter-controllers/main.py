"""
Add a FAST API for endpoint: /experiment-tools/

PUT {toolID: "toolID", op: "op_name" kwargs: {...}} to invoke an operation of the tool with the given kwargs

GET /experiment-tools/ can get the list of all available tools.
"""

import uvicorn
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/context-controller")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
