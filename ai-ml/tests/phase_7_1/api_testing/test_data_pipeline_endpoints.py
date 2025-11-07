"""API tests for data pipeline endpoints"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
from services.api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_data_upload_endpoint_structure():
    """Test that the data upload endpoint exists."""
    # Test with invalid data to check if endpoint exists
    response = client.post("/api/v1/data/upload", data={})
    # Should return 422 for validation error or 401 for auth error, but not 404
    assert response.status_code != 404

def test_batch_process_endpoint_structure():
    """Test that the batch process endpoint exists."""
    # Test with invalid data to check if endpoint exists
    response = client.post("/api/v1/data/batch-process", json={})
    # Should return 422 for validation error or 401 for auth error, but not 404
    assert response.status_code != 404

def test_job_status_endpoint_structure():
    """Test that the job status endpoint exists."""
    # Test with a sample job ID
    response = client.get("/api/v1/data/jobs/test-job-id")
    # Should return 422 for validation error or 401 for auth error, but not 404
    assert response.status_code != 404

def test_results_endpoint_structure():
    """Test that the results endpoint exists."""
    # Test with a sample result ID
    response = client.get("/api/v1/data/results/test-result-id")
    # Should return 422 for validation error or 401 for auth error, but not 404
    assert response.status_code != 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])