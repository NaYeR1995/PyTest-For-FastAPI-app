import traceback
import uuid
from uuid import UUID
from datetime import timedelta, datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError

import identity_service.schemas.user_schemas as user_schemas
from identity_service.DB.models.users import User

async def create_user(user: user_schemas.UserCreate, db: AsyncSession) -> User:
    try:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            email=user.email,
            password=user.password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        await db.rollback()
        traceback.print_exc()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise e

async def get_user(user_id: UUID, db: AsyncSession) -> Optional[User]:
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()
    except SQLAlchemyError as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        raise e

async def get_users(db: AsyncSession) -> Optional[List[User]]:
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except SQLAlchemyError as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        raise e

async def update_user(user_id: UUID, user_data: user_schemas.UserUpdate, db: AsyncSession) -> Optional[User]:
    try:
        user = await get_user(user_id, db)
        if not user:
            return None
        
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
            
        await db.commit()
        await db.refresh(user)
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        traceback.print_exc()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise e

async def delete_user(user_id: UUID, db: AsyncSession) -> Optional[User]:
    try:
        user = await get_user(user_id, db)
        if not user:
            return None
            
        await db.delete(user)
        await db.commit()
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        traceback.print_exc()
        raise e
    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise e