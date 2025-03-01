# Description: Stats router for handling stats related requests.

from fastapi import APIRouter  # type: ignore
from app.Mongo import read_all_pools

stats_router = APIRouter()


@stats_router.get(
    "/total_pools",
    summary="Retrieve the total number of pools.",
    response_description="Total number of pools managed.",
)
async def get_number_pools():
    """
    Retrieve the total number of pools in the database.

    Returns:
    - `total_pools`: Total number of pools in the database.
    """
    try:
        pools = read_all_pools()
        return {"status": "ok", "total_pools": len(pools)}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve stats: {str(e)}"}


@stats_router.get(
    "/total_logs",
    summary="Retrieve the total number of logs.",
    response_description="Total number of logs stored.",
)
async def get_number_logs():
    """
    Retrieve the amount of logs stored in the database.

    Returns:
    - `total_logs`: Total number of logs stored in the database.
    """
    try:
        pools = read_all_pools()

        total_logs = 0

        for pool in pools:
            total_logs += len(pool.logbook)
        return {"status": "ok", "total_logs": total_logs}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve stats: {str(e)}"}
