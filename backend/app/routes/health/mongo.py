from fastapi import APIRouter # type: ignore
from app.Mongo import (
    get_mongo_health,
    get_mongo_uptime,
    get_mongo_info,
    get_mongo_storage_stats,
    get_mongo_connection_stats,
    get_mongo_full_health,
)

mongo_health_router = APIRouter()


@mongo_health_router.get(
    "/status",
    summary="MongoDB Health Status",
    response_description="Health status of the MongoDB server.",
)
async def mongo_health():
    """
    Retrieve the health status of the MongoDB server.

    This endpoint checks the MongoDB connection and verifies if the server is running properly.

    Returns:
    - `status: ok` if the server is healthy.
    - `status: error` otherwise.
    """
    return get_mongo_health()


@mongo_health_router.get(
    "/uptime",
    summary="MongoDB Uptime",
    response_description="MongoDB server uptime in seconds.",
)
async def mongo_uptime():
    """
    Retrieve the uptime of the MongoDB server.

    This endpoint returns how long the MongoDB server has been running since its last restart.

    Returns:
    - `uptime_seconds`: Time in seconds the server has been running.
    """
    return get_mongo_uptime()


@mongo_health_router.get(
    "/info",
    summary="MongoDB Server Info",
    response_description="Detailed information about the MongoDB server.",
)
async def mongo_info():
    """
    Retrieve detailed information about the MongoDB server.

    This includes:
    - MongoDB version.
    - Build environment details.
    - Supported storage engines.
    - JavaScript engine.

    Returns:
    - Detailed server information in JSON format.
    """
    return get_mongo_info()


@mongo_health_router.get(
    "/storage",
    summary="MongoDB Storage Stats",
    response_description="MongoDB storage and memory utilization stats.",
)
async def mongo_storage_stats():
    """
    Retrieve MongoDB storage and memory utilization statistics.

    This includes:
    - Storage engine type.
    - Memory usage (resident, virtual, and mapped memory in MB).

    Returns:
    - A JSON object with storage engine and memory stats.
    """
    return get_mongo_storage_stats()


@mongo_health_router.get(
    "/connections",
    summary="MongoDB Connection Stats",
    response_description="Current MongoDB connection stats.",
)
async def mongo_connection_stats():
    """
    Retrieve MongoDB connection statistics.

    This includes:
    - Current active connections.
    - Available connections.
    - Total connections created.

    Returns:
    - A JSON object with connection stats.
    """
    return get_mongo_connection_stats()


@mongo_health_router.get(
    "/full_health",
    summary="Comprehensive MongoDB Health Report",
    response_description="A detailed health report of MongoDB.",
)
async def mongo_full_health():
    """
    Retrieve a comprehensive health report of the MongoDB server.

    This combines data from multiple sources, including:
    - Overall health status.
    - Uptime.
    - Storage stats.
    - Connection stats.

    Returns:
    - A JSON object with a detailed health report.
    """
    return get_mongo_full_health()
