import pytest  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from app.routes.pool.router import pool_router  # Import your FastAPI app

# Create a test client
client = TestClient(pool_router)

# Mock data
mock_pool_data = {
    "owner_name": "John Doe",
    "length": 10.0,
    "width": 5.0,
    "depth": 2.0,
    "type": "In-ground",
    "notes": "Needs a new pump filter soon",
    "water_volume": 100.0,
    "next_maintenance": "2025-01-10",
    "logbook": [],
}

mock_log_data = {
    "date": "2024-12-25",
    "pH_level": 7.4,
    "chlorine_level": 2.0,
    "notes": "Routine check",
}


# Test creating a pool (set up)
@pytest.fixture
def new_pool():
    # This fixture will create a pool and return its ID
    response = client.post("/", json=mock_pool_data)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    return response.json()["id"]


# Test 1: Add a maintenance log to a pool
def test_log_maintenance(new_pool):
    pool_id = new_pool
    response = client.post(f"/{pool_id}/log", json=mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance logged successfully.",
    }


# Test 2: Retrieve all maintenance logs for a pool
def test_get_all_pool_logs(new_pool):
    pool_id = new_pool
    # First, add a log entry
    client.post(f"/{pool_id}/log", json=mock_log_data)

    # Retrieve all logs
    response = client.get(f"/{pool_id}/log/all")

    assert response.status_code == 200
    logs = response.json().get("logs", [])
    assert len(logs) == 1
    assert logs[0]["date"] == mock_log_data["date"]
    assert logs[0]["pH_level"] == mock_log_data["pH_level"]
    assert logs[0]["chlorine_level"] == mock_log_data["chlorine_level"]
    assert logs[0]["notes"] == mock_log_data["notes"]


# Test 3: Retrieve a specific maintenance log by ID
def test_get_pool_log_by_id(new_pool):
    pool_id = new_pool
    # First, add a log entry
    client.post(f"/{pool_id}/log", json=mock_log_data)
    temp = client.get(f"/{pool_id}/log/all")
    log_id = temp.json()["logs"][0]["id"]
    # Retrieve the specific log entry
    response = client.get(f"/{pool_id}/log/{log_id}")

    assert response.status_code == 200
    print(response.json())
    log = response.json().get("log", {})
    assert log["date"] == mock_log_data["date"]
    assert log["pH_level"] == mock_log_data["pH_level"]
    assert log["chlorine_level"] == mock_log_data["chlorine_level"]
    assert log["notes"] == mock_log_data["notes"]


# Test 4: Try to retrieve a log that doesn't exist
def test_get_non_existent_log(new_pool):
    pool_id = new_pool
    invalid_log_id = "non-existent-log-id"

    response = client.get(f"/{pool_id}/log/{invalid_log_id}")

    assert response.status_code == 200
    assert response.json() == {"status": "error", "message": "Log not found."}


# Test 5: Try to log maintenance for a non-existent pool
def test_log_maintenance_for_non_existent_pool():
    invalid_pool_id = "non-existent-pool-id"

    response = client.post(f"/{invalid_pool_id}/log", json=mock_log_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json().get("status") == "error"


def test_delete_all_pool_logs(new_pool):
    pool_id = new_pool
    response = client.post(f"/{pool_id}/log", json=mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance logged successfully.",
    }

    response = client.post(f"/{pool_id}/log", json=mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance logged successfully.",
    }

    response = client.delete(f"/{pool_id}/log/all")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "All logs deleted successfully.",
    }


def test_delete_one_pool_log(new_pool):
    pool_id = new_pool
    response = client.post(f"/{pool_id}/log", json=mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance logged successfully.",
    }

    temp = client.get(f"/{pool_id}/log/all")
    log_id = temp.json()["logs"][0]["id"]
    # Retrieve the specific log entry
    response = client.delete(f"/{pool_id}/log/{log_id}")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Log deleted successfully."}


def test_update_one_pool_log(new_pool):
    pool_id = new_pool
    response = client.post(f"/{pool_id}/log", json=mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance logged successfully.",
    }

    temp = client.get(f"/{pool_id}/log/all")
    log_id = temp.json()["logs"][0]["id"]
    # Retrieve the specific log entry
    updated_mock_log_data = {
        "date": "2024-12-25",
        "pH_level": 7.4,
        "chlorine_level": 2.0,
        "notes": "Update Performed",
    }
    response = client.put(f"/{pool_id}/log/{log_id}", json=updated_mock_log_data)

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Maintenance updated successfully.",
    }

    response = client.get(f"/{pool_id}/log/{log_id}")

    assert response.status_code == 200
    logs = response.json().get("logbook", {})

    for log in logs:
        if log["id"] == log_id:
            assert log["date"] == updated_mock_log_data["date"]
            assert log["pH_level"] == updated_mock_log_data["pH_level"]
            assert log["chlorine_level"] == updated_mock_log_data["chlorine_level"]
            assert log["notes"] == updated_mock_log_data["notes"]


# flush preprod db after running tests
def test_flush_db():
    response = client.delete("/all")
    assert response.status_code == 200
