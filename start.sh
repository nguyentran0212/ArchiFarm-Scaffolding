#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if gum is installed and working
gum_is_working() {
    local gum_path="$1"
    "$gum_path" --version >/dev/null 2>&1
}

# Check if we're on macOS with arm64 architecture
if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
    echo "Detected macOS with arm64 architecture"

    # Set the path to the local gum binary
    GUM="$(pwd)/bin/gum"

    # Check if gum is already installed and working
    if [ -x "$GUM" ] && gum_is_working "$GUM"; then
        echo "gum is already installed and working. Skipping download."
    else
        # Check if curl is available
        if ! command_exists curl; then
            echo "Error: curl is not installed. Please install curl and try again."
            exit 1
        fi

        # Download and extract gum binary
        GUM_VERSION="0.14.5"
        GUM_URL="https://github.com/charmbracelet/gum/releases/download/v${GUM_VERSION}/gum_${GUM_VERSION}_Darwin_arm64.tar.gz"

        echo "Downloading gum binary..."
        curl -L "$GUM_URL" -o gum.tar.gz

        if [ $? -ne 0 ]; then
            echo "Error: Failed to download gum binary."
            exit 1
        fi

        echo "Extracting gum binary..."

        mkdir -p .tmp

        tar -xzf gum.tar.gz -C .tmp --strip-components 1
        if [ $? -ne 0 ]; then
            echo "Error: Failed to extract gum binary."
            exit 1
        fi

        # Create bin directory if it doesn't exist
        mkdir -p "$(pwd)/bin"

        # Move gum binary to bin directory
        mv .tmp/gum "$GUM"

        # Clean up
        rm gum.tar.gz
        rm -r .tmp

        echo "gum binary has been downloaded and placed in $GUM"
    fi

    # Update GUM variable
    export GUM
else
    # Use the existing GUM variable if not on macOS arm64
    export GUM="${GUM:-gum}"
fi

# Check if gum is available and working
if ! gum_is_working "$GUM"; then
    echo "Error: gum is not found or not working. Please ensure it's installed correctly."
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