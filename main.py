from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.db.db import init_db


app = FastAPI(
    title="Contract Management System",
    version="1.0.0"
)


# Include auth routes
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def root():
    return {
        "message": "Contract Management API is running"
    }