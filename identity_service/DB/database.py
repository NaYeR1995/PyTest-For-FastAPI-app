from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from identity_service.config import settings
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
TEST_SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_TESTING.replace('postgresql://', 'postgresql+asyncpg://')

# Create a new async engine instance
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=int(settings.POOL_SIZE),
    max_overflow=int(settings.MAX_OVERFLOW),
    pool_timeout=int(settings.POOL_TIMEOUT),
    pool_recycle=int(settings.POOL_RECYCLE),
    echo_pool=True,
    # echo=True
)

# Configure async_sessionmaker to establish new async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


# Base class for public schema
Base = declarative_base()
