from fastapi import APIRouter, status, HTTPException, Depends
from identity_service.routes.depn import SessionDep
from identity_service.services.user import create_user, update_user, get_user, delete_user, get_users
from identity_service.schemas.user_schemas import UserCreate, UserRead, UserUpdate
from uuid import UUID
from typing import List

user_router = APIRouter(tags=["User"], prefix="/auth")

@user_router.post("/create", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: SessionDep):
    try:
        user = await create_user(user_data, db)
        return UserRead.model_validate(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")

@user_router.get('/users', response_model=List[UserRead], status_code=status.HTTP_200_OK)
async def get_all_users(db: SessionDep):
    try:
        users = await get_users(db)
        if not users:
            raise HTTPException(status_code=404, detail="Users not found!")
        return [UserRead.model_validate(user, from_attributes=True) for user in users]
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server Error")

@user_router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_db(user_id: UUID, db: SessionDep):
    try:
        user = await get_user(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")
        return UserRead.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")
    
@user_router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_202_ACCEPTED)
async def update_user_db(user_id: UUID, user_data: UserUpdate, db: SessionDep):
    try:
        user = await update_user(user_id, user_data, db)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")
        return UserRead.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")
    
@user_router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def delete_user_db(user_id: UUID, db: SessionDep):
    try:
        user = await delete_user(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found!")
        return UserRead.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")