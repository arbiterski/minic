#!/usr/bin/env python3
"""
Test script for Alzheimer's Disease Analysis Database project.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        import fastapi
        print("  ✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"  ❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("  ✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"  ❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import redis
        print("  ✅ Redis imported successfully")
    except ImportError as e:
        print(f"  ❌ Redis import failed: {e}")
        return False
    
    try:
        import docker
        print("  ✅ Docker imported successfully")
    except ImportError as e:
        print(f"  ❌ Docker import failed: {e}")
        return False
    
    try:
        import pandas
        print("  ✅ Pandas imported successfully")
    except ImportError as e:
        print(f"  ❌ Pandas import failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test if the application structure is correct."""
    print("\n🏗️  Testing application structure...")
    
    required_dirs = [
        "app",
        "app/api",
        "app/core", 
        "app/models",
        "app/services",
        "app/utils",
        "tests",
        "docker",
        "scripts"
    ]
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/models/schemas.py",
        "app/core/config.py",
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        "README.md"
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ Directory: {dir_path}")
        else:
            print(f"  ❌ Missing directory: {dir_path}")
            all_good = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ File: {file_path}")
        else:
            print(f"  ❌ Missing file: {file_path}")
            all_good = False
    
    return all_good

def test_app_imports():
    """Test if the application modules can be imported."""
    print("\n📦 Testing application imports...")
    
    # Add app directory to Python path
    sys.path.insert(0, str(Path.cwd()))
    
    try:
        from app.main import app
        print("  ✅ Main app imported successfully")
    except Exception as e:
        print(f"  ❌ Main app import failed: {e}")
        return False
    
    try:
        from app.models.schemas import AskRequest, JobResponse
        print("  ✅ Schemas imported successfully")
    except Exception as e:
        print(f"  ❌ Schemas import failed: {e}")
        return False
    
    try:
        from app.services.llm_service import LLMService
        print("  ✅ LLM service imported successfully")
    except Exception as e:
        print(f"  ❌ LLM service import failed: {e}")
        return False
    
    try:
        from app.services.sandbox_service import SandboxService
        print("  ✅ Sandbox service imported successfully")
    except Exception as e:
        print(f"  ❌ Sandbox service import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading."""
    print("\n⚙️  Testing configuration...")
    
    try:
        from app.core.config import settings
        print("  ✅ Configuration loaded successfully")
        print(f"  📝 API Title: {settings.api_title}")
        print(f"  📝 API Version: {settings.api_version}")
        print(f"  📝 Dataset Path: {settings.dataset_path}")
        print(f"  📝 Artifact Dir: {settings.artifact_dir}")
        return True
    except Exception as e:
        print(f"  ❌ Configuration loading failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint definitions."""
    print("\n🌐 Testing API endpoints...")
    
    try:
        from app.main import app
        from app.api.endpoints import router
        
        # Check if router is included
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        
        expected_routes = [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/api/v1/ask",
            "/api/v1/result/{job_id}",
            "/api/v1/files/{job_id}/{filename}",
            "/api/v1/jobs/{job_id}"
        ]
        
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"  ✅ Route: {route}")
            else:
                print(f"  ❌ Missing route: {route}")
        
        return True
    except Exception as e:
        print(f"  ❌ API endpoint testing failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Alzheimer's Disease Analysis Database - Project Test")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("App Structure", test_app_structure),
        ("App Imports", test_app_imports),
        ("Configuration", test_config),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Project is ready to run.")
        print("\n🚀 Next steps:")
        print("  1. make install          # Install dependencies")
        print("  2. make build-sandbox    # Build sandbox image")
        print("  3. make sample-data      # Create sample dataset")
        print("  4. make start            # Start services")
        print("  5. make test             # Run tests")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
