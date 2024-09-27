"""
Add a FAST API for endpoint: /prototyping-tools/

PUT {toolID: "toolID", op: "op_name" kwargs: {...}} to invoke an operation of the tool with the given kwargs

GET /prototyping-tools/ can get the list of all available tools.
"""


from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)