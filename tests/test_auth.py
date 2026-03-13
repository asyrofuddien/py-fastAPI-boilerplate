import pytest
from httpx import AsyncClient
from src.auth.service import UserService
from src.auth.schemas import UserCreate


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = await client.post("/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test user login."""
    # First register a user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    await client.post("/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = await client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """Test getting current user profile."""
    # Register and login
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    await client.post("/auth/register", json=user_data)
    
    login_response = await client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword123"
    })
    
    token = login_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient):
    """Test registering duplicate user fails."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    # Register first user
    response1 = await client.post("/auth/register", json=user_data)
    assert response1.status_code == 201
    
    # Try to register same user again
    response2 = await client.post("/auth/register", json=user_data)
    assert response2.status_code == 400


@pytest.mark.asyncio
async def test_invalid_login(client: AsyncClient):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401