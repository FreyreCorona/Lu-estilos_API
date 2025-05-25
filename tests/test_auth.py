from random import choice
import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app
from random import choice
@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        rnd_email = f"test{str(choice([10,99]))}@example.com"
        # Registro
        response = await ac.post("/auth/register", json={
            "name": "Test User",
            "email": rnd_email,
            "cpf": f"{str(choice([100000000,999999999]))}",
            "role": "user",
            "password": "senha123",
        })
        print(response.json())
        assert response.status_code == 200

        # Login
        response = await ac.post("/auth/login", json={
            "email": rnd_email,
            "password": "senha123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

