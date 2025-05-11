# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport  # Important!
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from identity_service.DB.models.users import User
from identity_service.main import app
from identity_service.DB.database import Base
from identity_service.DB import get_db
from identity_service.config import settings

TEST_SCHEMA = "testing"

# Test database setup
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create test engine with proper pool settings
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    # echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

@pytest.fixture
async def db_session():
    """Create a database session for each test"""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture
def client(db_session):
    """Test client that uses the same session for each test"""
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.rollback()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
async def async_client(db_session):
    """Async client fixture with proper cleanup"""
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.rollback()

    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
