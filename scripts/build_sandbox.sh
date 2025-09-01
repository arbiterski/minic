#!/bin/bash

# Build sandbox Docker image for Alzheimer's Disease Analysis Database

echo "Building sandbox Docker image..."

# Navigate to docker directory
cd docker

# Build the sandbox image
docker build -f sandbox.Dockerfile -t dementia-sandbox:latest .

if [ $? -eq 0 ]; then
    echo "✅ Sandbox image built successfully!"
    echo "Image: dementia-sandbox:latest"
else
    echo "❌ Failed to build sandbox image"
    exit 1
fi

# Return to root directory
cd ..

echo "Sandbox build complete!"
