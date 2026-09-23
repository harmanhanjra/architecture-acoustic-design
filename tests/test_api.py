import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_record_stress_event():
    response = client.post("/api/v1/stress", json={
        "timestamp": "2026-09-23T00:30:00Z",
        "gsr": 0.5,
        "hrv": 60.0,
        "temperature": 37.0,
        "anxiety_score": 0.3
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_stress_events():
    response = client.get("/api/v1/stress")
    assert response.status_code == 200
    assert "events" in response.json()

def test_record_acoustic_metrics():
    response = client.post("/api/v1/acoustic", json={
        "rt60": 2.1,
        "sti": 0.6,
        "frequency_response": {"1000Hz": 0.8},
        "spatial_metrics": {"azimuth_error": 2.5},
        "timestamp": "2026-09-23T00:30:00Z"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_acoustic_metrics():
    response = client.get("/api/v1/acoustic")
    assert response.status_code == 200
    assert "metrics" in response.json()
