#!/bin/bash
# Script to activate the Python virtual environment

# Check if the script is being sourced
(return 0 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "Please run: source activate_venv.sh"
    exit 1
fi

VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment in $VENV_DIR..."
    source "$VENV_DIR/bin/activate"
else
    echo "Virtual environment not found in $VENV_DIR."
    return 1
fi
