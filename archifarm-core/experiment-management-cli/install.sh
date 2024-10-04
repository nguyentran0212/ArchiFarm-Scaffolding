#!/bin/bash

# install.sh
# Script to install the CLI using Poetry

# Required Poetry version
REQUIRED_POETRY_VERSION="1.4.2"

# Function to compare version numbers
version_ge() {
  # Returns 0 (true) if $1 >= $2
  [ "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1" ]
}

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -

    # Add Poetry to PATH
    export PATH="$HOME/.local/bin:$PATH"

    # Verify installation
    if ! command -v poetry &> /dev/null; then
        echo "Poetry installation failed. Please install it manually."
        exit 1
    fi
    echo "Poetry installed successfully."
else
    echo "Poetry is already installed."
fi

# Check Poetry version
INSTALLED_POETRY_VERSION=$(poetry --version | awk '{print $2}')
echo "Installed Poetry version: $INSTALLED_POETRY_VERSION"

if version_ge "$INSTALLED_POETRY_VERSION" "$REQUIRED_POETRY_VERSION"; then
    echo "Poetry version meets the requirement."
else
    echo "Poetry version is lower than required ($REQUIRED_POETRY_VERSION). Please update Poetry."
    exit 1
fi

# Install the CLI dependencies
echo "Installing CLI dependencies with Poetry..."
poetry install --no-dev

echo "CLI installed successfully."

echo "Please run 'poetry shell' to activate the virtual environment."
echo "Then run 'experiment-cli' to start the CLI."
echo "Run 'experiment-cli --help' to see the available commands."