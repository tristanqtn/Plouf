# Description: Health check API routes for the FastAPI application.

import time
from fastapi import APIRouter # type: ignore

start_time = time.time()

api_health_router = APIRouter()


@api_health_router.get(
    "/status",
    summary="API Health Status",
    response_description="Health status of the API server.",
)
async def api_health():
    """
    Retrieve the health status of the API server.

    This endpoint checks the API status and verifies if the server is running properly.

    Returns:
    - `status: ok` if the server is healthy.
    - `status: error` otherwise.
    """
    return {"status": "ok", "message": "API server is healthy."}


@api_health_router.get(
    "/uptime",
    summary="API Uptime",
    response_description="API server uptime in seconds.",
)
async def api_uptime():
    """
    Retrieve the uptime of the API server.

    This endpoint returns how long the API server has been running since its last restart.

    Returns:
    - `uptime_seconds`: Time in seconds the server has been running.
    """
    try:
        return {"status": "ok", "uptime_seconds": time.time() - start_time}
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch uptime: {str(e)}"}
