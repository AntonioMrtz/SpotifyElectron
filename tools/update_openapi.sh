#!/bin/bash
cd ../


cd Backend/

# Activate the virtual environment
source venv/bin/activate
echo "Virtual environment activated"

# Check if mongomock is installed
if pip show mongomock > /dev/null 2>&1; then
    echo "mongomock is installed"
else
    echo "mongomock is not installed"
    exit 1
fi

# Set the environment variable and execute the Python command
echo "Generating OpenAPI schema with timeout..."
timeout 15s env ENV_VALUE="TEST" python -m app.tools.generate_openapi || {
    echo "Error: Python generate_openapi script timed out";
    exit 1
}

echo "OpenAPI schema generation completed"

# Deactivate the virtual environment
deactivate
echo "Virtual environment deactivated"

# Navigate to the Electron directory and run OpenAPI client generation
cd ../Electron/

npm install
npm build
# Generate the OpenAPI client
echo "Generating OpenAPI client..."
npm run generate-openapi-client || { echo "Error: OpenAPI client generation failed"; exit 1; }
echo "OpenAPI client generation completed"
