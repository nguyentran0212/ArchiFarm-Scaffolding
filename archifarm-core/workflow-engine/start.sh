#!/bin/bash

# check if the data_storage directory exists, if not create it
if [ ! -d "data_storage" ]; then
    mkdir data_storage
    # grant permissions to the data_storage directory
    chmod -R 777 data_storage
fi

# check if the n8n_storage directory exists, if not create it
if [ ! -d "n8n_storage" ]; then
    mkdir n8n_storage
    # grant permissions to the n8n_storage directory
    chmod -R 777 n8n_storage
fi

# Check if the archifarm-network exists, if not create it
if ! docker network inspect archifarm-network >/dev/null 2>&1; then
    echo "Creating archifarm-network..."
    docker network create archifarm-network
else
    echo "archifarm-network already exists."
fi

docker compose up -d --build