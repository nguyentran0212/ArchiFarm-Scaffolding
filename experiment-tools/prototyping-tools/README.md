# Prototyping Tools

Prototyping tool is responsible for setting the architectural parameters of a distillation before running an experiment. Generally, setting architectural parameters means generating a new prototype on the fly (e.g., sending DLT network architecture to a prototyping tool as parameter, receiving a prototype DLT network with corresponding architecture as the output). A server for calling tool is provided.

## Project Structure

```
prototyping-tools/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── tool_request.py
│   └── tools/
│       ├── __init__.py
│       ├── base.py
│       ├── network_tool.py
│       └── compute_tool.py
├── main.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
└── README.md
```

## How to adapt this code

1. Add the code of your prototyping tools in the `app/tools/` folder.
2. Modify the `app/tools/__init__.py` to import and register your new tools.

## Setup

1. Make sure you have Python 3.9+ and Poetry installed.
2. Clone this repository.
3. Install dependencies:
   ```
   poetry install
   ```

## Running the Server

To run the server locally:

```
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`.

## Running with Docker

1. Build the Docker image:
   ```
   docker build -t prototyping-tools-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 prototyping-tools-api
   ```

The API will be available at `http://localhost:8000`.

## API Usage

The API provides two endpoints:

### 1. GET /prototyping-tools/

This endpoint returns a list of all available prototyping tools.

**Example request:**
```
curl -X GET http://localhost:8000/prototyping-tools/
```

**Example response:**
```json
{
  "available_tools": ["network_tool", "compute_tool"]
}
```

### 2. PUT /prototyping-tools/

This endpoint invokes an operation of a specified prototyping tool with given parameters.

**Request body:**
```json
{
  "toolID": "string",
  "op": "string",
  "kwargs": {}
}
```

- `toolID`: The identifier of the tool you want to use.
- `op`: The name of the operation you want to perform.
- `kwargs`: A dictionary of keyword arguments for the operation.

**Example requests:**

1. Using the network tool:
```
curl -X PUT http://localhost:8000/prototyping-tools/ \
     -H "Content-Type: application/json" \
     -d '{"toolID": "network_tool", "op": "generate_network", "kwargs": {"nodes": 5, "consensus": "PoW"}}'
```

**Example response:**
```json
{
  "result": {
    "network_type": "DLT",
    "nodes": 5,
    "consensus": "PoW",
    "generated": true
  }
}
```

2. Using the compute tool:
```
curl -X PUT http://localhost:8000/prototyping-tools/ \
     -H "Content-Type: application/json" \
     -d '{"toolID": "compute_tool", "op": "create_model", "kwargs": {"layers": [64, 32, 16], "activation": "relu"}}'
```

**Example response:**
```json
{
  "result": {
    "model_type": "Neural Network",
    "layers": [64, 32, 16],
    "activation": "relu",
    "created": true
  }
}
```

## Error Handling

The API will return appropriate HTTP status codes and error messages for various scenarios:

- 404: Tool not found
- 400: Operation not supported
- 500: Internal server error (with error details)

## Extending the API

To add new prototyping tools:

1. Create a new tool class in the `app/tools/` directory.
2. Inherit from the `BaseTool` class defined in `app/tools/base.py`.
3. Implement the required methods for your new tool.
4. Add the new tool to the `available_tools` dictionary in `app/tools/__init__.py`.

Remember to update the README with any new tools or operations you add.

## Development

For development purposes, you can run the server with auto-reload:

```
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

This will automatically restart the server when you make changes to the code.