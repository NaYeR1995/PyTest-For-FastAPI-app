from identity_service.DB import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated


SessionDep = Annotated[AsyncSession, Depends(get_db)]