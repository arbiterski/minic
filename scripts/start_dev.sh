#!/bin/bash

# Start development environment for Alzheimer's Disease Analysis Database

echo "Starting development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build sandbox image if it doesn't exist
if ! docker image inspect dementia-sandbox:latest > /dev/null 2>&1; then
    echo "Building sandbox image..."
    ./scripts/build_sandbox.sh
fi

# Start services
echo "Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check service status
echo "Checking service status..."
docker-compose ps

# Test API
echo "Testing API..."
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health

echo ""
echo "✅ Development environment started!"
echo "🌐 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "🔍 Health: http://localhost:8000/health"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
