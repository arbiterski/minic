"""
Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_ask_endpoint():
    """Test ask endpoint."""
    request_data = {
        "question": "What is the average age of patients?",
        "dataset_id": "alzheimers_cohort_v1",
        "outputs": ["plot", "table"],
        "privacy_level": "k_anonymous"
    }
    
    response = client.post("/api/v1/ask", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"

def test_get_job_result():
    """Test get job result endpoint."""
    # First create a job
    request_data = {
        "question": "Test question",
        "outputs": ["table"],
        "privacy_level": "public"
    }
    
    create_response = client.post("/api/v1/ask", json=request_data)
    job_id = create_response.json()["job_id"]
    
    # Then get the result
    response = client.get(f"/api/v1/result/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
