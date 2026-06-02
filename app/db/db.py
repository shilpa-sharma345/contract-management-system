from sqlalchemy.orm import declarative_base
from app.constants.environ import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from urllib.parse import quote_plus
# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker  


Base = declarative_base()
safe_user= quote_plus(DB_USER)
safe_password = quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"postgresql+asyncpg://{safe_user}:{safe_password}"
    f"@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "timeout": 30,
        "command_timeout": 30,
    }
)

AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def create_connection() -> AsyncSession:
    return AsyncSessionLocal()

async def close_connection(session: AsyncSession) -> None:
    await session.close()

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def dispose_engine() -> None:
    await engine.dispose()