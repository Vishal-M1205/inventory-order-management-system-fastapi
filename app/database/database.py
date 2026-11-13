from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import URL
from core.config import config
from sqlalchemy.pool import AsyncAdaptedQueuePool

conn_url = URL(
    host=config.database_host,
    username=config.database_user,
    password=config.database_password,
    port=config.database_port,
    drivername=config.database_drivername,
    database=config.database_name,
)

async_engine = create_async_engine(
    url=conn_url,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=3,
    max_overflow=10,
    pool_pre_ping=True,
)

AsyncSessionGenerator = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionGenerator() as session:
        yield session
