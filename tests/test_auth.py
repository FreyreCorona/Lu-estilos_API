import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Registro
        response = await ac.post("/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "cpf": "12345678900",
            "role": "user",
            "password": "senha123",
        })
        assert response.status_code == 200

        # Login
        response = await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "senha123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

