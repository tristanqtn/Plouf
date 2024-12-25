from fastapi import FastAPI # type: ignore
from app.routes.health.mongo import mongo_health_router
from app.routes.health.api import api_health_router

app = FastAPI()

# Include the router

app.include_router(mongo_health_router, prefix="/health/mongo", tags=["Health"])
app.include_router(api_health_router, prefix="/health/api", tags=["Health"])


@app.get("/")
async def root():
    """
    Plouf API home endpoint.
    """
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    import os
    import uvicorn # type: ignore
    from dotenv import load_dotenv

    load_dotenv()

    # Get the port from the environment variable
    PORT = int(os.getenv("BACKEND_PORT", 8000))
    HOST = os.getenv("BACKEND_ADDRESS", "127.0.0.1")

    print(f"Starting the server at {HOST}:{PORT}")

    uvicorn.run(app, host=HOST, port=PORT)
