import datetime
from io import BytesIO
import json
import random
import string
import uuid
import zipfile
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
from app.models.tool_request import PrototypingRequest, PrototypingResponse, AvailableToolsResponse
from app.tools import get_tool, available_tools
from loguru import logger

router = APIRouter()

import os

mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
client = AsyncIOMotorClient(f"mongodb://{mongodb_host}:27017")
cache = {}

@router.get("/prototyping-tools/", response_model=AvailableToolsResponse)
async def get_available_tools():
    return AvailableToolsResponse(available_tools=list(available_tools.keys()))

@router.post("/prototyping-tools/run-experiment", response_model=PrototypingResponse)
async def run_experiment(request: PrototypingRequest):
    tool = get_tool(request.toolID)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    if request.op not in tool.keys():
        raise HTTPException(status_code=400, detail="Operation not supported")

    try:
        result = {
            "experiment_id": str(uuid.uuid4()),
            "experiment_status": "running",
            "start_time": datetime.datetime.now().timestamp()
        }
        cache[result["experiment_id"]] = result
        # randomly add a fake estimate of time to completion to the cache from 1 to 30 seconds
        time_to_completion = random.randint(1, 30)
        cache[result["experiment_id"]]["time_to_completion"] = time_to_completion
        logger.info(f"Experiment {result['experiment_id']} started")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prototyping-tools/get-experiment-status/{experiment_id}", response_model=PrototypingResponse)
async def get_experiment_status(experiment_id: str):
    # if the experiment is not in the cache, return an error
    if experiment_id not in cache:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # check whether the experiment is still running
    end_time = cache[experiment_id]["start_time"] + cache[experiment_id]["time_to_completion"]
    if datetime.datetime.now().timestamp() > end_time:
        cache[experiment_id]["experiment_status"] = "completed"
        cache[experiment_id]["end_time"] = end_time
        return PrototypingResponse(**cache[experiment_id])

    # if the experiment is not running, return the result
    if cache[experiment_id]["experiment_status"] != "running":
        return PrototypingResponse(**cache[experiment_id])

    # if the experiment is running, return the status
    return PrototypingResponse(**cache[experiment_id])
@router.get("/prototyping-tools/get-experiment-results/{experiment_id}")
async def get_experiment_results(experiment_id: str):
    # if the experiment is not in the cache, return an error
    if experiment_id not in cache:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # if experiment is still running, return an error
    if cache[experiment_id]["experiment_status"] == "running":
        raise HTTPException(status_code=400, detail="Experiment still running")

    # convert the cache[experiment_id] to a string
    result = str(cache[experiment_id])
    # Create a zip file with the random string
    zip_file = BytesIO()
    with zipfile.ZipFile(zip_file, 'w') as zip_ref:
        zip_ref.writestr(f"{experiment_id}.txt", result.encode())
    zip_file.seek(0)
    # Return the zip file
    return StreamingResponse(zip_file, media_type="application/zip")

@router.post("/prototyping-tools/store-experiment-result")
async def store_experiment_result(
    experiment_id: str = Form(...),
    metadata: str = Form(...),
    file: UploadFile = File(...)
):
    # MongoDB connection
    db = client.get_database("experiment_db")
    fs = AsyncIOMotorGridFSBucket(db)
    try:
        # convert metadata to a dictionary
        metadata = json.loads(metadata)
        if not isinstance(metadata, dict):
            raise HTTPException(status_code=400, detail="Metadata must be a JSON string")
        # Read the file content
        file_content = await file.read()

        # Store the file in GridFS
        file_id = await fs.upload_from_stream(
            file.filename,
            file_content,
            metadata={"experiment_id": experiment_id}
        )

        logger.info(f"File {file.filename} uploaded to GridFS with ID {file_id}")

        # Prepare the experiment result document
        experiment_result = {
            "experiment_id": experiment_id,
            "file_id": str(file_id),
            "filename": file.filename,
            "metadata": metadata,
            "upload_time": datetime.datetime.now()
        }

        # Insert the experiment result into the experiment_results collection
        result = await db.experiment_results.insert_one(experiment_result)

        return {
            "message": "Experiment result stored successfully",
            "experiment_id": experiment_id,
            "file_id": str(file_id),
            "result_id": str(result.inserted_id)
        }
    except Exception as e:
        logger.error(f"Error storing experiment result: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error storing experiment result: {str(e)}")

@router.get("/prototyping-tools/get-experiment-file/{experiment_id}")
async def get_experiment_file(experiment_id: str):
    # MongoDB connection
    db = client.get_database("experiment_db")
    fs = AsyncIOMotorGridFSBucket(db)
    try:
        # Find the experiment result
        experiment_result = await db.experiment_results.find_one({"experiment_id": experiment_id})
        if not experiment_result:
            raise HTTPException(status_code=404, detail="Experiment result not found")

        # Get the file from GridFS
        file_id = ObjectId(experiment_result["file_id"])
        grid_out = await fs.open_download_stream(file_id)

        # Read the file content
        file_content = await grid_out.read()

        # Return the file as a downloadable attachment
        return StreamingResponse(
            BytesIO(file_content),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={experiment_result['filename']}"}
        )
    except Exception as e:
        logger.error(f"Error retrieving experiment file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving experiment file: {str(e)}")