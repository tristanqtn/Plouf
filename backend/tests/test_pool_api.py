import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from app.routes.pool.router import pool_router

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

client = TestClient(pool_router)


@pytest.fixture
def new_pool():
    # This fixture will create a pool and return its ID
    response = client.post("/", json=mock_pool_data)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    return response.json()["id"]


def test_create_new_pool():
    response = client.post("/", json=mock_pool_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Pool created with ID" in data["message"]


def test_get_all_pools():
    response = client.get("/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["pools"], list)


def test_get_pool_by_id(new_pool):
    response = client.get(f"/{new_pool}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["pool"]["owner_name"] == mock_pool_data["owner_name"]


def test_update_pool_by_id(new_pool):
    updated_data = mock_pool_data.copy()
    updated_data["notes"] = "Updated pump filter"
    response = client.put(f"/{new_pool}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Pool updated successfully."


def test_delete_pool_by_id(new_pool):
    response = client.delete(f"/{new_pool}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Pool deleted successfully."


def test_delete_all_pools():
    # This fixture will create a pool and return its ID
    response = client.delete("/all")  # Flush pools
    assert response.status_code == 200
    response = client.post("/", json=mock_pool_data)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    response = client.delete("/all")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Deleted 1 pools successfully."
