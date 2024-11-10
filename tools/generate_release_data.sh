#!/bin/bash

# Exit on error for most commands but allow non-critical errors to be skipped
set -e
set -o pipefail  # Capture errors from pipes

# =============================
# Create release_temp directory
# =============================
cd ../
mkdir -p release_temp/

# =============================
# Copy release assets
# =============================
echo "Copying release assets..."

cp docs/assets/logo.png release_temp/logo.png
echo "Copied logo.png"

cp docs/assets/logo.png release_temp/spotify-electron.desktop
echo "Copied spotify-electron.desktop"

# =============================
# Backend OPENAPI generation and Frontend OPENAPI client update
# =============================
echo "Starting Backend OPENAPI generation and Frontend OpenAPI client update..."

cd tools/
./update_openapi.sh

echo "Virtual environment deactivated"

# =============================
# FRONTEND app client
# =============================
echo "Starting Frontend app client update..."

# Navigate to the Electron directory
cd ../Electron/

# Install dependencies, build, and generate OpenAPI client
npm install
echo "npm install completed"

npm run build
echo "Frontend build completed"

# =============================
# Package the app for Linux and Windows
# =============================
npm run package:linux:appimage
mv release/build/SpotifyElectron.AppImage ../release_temp/
echo "Linux AppImage packaged and moved"

npm run package:win
mv release/build/SpotifyElectron.exe  ../release_temp/
echo "Windows executable packaged and moved"

# =============================
# Finish
# =============================
echo "Release process completed successfully."
exit 0
