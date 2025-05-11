# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport  # Important!
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.schema import CreateSchema, DropSchema

from identity_service.DB.models.users import TestUser, User
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

# @pytest.fixture(scope="session", autouse=True)
# async def setup_test_schema():
#     """Create and drop test schema at session start/end"""
#     async with test_engine.begin() as conn:
#         await conn.execute(CreateSchema(TEST_SCHEMA, if_not_exists=True))
#         # Create all tables in test schema
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.execute(DropSchema(TEST_SCHEMA, cascade=True))

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

@pytest.fixture
def use_test_user():
    """Fixture to ensure TestUser is used and in correct schema"""
    # Store original User table info
    original_table = User.__table__
    
    # Swap to TestUser
    User.__table__ = TestUser.__table__
    User.__table_args__ = {"schema": TEST_SCHEMA}
    
    yield
    
    # Restore original User
    User.__table__ = original_table
    User.__table_args__ = {}

# @pytest.fixture(autouse=True)
# async def clean_tables(db_session):
#     """Clean test tables between tests"""
#     try:
#         for table in Base.metadata.tables.values():
#             if table.schema == TEST_SCHEMA:
#                 await db_session.execute(table.delete())
#         await db_session.commit()
#     except Exception as e:
#         await db_session.rollback()
#         raise e


