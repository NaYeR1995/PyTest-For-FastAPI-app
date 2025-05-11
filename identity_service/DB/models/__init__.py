from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from identity_service.DB.database import Base, AsyncSessionLocal

__all__ = [
    "Base", "AsyncSessionLocal", "get_db",
    "User",
]

# Set up logging properly
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Import all tables (placeholder for your models)
from identity_service.DB.models.users import User
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            logger.info("Session is created...")
            yield db
        except Exception as e:
            await db.rollback()
            logger.error("Rollback is done due to exception: %s", e)
            raise
        finally:
            logger.info("Session is closed...")
            await db.close()
