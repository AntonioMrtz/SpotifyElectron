#!/bin/bash
# Install all dependencies stored in the root directory in an existing venv enviroment.
# Virtual enviroment folder must be named `venv`

# Exit immediately if a command exits with a non-zero status.
set -e

# Find all files that contain "requirements" in their name and end with ".txt"
requirements_files=$(find . -type f -name '*requirements*.txt')

PYTHON_COMMAND="python"

if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
    python3 --version
    PYTHON_COMMAND="python3"
else
    if command -v python &>/dev/null; then
        echo "Python 3 is not installed, falling back to Python."
        python --version
    else
        echo "Neither Python 3 nor Python are installed."
        exit 1
    fi
fi

echo "Using $PYTHON_COMMAND"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    # Unix-like systems
    source venv/bin/activate
else
    echo "Failed to activate virtual environment. Please create a virtual environment named 'venv'."
    exit 1
fi


pip install --upgrade pip

# Install dependencies from each requirements file found
for requirement in $requirements_files; do
    echo "Installing from $requirement"
    # Install requirements inside virtual environment
    $PYTHON_COMMAND -m pip install -r "$requirement"
done

# Deactivate virtual environment
deactivate

echo "All dependencies installed and virtual environment deactivated."
