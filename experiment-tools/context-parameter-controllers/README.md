# Context Parameter Controller Tools

This directory contains tools for setting and resetting contextual parameters in Architecture Farming experiments (e.g., changing network parameters of a testbed infrastructure to specify the network constraint). These tools are accessed by the ArchiFarm core via REST API. A server for calling tools is provided.

## Setup

1. Install Poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install the project dependencies:
   ```
   poetry install
   ```

## Running the server

To start the server, run:

```
poetry run start
```

The server will start on `http://0.0.0.0:8000`.

## API Endpoints

### 1. Invoke a Tool Operation

- **Endpoint**: `PUT /experiment-tools/`
- **Description**: Invokes an operation of a specified tool with given parameters.
- **Request Body**:
  ```json
  {
    "toolID": "string",
    "op": "string",
    "kwargs": {
      "key1": "value1",
      "key2": "value2"
    }
  }
  ```
- **Response**:
  - Success (200 OK):
    ```json
    {
      "result": "string"
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "detail": "Tool not found"
    }
    ```
    or
    ```json
    {
      "detail": "Operation not found"
    }
    ```
  - Error (400 Bad Request):
    ```json
    {
      "detail": "Error message"
    }
    ```

### 2. List Available Tools

- **Endpoint**: `GET /experiment-tools/`
- **Description**: Retrieves a list of all available tools and their operations.
- **Response**:
  - Success (200 OK):
    ```json
    [
      {
        "toolID": "string",
        "operations": ["string", "string", ...]
      },
      ...
    ]
    ```

## Available Tools and Operations

### 1. Network Tool

- **Tool ID**: `network`
- **Operations**:
  - `set_bandwidth(bandwidth: int)`: Sets the bandwidth in Mbps
  - `set_latency(latency: int)`: Sets the latency in ms

### 2. Compute Tool

- **Tool ID**: `compute`
- **Operations**:
  - `set_cpu_limit(limit: int)`: Sets the CPU limit in percentage
  - `set_memory_limit(limit: int)`: Sets the memory limit in MB

## Examples

### Invoking a Tool Operation

```bash
curl -X PUT http://localhost:8000/experiment-tools/ \
     -H "Content-Type: application/json" \
     -d '{"toolID": "network", "op": "set_bandwidth", "kwargs": {"bandwidth": 100}}'
```

### Listing Available Tools

```bash
curl -X GET http://localhost:8000/experiment-tools/
```

## How to adapt this code

1. Add the code of your experiment tools in the `context_parameter_controller/tools/` folder.
2. Modify the `context_parameter_controller/tools/__init__.py` file to import and register your new tools.
3. Update the README to include documentation for your new tools and operations.

## Running tests

To run the tests, use:

```
poetry run pytest
```