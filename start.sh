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

# Verify that docker network is created, if not create it as a bridge network
if ! docker network ls | grep -q archifarm-network; then
    $GUM style --foreground 214 "Docker network is not created. Creating the network..."
    docker network create archifarm-network
fi

current_dir=$(pwd)

# Function to start a docker compose stack
start_stack() {
    local component=$1
    local directory=$2

    $GUM style "Starting the $component..."
    cd "$directory"
    $GUM spin --spinner dot --title "Starting $component" -- docker compose up -d
    cd "$current_dir"
    $GUM style --foreground 46 "$component started successfully!"
}

# Main installation process
$GUM style --foreground 99 'ArchiFarm Installation'

# Workflow engine
start_stack "workflow engine" "./archifarm-core/workflow-engine"

# Telemetry collector
start_stack "telemetry collector" "./archifarm-core/telemetry-collector"

# Testbed status dashboard
start_stack "testbed status dashboard" "./archifarm-core/testbed-status-dashboard"

# Remaining components
$GUM style "Starting the remaining components..."
$GUM spin --spinner dot --title "Starting remaining components" -- docker compose up -d
$GUM style --foreground 46 "Remaining components started successfully!"

$GUM style --foreground 82 --bold "Installation completed successfully!"

# Display the table of Docker containers and port mappings
$GUM style --foreground 99 'Docker Containers and Port Mappings'
docker ps --format "table {{.Names}}\t{{.Ports}}" |
    tail -n +2 |  # Remove the header row
    sed 's/0.0.0.0://g; s/:::/ /g; s/, / /g'

$GUM style --foreground 99 'To Generate Experiment and run it, go to archifarm-core/experiment-management-cli'