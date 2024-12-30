from fastapi import FastAPI  # type: ignore
from app.routes.health.mongo import mongo_health_router
from app.routes.health.api import api_health_router
from app.routes.pool.router import pool_router

import os
from dotenv import load_dotenv

load_dotenv()

# Get the port from the environment variable
PORT = int(os.getenv("BACKEND_PORT", 8000))
HOST = os.getenv("BACKEND_ADDRESS", "0.0.0.0")

BACKEND_VERSION = os.getenv("BACKEND_VERSION", "1.0.0")

app = FastAPI()

# Include the router
app.include_router(pool_router, prefix="/pool", tags=["Pool"])

app.include_router(mongo_health_router, prefix="/health/mongo", tags=["Health"])
app.include_router(api_health_router, prefix="/health/api", tags=["Health"])


@app.get("/")
async def root():
    """
    Plouf API home endpoint.
    """
    return {"message": "Welcome to Plouf backend ! 🏊‍♂️",
            "version": BACKEND_VERSION}

if __name__ == "__main__":
    import uvicorn  # type: ignore

    print(f"Starting the server at {HOST}:{PORT}")
    print(f"Backend version: {BACKEND_VERSION}")

    uvicorn.run(app, host=HOST, port=PORT)
