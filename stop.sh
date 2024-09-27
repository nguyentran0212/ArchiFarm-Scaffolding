#!/bin/bash

# Set the path to the local gum binary
GUM="$(pwd)/bin/gum"

# Check if gum is available in the local bin directory
if [ ! -x "$GUM" ]; then
    echo "gum is not found in ./bin/gum. Please ensure it's installed in the correct location."
    exit 1
fi

# Verify that docker is running
if ! docker info > /dev/null 2>&1; then
    $GUM style --foreground 196 "Docker is not running. Please start Docker before running this script."
    exit 1
fi

current_dir=$(pwd)

# Function to stop a docker compose stack
stop_stack() {
    local component=$1
    local directory=$2

    $GUM style "Stopping the $component..."
    cd "$directory"
    $GUM spin --spinner dot --title "Stopping $component" -- docker compose down
    cd "$current_dir"
    $GUM style --foreground 46 "$component stopped successfully!"
}

# Main stopping process
$GUM style --foreground 99 'ArchiFarm Shutdown'

# Stop the main docker-compose stack
$GUM style "Stopping the main components..."
$GUM spin --spinner dot --title "Stopping main components" -- docker compose down

# Stop the testbed status dashboard
stop_stack "testbed status dashboard" "./archifarm-core/testbed-status-dashboard"

# Stop the telemetry collector
stop_stack "telemetry collector" "./archifarm-core/telemetry-collector"

# Stop the workflow engine
stop_stack "workflow engine" "./archifarm-core/workflow-engine"

# Remove the docker network if it exists
if docker network ls | grep -q archifarm-network; then
    $GUM style "Removing the archifarm-network..."
    $GUM spin --spinner dot --title "Removing network" -- docker network rm archifarm-network
fi

$GUM style --foreground 82 --bold "All services have been stopped successfully!"
