import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from app.routes.stats.router import stats_router # type: ignore
from app.routes.pool.router import pool_router

from fastapi import FastAPI  # type: ignore

# Create a test app and include the router
app = FastAPI()
app.include_router(stats_router, prefix="/stats")
app.include_router(pool_router, prefix="/pool")

client = TestClient(app)

# Sample pool data (use the same data as the body in the API requests)
mock_pool_data = {
    "owner_name": "John Doe",
    "length": 10.0,
    "width": 5.0,
    "depth": 2.0,
    "type": "In-ground",
    "notes": "Needs a new pump filter soon",
    "water_volume": 100.0,
    "next_maintenance": "2025-01-10",
    "logbook": [
        {
            "date": "2024-12-25",
            "pH_level": 7.4,
            "chlorine_level": 2.0,
            "notes": "Routine check",
        },
        {
            "date": "2024-12-20",
            "pH_level": 7.3,
            "chlorine_level": 2.5,
            "notes": "Added chlorine",
        },
    ],
}

def flush_db():
    response = client.delete("/pool/all")
    assert response.status_code == 200

def create_pool():
    response = client.post("/pool", json=mock_pool_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Pool created with ID" in data["message"]

# Test 1: Test the /total_pools endpoint
def test_total_pools():
    """
    Test the /status endpoint to ensure it returns the correct number of pools.
    """

    # initialize
    flush_db()

    create_pool()
    create_pool()

    response = client.get("/stats/total_pools")
    assert response.status_code == 200
    data = response.json()
    assert data["total_pools"] == 2

    flush_db()

# Test 2: Test the /total_logs endpoint
def test_total_logs():
    """
    Test the /total_logs endpoint to ensure it returns the correct number of logs.
    """

    # initialize
    flush_db()

    create_pool()
    create_pool()

    response = client.get("/stats/total_logs")
    assert response.status_code == 200
    data = response.json()
    assert data["total_logs"] == 4

    flush_db()


