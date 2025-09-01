#!/bin/bash

# Check project status for Alzheimer's Disease Analysis Database

echo "🔍 Alzheimer's Disease Analysis Database - Status Check"
echo "=================================================="

# Check Docker
echo "🐳 Docker Status:"
if docker info > /dev/null 2>&1; then
    echo "  ✅ Docker is running"
    
    # Check sandbox image
    if docker image inspect dementia-sandbox:latest > /dev/null 2>&1; then
        echo "  ✅ Sandbox image exists"
    else
        echo "  ❌ Sandbox image missing (run: make build-sandbox)"
    fi
else
    echo "  ❌ Docker is not running"
    exit 1
fi

# Check Python environment
echo ""
echo "🐍 Python Environment:"
if command -v python3 > /dev/null 2>&1; then
    python_version=$(python3 --version)
    echo "  ✅ Python: $python_version"
    
    # Check if requirements are installed
    if python3 -c "import fastapi, redis, docker" 2>/dev/null; then
        echo "  ✅ Dependencies installed"
    else
        echo "  ❌ Dependencies missing (run: make install)"
    fi
else
    echo "  ❌ Python3 not found"
fi

# Check data directory
echo ""
echo "📁 Data Directory:"
data_dir="data/alzheimers_cohort_v1"
if [ -d "$data_dir" ]; then
    echo "  ✅ Data directory exists: $data_dir"
    
    # Check for data files
    if [ -f "$data_dir/patients.parquet" ]; then
        echo "  ✅ Parquet dataset found"
    elif [ -f "$data_dir/patients.xlsx" ]; then
        echo "  ✅ Excel dataset found"
    else
        echo "  ❌ No dataset files found (run: make sample-data)"
    fi
else
    echo "  ❌ Data directory missing: $data_dir"
fi

# Check artifacts directory
echo ""
echo "📦 Artifacts Directory:"
artifacts_dir="artifacts"
if [ -d "$artifacts_dir" ]; then
    echo "  ✅ Artifacts directory exists: $artifacts_dir"
else
    echo "  ❌ Artifacts directory missing"
fi

# Check Docker Compose
echo ""
echo "🐙 Docker Compose:"
if command -v docker-compose > /dev/null 2>&1; then
    echo "  ✅ Docker Compose available"
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        echo "  ✅ Services are running"
        echo ""
        echo "📊 Service Status:"
        docker-compose ps
    else
        echo "  ❌ No services running (run: make start)"
    fi
else
    echo "  ❌ Docker Compose not found"
fi

# Check API
echo ""
echo "🌐 API Status:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ API is responding"
    
    # Get API info
    api_info=$(curl -s http://localhost:8000/ | jq -r '.message // "Unknown"' 2>/dev/null || echo "Unknown")
    echo "  📝 API: $api_info"
    
    # Check docs
    if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
        echo "  📚 API Documentation: http://localhost:8000/docs"
    fi
else
    echo "  ❌ API is not responding"
fi

echo ""
echo "=================================================="
echo "🎯 Next Steps:"
echo "  • To start services: make start"
echo "  • To create sample data: make sample-data"
echo "  • To run tests: make test"
echo "  • To view logs: make logs"
echo "  • To stop services: make stop"
echo "  • For help: make help"
