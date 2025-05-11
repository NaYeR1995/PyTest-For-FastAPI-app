from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from identity_service.DB.database import Base, AsyncSessionLocal

__all__ = [
    "Base", "AsyncSessionLocal", "get_db",
]

# Set up logging properly
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Import all tables (placeholder for your models)
# from . import models

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise
        finally:
            await db.close()
