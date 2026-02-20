#!/bin/bash
# Script to create a Python virtual environment in the current directory

set -e

VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists in $VENV_DIR."
else
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created in $VENV_DIR."
fi

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    echo "Dependencies from requirements.txt installed."
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

echo "To activate, run: source $VENV_DIR/bin/activate"