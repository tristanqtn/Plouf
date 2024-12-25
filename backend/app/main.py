from fastapi import FastAPI
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
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
