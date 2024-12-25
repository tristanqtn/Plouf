# Description: Controller for all MongoDB operations

import os
import json
import uuid
from typing import Dict, Any

from dotenv import load_dotenv
from pymongo import MongoClient  # type: ignore
from typing import List, Optional
from bson.binary import Binary, UuidRepresentation  # type: ignore
from bson.objectid import ObjectId  # type: ignore

from app.Pools import Pool, PoolLog

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

MONGO_ADDRESS = os.getenv("MONGO_ADDRESS")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_ADDRESS}"

if not MONGO_DATABASE or not MONGO_COLLECTION:
    raise ValueError(
        "Environment variables MONGO_DATABASE and MONGO_COLLECTION must be set and non-empty strings."
    )

# MongoDB connection setup
client = MongoClient(mongo_uri, uuidRepresentation="standard")
pools_collection = client[MONGO_DATABASE][MONGO_COLLECTION]

# UTILS


def parse_pool_data(mongo_data: Dict[str, Any]) -> Pool:
    # Convert MongoDB's _id (ObjectId) to UUID
    pool_id = str(mongo_data["_id"])  # Convert ObjectId to UUID
    # Convert logbook entries' ids from UUID string to UUID object
    logbook = []
    for log in mongo_data.get("logbook", []):
        logbook.append(
            PoolLog(
                id=log["id"],
                date=log["date"],
                pH_level=log["pH_level"],
                chlorine_level=log["chlorine_level"],
                notes=log["notes"],
            )
        )
        # Return a Pool object with all the converted fields
    return Pool(
        id=pool_id,
        owner_name=mongo_data["owner_name"],
        length=mongo_data["length"],
        width=mongo_data["width"],
        depth=mongo_data["depth"],
        type=mongo_data["type"],
        notes=mongo_data["notes"],
        water_volume=mongo_data["water_volume"],
        next_maintenance=mongo_data.get("next_maintenance"),
        logbook=logbook,
    )


# Helper function to convert Pool to dictionary
def pool_to_dict(pool: Pool):
    return json.loads(pool.json())


# MONGO OPERATIONS


def create_pool(pool: Pool):
    """
    Inserts a new pool into the database.
    """
    pool_data = pool_to_dict(pool)
    result = pools_collection.insert_one(pool_data)
    return str(result.inserted_id)


def read_all_pools() -> List[Pool]:
    """
    Retrieves all pools from the database.
    """
    results = pools_collection.find()
    return [parse_pool_data(pool) for pool in results]


def retrieve_pool(pool_id: str) -> Optional[Pool]:
    """
    Retrieves a specific pool by ID.
    """
    pool_data = pools_collection.find_one({"_id": ObjectId(pool_id)})
    print(pool_data)
    if pool_data:
        return parse_pool_data(pool_data)
    return None


def update_pool(pool_id: str, updated_data: dict):
    """
    Updates a pool's data by ID.
    """
    result = pools_collection.update_one(
        {"_id": ObjectId(pool_id)}, {"$set": updated_data}
    )
    return result.modified_count > 0


def delete_pool(pool_id: str):
    """
    Deletes a pool by ID.
    """
    result = pools_collection.delete_one({"_id": ObjectId(pool_id)})
    return result.deleted_count > 0


def insert_pool_log(pool_id, log_data):
    # Convert UUID to BSON Binary
    if "id" in log_data and isinstance(log_data["id"], uuid.UUID):
        log_data["id"] = Binary.from_uuid(
            log_data["id"], uuid_representation=UuidRepresentation.STANDARD
        )

    result = pools_collection.update_one(
        {"_id": ObjectId(pool_id)},
        {"$push": {"logbook": log_data}},
    )
    return result.modified_count > 0


def retrieve_pool_logs(pool_id: str) -> List[dict]:
    """
    Retrieves all maintenance logs for a pool.
    """
    pool_data = pools_collection.find_one({"_id": ObjectId(pool_id)})
    if pool_data:
        return pool_data.get("logbook", [])
    return []


def delete_pool_logs(pool_id: str):
    """
    Deletes all maintenance logs for a pool.
    """
    result = pools_collection.update_one(
        {"_id": ObjectId(pool_id)}, {"$set": {"logbook": []}}
    )
    return result.modified_count > 0


def delete_all_pools():
    """
    Deletes all pools from the database.
    """
    result = pools_collection.delete_many({})
    return result.deleted_count


def retrieve_pool_log_by_id(pool_id: str, log_id: str) -> Optional[dict]:
    """
    Retrieves a specific maintenance log entry by ID.
    """
    pool_data = pools_collection.find_one({"_id": ObjectId(pool_id)})
    if pool_data:
        for log in pool_data.get("logbook", []):
            if str(log.get("id")) == str(log_id):
                return log
    return None


def update_pool_log_by_id(pool_id: str, log_id: str, updated_log: dict) -> bool:
    """
    Updates a specific maintenance log entry by ID.
    """
    result = pools_collection.update_one(
        {"_id": ObjectId(pool_id), "logbook.id": log_id},
        {"$set": {"logbook.$": updated_log}},
    )
    return result.modified_count > 0


def delete_pool_log_by_id(pool_id: str, log_id: str) -> bool:
    """
    Deletes a specific maintenance log entry by ID.
    """
    result = pools_collection.update_one(
        {"_id": ObjectId(pool_id)}, {"$pull": {"logbook": {"id": log_id}}}
    )
    return result.modified_count > 0


# MONGO HEALTH CHECKS


def get_mongo_info():
    """
    Retrieve MongoDB server version and build info.
    """
    try:
        info = client.server_info()
        return {
            "status": "ok",
            "version": info.get("version"),
            "build_environment": info.get("buildEnvironment", {}),
            "storage_engines": info.get("storageEngines", []),
            "javascript_engine": info.get("javascriptEngine"),
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch server info: {str(e)}"}


def get_mongo_uptime():
    """
    Get MongoDB server uptime in seconds.
    """
    try:
        server_status = client.admin.command("serverStatus")
        uptime_seconds = server_status.get("uptime", 0)
        return {"status": "ok", "uptime_seconds": uptime_seconds}
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch uptime: {str(e)}"}


def get_mongo_health():
    """
    Check if the MongoDB connection is healthy.
    """
    try:
        info = client.server_info()
        if info.get("ok") == 1:
            return {"status": "ok", "message": "MongoDB server is healthy."}
        else:
            return {
                "status": "error",
                "message": "MongoDB server returned a non-OK status.",
            }
    except Exception as e:
        return {"status": "error", "message": f"Error connecting to MongoDB: {str(e)}"}


def get_mongo_storage_stats():
    """
    Retrieve MongoDB storage statistics.
    """
    try:
        server_status = client.admin.command("serverStatus")
        storage_engine = server_status.get("storageEngine", {}).get("name", "unknown")
        memory_info = server_status.get("mem", {})
        return {
            "status": "ok",
            "storage_engine": storage_engine,
            "memory": {
                "resident_MB": memory_info.get("resident"),
                "virtual_MB": memory_info.get("virtual"),
                "mapped_MB": memory_info.get("mapped"),
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch storage stats: {str(e)}",
        }


def get_mongo_connection_stats():
    """
    Retrieve MongoDB connection statistics.
    """
    try:
        server_status = client.admin.command("serverStatus")
        connections = server_status.get("connections", {})
        return {
            "status": "ok",
            "connections": {
                "current": connections.get("current"),
                "available": connections.get("available"),
                "total_created": connections.get("totalCreated"),
            },
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch connection stats: {str(e)}",
        }


def get_mongo_full_health():
    """
    Retrieve a comprehensive health report of MongoDB.
    """
    try:
        health = get_mongo_health()
        uptime = get_mongo_uptime()
        storage = get_mongo_storage_stats()
        connections = get_mongo_connection_stats()

        return {
            "overall_status": health["status"],
            "health": health,
            "uptime": uptime,
            "storage_stats": storage,
            "connection_stats": connections,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch full health report: {str(e)}",
        }
