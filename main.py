from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.setup_cors import enable_cors

from app.api.auth_router import auth_router
from app.db.db import dispose_engine, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await dispose_engine()



app = FastAPI(
    title="Contract Management System",
    version="1.0.0",
    lifespan=lifespan 
)

enable_cors(app)


# Include auth routes
app.include_router(auth_router)

