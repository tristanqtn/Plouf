from fastapi.testclient import TestClient # type: ignore
from app.routes.health.mongo import mongo_health_router 
from fastapi import FastAPI # type: ignore

# Create a test app and include the router
app = FastAPI()
app.include_router(mongo_health_router)

client = TestClient(app)


def test_mongo_health_status():
    """
    Test the /status endpoint for MongoDB health.
    """
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["ok", "error"]


def test_mongo_uptime():
    """
    Test the /uptime endpoint to validate MongoDB uptime.
    """
    response = client.get("/uptime")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_mongo_info():
    """
    Test the /info endpoint for MongoDB server information.
    """
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data
    assert "storage_engines" in data


def test_mongo_storage_stats():
    """
    Test the /storage endpoint for MongoDB storage stats.
    """
    response = client.get("/storage")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "storage_engine" in data
    assert "memory" in data


def test_mongo_connection_stats():
    """
    Test the /connections endpoint for MongoDB connection stats.
    """
    response = client.get("/connections")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "connections" in data

def test_mongo_full_health():
    """
    Test the /full_health endpoint for a comprehensive MongoDB health report.
    """
    response = client.get("/full_health")
    assert response.status_code == 200
    data = response.json()
    assert "overall_status" in data
    assert data["overall_status"] == "ok"
    assert "health" in data
    assert "uptime" in data
    assert "storage_stats" in data
    assert "connection_stats" in data