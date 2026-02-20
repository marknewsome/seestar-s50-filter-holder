#!/bin/bash
# Script to deactivate the Python virtual environment

# Check if the script is being sourced
(return 0 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "Please run: source deactivate_venv.sh"
    exit 1
fi

VENV_DIR="venv"

if [ -n "$VIRTUAL_ENV" ] && [[ "$VIRTUAL_ENV" == *"$VENV_DIR"* ]]; then
    echo "Deactivating virtual environment in $VENV_DIR..."
    deactivate
else
    echo "No active virtual environment in $VENV_DIR to deactivate."
    return 1
fi
