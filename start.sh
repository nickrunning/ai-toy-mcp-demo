#!/bin/bash

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Virtual environment path
VENV_DIR=".venv"

echo "--- Starting MCP Demo ---"

# 1. Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating it..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    INSTALL_REQS=true
fi

# 2. Activate virtual environment
source "$VENV_DIR/bin/activate"

# 3. Install requirements if env was just created or requirements.txt is newer than venv
if [ "$INSTALL_REQS" = true ] || [ "requirements.txt" -nt "$VENV_DIR" ]; then
    echo "Installing/Updating dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        exit 1
    fi
    # Create a marker or use venv folder's timestamp
    touch "$VENV_DIR"
fi

# 4. Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "WARNING: OPENAI_API_KEY is not set."
    echo "Please set it before running, e.g.:"
    echo "  export OPENAI_API_KEY='your_key_here'"
    echo ""
    # Optional: read from user if missing
    read -p "Enter OPENAI_API_KEY (or press Enter to skip if already in environment): " USER_KEY
    if [ -n "$USER_KEY" ]; then
        export OPENAI_API_KEY="$USER_KEY"
    else
        echo "Exiting because OPENAI_API_KEY is required."
        exit 1
    fi
fi

# 5. Run the client
echo "Starting Client..."
python client.py
