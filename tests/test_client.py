import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_full_client_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Cadastar cliente
        register_response = await ac.post("/auth/register", json={
            "name": "Test Client",
            "email": "client1@example.com",
            "cpf": "12312312300",
            "role": "user",
            "password": "clientpass"
        })
        assert register_response.status_code == 200

        # Login
        login = await ac.post("/auth/login", json={
            "email": "client1@example.com",
            "password": "clientpass"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # GET /clients
        response = await ac.get("/clients", headers=headers)
        assert response.status_code == 200
        clients = response.json()
        assert len(clients) > 0
        client_id = clients[0]["id"]

        # GET /clients/{id}
        response = await ac.get(f"/clients/{client_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "client1@example.com"

        # PUT /clients/{id}
        update = await ac.put(f"/clients/{client_id}", headers=headers, json={
            "name": "Updated Client",
            "email": "client1@example.com",
            "cpf": "12312312300",
            "role": "user",
            "password": "clientpass"
        })
        assert update.status_code == 200
        assert update.json()["name"] == "Updated Client"

        # DELETE /clients/{id} (requer admin)
        # Criamos admin pra isso
        await ac.post("/auth/register", json={
            "name": "Admin",
            "email": "admin@example.com",
            "cpf": "22233344455",
            "role": "user",
            "password": "adminpass"
        })
        await ac.post("/auth/login", json={
            "email": "admin@example.com",
            "password": "adminpass"
        })
        # Forzar admin na DB o teste manual
        from app.database import SessionLocal
        db = SessionLocal()
        admin = db.query(app.models.Client).filter_by(email="admin@example.com").first()
        admin.role = "admin"
        db.commit()
        db.close()

        login_admin = await ac.post("/auth/login", json={
            "email": "admin@example.com",
            "password": "adminpass"
        })
        admin_token = login_admin.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        delete = await ac.delete(f"/clients/{client_id}", headers=admin_headers)
        assert delete.status_code == 200
