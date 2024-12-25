import pytest
from fastapi.testclient import TestClient
from app.routes.health.api import api_health_router  # Adjust the import based on your app structure
from fastapi import FastAPI

# Create a test app and include the router
app = FastAPI()
app.include_router(api_health_router)

client = TestClient(app)

def test_api_health():
    """
    Test the /status endpoint to ensure it returns the correct health status.
    """
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "API server is healthy."

def test_api_uptime():
    """
    Test the /uptime endpoint to ensure it returns the correct uptime value.
    """
    response = client.get("/uptime")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data

    # Ensure uptime is a positive float value
    uptime = data["uptime_seconds"]
    assert isinstance(uptime, float)
    assert uptime >= 0

    # Optional: Check that uptime increases with time
    response_later = client.get("/uptime")
    uptime_later = response_later.json()["uptime_seconds"]
    assert uptime_later > uptime

@pytest.mark.parametrize(
    "endpoint,expected_status,expected_key",
    [
        ("/status", "ok", "message"),
        ("/uptime", "ok", "uptime_seconds"),
    ],
)
def test_endpoints_status(endpoint, expected_status, expected_key):
    """
    Parametrized test for multiple endpoints to validate status and response keys.
    """
    response = client.get(endpoint)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == expected_status
    assert expected_key in data
