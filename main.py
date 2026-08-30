from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.setup_cors import enable_cors

from app.api.auth_router import auth_router, contracts_router, dashboard_router, upload_router, reminders_router
from app.db.db import dispose_engine, init_db
from app.utils.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    start_scheduler()
    yield
    stop_scheduler()
    await dispose_engine()

app = FastAPI(
    title="Contract Management System",
    version="1.0.0",
    lifespan=lifespan
)

enable_cors(app)

app.include_router(auth_router)
app.include_router(contracts_router)
app.include_router(dashboard_router)
app.include_router(upload_router)
app.include_router(reminders_router)