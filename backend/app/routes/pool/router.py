# Description: Pool routes for supporting CRUD operations.
import uuid  # type: ignore

from fastapi import APIRouter  # type: ignore
from app.Pools import Pool, PoolLog
from app.Mongo import (
    create_pool,
    read_all_pools,
    retrieve_pool,
    update_pool,
    delete_pool,
    delete_all_pools,
    retrieve_pool_log_by_id,
    delete_pool_logs,
    delete_pool_log_by_id,
)

pool_router = APIRouter()


@pool_router.post(
    "/",
    summary="Register a new pool",
    response_description="Pool creation status.",
)
async def create_new_pool(pool_data: dict):
    """
    Register a new pool in the database.

    Args:
    - `pool_data`: Pool data to be registered.

    Returns:
    - `status`: Status of the operation.
    - `message`: Additional information about the operation.
    """
    try:
        pool = Pool(**pool_data)
        pool_id = create_pool(pool)
        return {
            "status": "ok",
            "id": pool_id,
            "message": f"Pool created with ID: {pool_id}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to create pool: {str(e)}"}


@pool_router.get(
    "/all",
    summary="Retrieve all pools",
    response_description="Table of pools.",
)
async def get_all_pools():
    """
    Retrieve all pools from the database.

    Returns:
    - `pools`: List of pools in the database.
    """
    try:
        pools = read_all_pools()
        return {"status": "ok", "pools": pools}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve pools: {str(e)}"}


@pool_router.delete(
    "/all",
    summary="Delete all pools",
    response_description="Pool deletion status.",
)
async def delete_all_pools_route():
    """
    Delete all pools from the database.

    Returns:
    - `status`: Status of the operation.
    - `message`: Additional information about the operation.
    """
    try:
        deleted_count = delete_all_pools()
        return {
            "status": "ok",
            "message": f"Deleted {deleted_count} pools successfully.",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete pools: {str(e)}"}


@pool_router.get(
    "/{pool_id}",
    summary="Retrieve a specific pool",
    response_description="Pool data.",
)
async def get_pool_by_id(pool_id: str):
    """
    Retrieve a specific pool from the database.

    Args:
    - `pool_id`: ID of the pool to be retrieved.

    Returns:
    - `pool`: Pool data.
    """
    try:
        pool = retrieve_pool(pool_id)
        return {"status": "ok", "pool": pool}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve pool: {str(e)}"}


@pool_router.put(
    "/{pool_id}",
    summary="Update a specific pool",
    response_description="Pool update status.",
)
async def update_pool_by_id(pool_id: str, pool_data: dict):
    """
    Update a specific pool in the database.

    Args:
    - `pool_id`: ID of the pool to be updated.
    - `pool_data`: Updated pool data.

    Returns:
    - `status`: Status of the operation.
    - `message`: Additional information about the operation.
    """
    try:
        updated = update_pool(pool_id, pool_data)
        if not updated:
            return {"status": "error", "message": "Pool not found."}
        return {"status": "ok", "message": "Pool updated successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to update pool: {str(e)}"}


@pool_router.delete(
    "/{pool_id}",
    summary="Delete a specific pool",
    response_description="Pool deletion status.",
)
async def delete_pool_by_id(pool_id: str):
    """
    Delete a specific pool from the database.

    Args:
    - `pool_id`: ID of the pool to be deleted.

    Returns:
    - `status`: Status of the operation.
    - `message`: Additional information about the operation.
    """
    try:
        deleted = delete_pool(pool_id)
        if not deleted:
            return {"status": "error", "message": "Pool not found."}
        return {"status": "ok", "message": "Pool deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete pool: {str(e)}"}


@pool_router.post(
    "/{pool_id}/log",
    summary="Log maintenance for a pool",
    response_description="Maintenance log status.",
)
async def log_maintenance(pool_id: str, log_data: dict):
    """
    Log maintenance for a specific pool.

    Args:
    - `pool_id`: ID of the pool to log maintenance for.
    - `log_data`: Maintenance log data.

    Returns:
    - `status`: Status of the operation.
    - `message`: Additional information about the operation.
    """
    try:
        pool = retrieve_pool(pool_id)
        if not pool:
            return {"status": "error", "message": "Pool not found."}
        log = PoolLog(**log_data)
        pool.log_maintenance(log)
        updated = update_pool(pool_id, pool.dict())
        if not updated:
            return {"status": "error", "message": "Failed to log maintenance."}
        return {"status": "ok", "message": "Maintenance logged successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to log maintenance: {str(e)}"}


@pool_router.get(
    "/{pool_id}/log/all",
    summary="Retrieve all maintenance logs",
    response_description="Maintenance log data.",
)
async def get_all_pool_logs(pool_id: str):
    """
    Retrieve all maintenance logs for a specific pool.

    Args:
    - `pool_id`: ID of the pool to retrieve logs from.

    Returns:
    - `logs`: List of maintenance log entries.
    """
    try:
        pool = retrieve_pool(pool_id)
        if not pool:
            return {"status": "error", "message": "Pool not found."}
        return {"status": "ok", "logs": pool.logbook}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve logs: {str(e)}"}


@pool_router.delete(
    "/{pool_id}/log/all",
    summary="Delete all maintenance logs for a pool",
    response_description="Deletion status.",
)
async def delete_all_pool_log_(pool_id: str):
    """
    Delete all maintenance log entries for a pool.

    Args:
    - `pool_id`: ID of the pool to retrieve the log from.

    Returns:
    - `status`: Status of the operation.
    """
    try:
        delete_pool_logs(pool_id)
        return {"status": "ok", "message": "All logs deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete logs: {str(e)}"}


@pool_router.get(
    "/{pool_id}/log/{log_id}",
    summary="Retrieve a specific maintenance log",
    response_description="Maintenance log data.",
)
async def get_pool_log_by_id(pool_id: str, log_id: str):
    """
    Retrieve a specific maintenance log entry for a pool.

    Args:
    - `pool_id`: ID of the pool to retrieve the log from.
    - `log_id`: ID of the log entry to be retrieved.

    Returns:
    - `log`: Maintenance log data.
    """
    try:
        log = retrieve_pool_log_by_id(pool_id, log_id)
        if not log:
            return {"status": "error", "message": "Log not found."}
        return {"status": "ok", "log": log}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve log: {str(e)}"}


@pool_router.put(
    "/{pool_id}/log/{log_id}",
    summary="Update a specific maintenance log",
    response_description="Update status.",
)
async def update_pool_log(pool_id: str, log_id: str, log_data: dict):
    """
    Update a specific maintenance log entry for a pool.

    Args:
    - `pool_id`: ID of the pool to retrieve the log from.
    - `log_id`: ID of the log entry to be update.

    Returns:
    - Update success status.
    """
    try:
        pool = retrieve_pool(pool_id)
        if not pool:
            return {"status": "error", "message": "Pool not found."}
        log = PoolLog(**log_data)
        log.id = uuid.UUID(log_id)

        for i, log_entry in enumerate(pool.logbook):
            if str(log_entry.id) == str(log_id):
                pool.logbook[i] = log
                break
        updated = update_pool(pool_id, pool.dict())
        if not updated:
            return {"status": "error", "message": "Failed to update maintenance."}
        return {"status": "ok", "message": "Maintenance updated successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to update maintenance: {str(e)}"}


@pool_router.delete(
    "/{pool_id}/log/{log_id}",
    summary="Delete a specific maintenance log",
    response_description="Deletion status.",
)
async def delete_pool_log_by_id_(pool_id: str, log_id: str):
    """
    Delete a specific maintenance log entry for a pool.

    Args:
    - `pool_id`: ID of the pool to retrieve the log from.
    - `log_id`: ID of the log entry to be deleted.

    Returns:
    - `status`: Status of the operation.
    """
    try:
        deleted = delete_pool_log_by_id(pool_id, log_id)
        if not deleted:
            return {"status": "error", "message": "Log not found."}
        return {"status": "ok", "message": "Log deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete log: {str(e)}"}
