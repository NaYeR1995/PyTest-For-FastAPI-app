# tests/test_users.py
import pytest
from fastapi import status
from uuid import uuid4
from identity_service.schemas.user_schemas import UserCreate, UserUpdate
import random
import string

def random_email():
    """Generate a random email for each test"""
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

@pytest.fixture(autouse=True)
async def run_around_tests(db_session):
    """Ensure each test starts with a clean slate"""
    yield
    await db_session.rollback()  # Additional safety

@pytest.mark.asyncio
async def test_create_user(async_client):
    new_email = random_email()
    test_user = UserCreate(
        first_name="John",
        last_name="Doe",
        email=new_email,  # Use random email
        password="secret123"
    )
    response = await async_client.post("/auth/create", json=test_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == new_email
    assert "user_id" in data
    
    return response.json().get("user_id")

@pytest.mark.asyncio
async def test_get_user(async_client):
    new_email = random_email()
    test_user_2 = UserCreate(
        first_name="John",
        last_name="Doe",
        email=new_email,
        password="secret123"
    )
    
    create_response = await  async_client.post("/auth/create", json=test_user_2.model_dump())
    user_id = create_response.json().get("user_id")

    response_2 = await  async_client.get(f"/auth/{user_id}")
    assert response_2.status_code == status.HTTP_200_OK
    assert response_2.json().get("first_name") == "John"
    assert response_2.json().get("email") == new_email
    return user_id

@pytest.mark.asyncio
async def test_get_all_user(async_client):
    
    response_2 = await  async_client.get(f"/auth/users")
    assert response_2.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_update_user(async_client):
    # Create test user
    new_email = random_email()
    test_user = UserCreate(
        first_name="Original",
        last_name="User",
        email=new_email,
        password="secret123"
    )

    create_response = await  async_client.post("/auth/create", json=test_user.model_dump())
    user_id = create_response.json().get("user_id")
    
    # user_id = await test_get_user(async_client)

    # Update the user
    update_data = UserUpdate(first_name="Updated")
    response = await  async_client.put(f"/auth/{user_id}", json=update_data.model_dump(exclude_unset=True))
    
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert data["first_name"] == "Updated"

@pytest.mark.asyncio
async def test_delete_user(async_client):
    # Create test user
    # new_email = random_email()
    # test_user_5 = UserCreate(
    #     first_name="ToDelete",
    #     last_name="User",
    #     email=new_email,
    #     password="secret123"
    # )
    # create_response = await async_client.post("/auth/create", json=test_user_5.model_dump())
    # user_id = create_response.json().get("user_id")
    
    user = await test_get_user(async_client)

    # Delete the user
    response_3 = await async_client.delete(f"/auth/{user}")
    assert response_3.status_code == status.HTTP_200_OK
    
    # Verify deletion
    verify_response = await async_client.get(f"/auth/{user}")
    assert verify_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client):
    fake_uuid = uuid4()
    response = await async_client.get(f"/auth/{fake_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"User with ID {fake_uuid} not found!" in response.json()["detail"]