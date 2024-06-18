#!/bin/bash
# Creates a virtual enviroment and install all dependencies stored in the root directory


# Find all files that contain "requirements" in their name and end with ".txt"
requirements_files=$(find . -type f -name '*requirements*.txt')

PYTHON_COMMAND="python"

if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
    python3 --version
    PYTHON_COMMAND="${PYTHON_COMMAND}3"
else
    echo "Python 3 is not installed."
    python --version
fi

echo "using $PYTHON_COMMAND"

for requirement in $requirements_files; do
    echo "Installing from $requirement"
    # Create and activate virtual environment
    $PYTHON_COMMAND -m venv venv
    source venv/bin/activate
    # Install requirements inside virtual environment
    $PYTHON_COMMAND -m pip install -r "$requirement"
    # Deactivate virtual environment
done
deactivate
